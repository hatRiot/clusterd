#!/usr/bin/env python

import sys
from shutil import rmtree
from os import getcwd, mkdir, path
sys.path.insert(0, getcwd() + '/src/core/')

from fingerprint import FingerEngine
from src.module import generate_payload, deploy_utils, discovery
from auxengine import auxengine
from parse_cmd import parse
from log import LOG
import platform
import utility
import state

""" Clustered environment exploitation framework
"""

def prerun(options):
    """ Run misc flags that don't necessarily have anything to do
    with fingerprinting or exploiting.
    """

    # first check if we need to generate a payload
    if options.generate_payload:
        generate_payload.run(options)

    # Check to see if we need to run the discovery module
    if options.discovery_file:
        discovery.run(options)

    # then check if they want a listing of all deployers
    if options.deploy_list:
        deploy_utils.deploy_list(options.deploy_list)

    if options.aux_list:
        deploy_utils.auxiliary_list(options.aux_list)

    if path.isdir(state.serve_dir):
        # stale temp dir from a crash, etc.
        rmtree(state.serve_dir)

    # create our temporary directory
    mkdir(state.serve_dir)


def postrun(options):
    """ Cleanup routine after everything is done
    """

    rmtree(state.serve_dir, ignore_errors=True)


def run(options):
    """ Parse up our hosts and run fingerprinting/exploitation
    on each one
    """

    servers = []
    if options.input_list:
        with open(options.input_list, 'r') as f:
            for ip in f.readlines():
                if ip.count('.') < 3:
                    rip = utility.resolve_host(ip.strip())
                    if rip:
                        servers.append(rip)
                    else:
                        utility.Msg("Host %s could not be resolved.  Skipping." % 
                                                            ip.strip(), LOG.DEBUG)
                else:
                    servers.append(ip.strip())
                    
        utility.Msg("Loaded %d servers." % len(servers))
    else:
        if options.ip.count('.') < 3:
            ip = utility.resolve_host(options.ip)
            if ip:
                servers.append(ip)
            else:
                utility.Msg("Could not resolve hostname %s" % options.ip, LOG.ERROR)
                return
        else:
            servers.append(options.ip)

    utility.Msg("Servers' OS hinted at %s" % options.remote_os)
    # iterate through all servers, fingerprint and load auxengine
    for server in servers:
        fingerengine = FingerEngine()
        fingerengine.options = options
        fingerengine.options.ip = server

        fingerengine.run()
        if len(fingerengine.fingerprints) is 0:
            continue

        utility.Msg("Fingerprinting completed.", LOG.UPDATE)

        # We've got the host fingerprinted, now kick off the
        # exploitation engine for the service
        utility.Msg("Loading auxiliary for '%s'..." % fingerengine.service,
                                                      LOG.DEBUG)

        # execute the auxiliary engine
        auxengine(fingerengine)

if __name__ == "__main__":

    utility.header()
    options = parse(sys.argv[1:])

    # set platform
    state.platform = platform.system().lower()

    utility.Msg("Started at %s" % (utility.timestamp()))

    # log the CLI args
    utility.log(' '.join(sys.argv))

    try:
        prerun(options)

        if options.ip or options.input_list:
            run(options)

        postrun(options)
    except KeyboardInterrupt:
        pass

    utility.Msg("Finished at %s" % (utility.timestamp()))
