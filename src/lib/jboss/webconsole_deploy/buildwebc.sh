#!/bin/sh

#
# This application is part of the clusterd attack framework.
# this file builds our web-console deployer.

javac -cp ..:../jbossall-client.jar:../console-mgr-classes.jar webc_deploy.java
