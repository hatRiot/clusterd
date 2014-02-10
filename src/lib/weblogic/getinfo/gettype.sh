#!/bin/sh

#
# This application is part of the clusterd attack framework
#

#
# This interfaces with weblogic.Admin to pull specific JVM and host information.
# Even though I can use -property to fetch individual properties, its much quicker
# to grab everything at once.
#
# Invocation:
#   ./gettype.sh [remote ip] [remote port] [username] [password] [type]
#
# Where type is the MBean type to dump info from.  A list of these can be found at:
#   http://middlewaremagic.com/weblogic/?tag=weblogic-utilities
# You can also use "query -pattern *:*" to fetch all MBeans.
#
# Pass in "ssl" as the sixth argument if we are connecting to an SSL server
#

args=""
util="weblogic.Admin"
usr="-username $3"
pswd="-password $4"

if [ $# -eq 6 ] && [ "$6" = "ssl" ]; then
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

java -cp .:../wlfullclient.jar:../wlcipher.jar $args GET -type $5 -pretty 2>/dev/null
