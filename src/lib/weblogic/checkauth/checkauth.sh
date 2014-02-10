#!/bin/sh

#
# This application is part of the clusterd attack framework
#

#
# This interfaces with weblogic.Admin to grab the VERSION from the remote
# weblogic server.  It's core intent is a login attempt
#
# Invocation:
#   ./checkauth.sh [remote ip] [remote port] [username] [password]
#
# Pass in "ssl" as the fifth argument if we are connecting to an SSL server
#

args=""
util="weblogic.Admin"
usr="-username $3"
pswd="-password $4"

if [ $# -eq 5 ] && [ "$5" = "ssl" ]; then
    url="-adminurl t3s://$1:$2"

    # this fixes a bug in weblogic urandom
    ssl_fix="-Djava.security.egd=file:/dev/./urandom"

    # this disregards hostname verification in SSL
    hostname="-Dweblogic.security.SSL.ignoreHostnameVerification=true"

    # most servers i've found don't bother changing up the keystore
    dks="-Dweblogic.security.SSL.trustedCAKeyStore=../DemoTrust.jks"

    # allow small RSA exponents in weak certs
    rsa="-Dweblogic.security.SSL.allowSmallRSAExponent=true"

    # constraints yo
    cons="-Dweblogic.security.SSL.enforceConstraints=off"

    # debug
    debug="-Dssl.debug=true"
    debug2="-Dweblogic.StdoutDebugEnabled=true"
    args="$ssl_fix $hostname $dks $cons $debug $debug2 $rsa $util $url $usr $pswd"
else
    url="-adminurl t3://$1:$2"
    args="$util $url $usr $pswd"
fi

java -cp .:../wlfullclient.jar:../wlcipher.jar $args VERSION 2>/dev/null
