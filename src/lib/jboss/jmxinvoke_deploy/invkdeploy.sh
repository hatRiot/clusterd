#!/bin/sh

#
# This application is part of the clusterd attack framework.
#

# ensure we're compiled
if [ ! -f "invkdeploy.class" ]; then
    ./buildinvoke.sh
fi

# invoke
java -cp .:../console-mgr-classes.jar:../jbossall-client.jar invkdeploy $1 $2 $3
