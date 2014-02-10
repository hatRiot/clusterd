#!/bin/sh

#
# This application is part of the clusterd attack framework
#

# 
# This interfaces with weblogic.Deployer to fetch a list of all deployed apps
#
# Invocation:
#   ./list_apps.sh [remote ip] [remote port] [username] [password]
#
# Pass in "ssl" as the fifth argument if we are connecting to an SSL server
#

args=""
util="weblogic.Deployer"
usr="-username $3"
pswd="-password $4"

if [ $# -eq 5 ] && [ "$5" = "ssl" ]; then
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

java -cp .:../wlfullclient.jar:../wlcipher.jar $args -listapps 2>/dev/null
