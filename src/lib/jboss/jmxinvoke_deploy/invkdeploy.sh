#!/bin/sh

#
# This application is part of the clusterd attack framework.
#

# ensure we're compiled
./buildinvoke.sh $1

# invoke
compare_result=`echo $1" > 4.0" | bc`

if [ "$compare_result" -gt 0 ] ; then
    if [ "$#" -gt 5 ] ; then
        java -cp .:../jbossall-client.jar:../console-mgr-classes.jar invkdeploy $1 $2 $3 $4 $5 $6
    else
        java -cp .:../jbossall-client.jar:../console-mgr-classes.jar invkdeploy $1 $2 $3 $4
    fi
else
    if [ "$#" -gt 5 ] ; then
        java -cp .:../jbossall-client-old.jar invkdeploy $1 $2 $3 $4 $5 $6
    else
        java -cp .:../jbossall-client-old.jar invkdeploy $1 $2 $3 $4
    fi
fi
