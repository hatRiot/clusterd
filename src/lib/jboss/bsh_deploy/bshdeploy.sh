#!/bin/sh

#
# This application is part of the clusterd attack framework.
#

# ensure we're compiled
if [ ! -f "bshdeploy.class" ]; then
    ./buildbsh.sh
fi

# invoke
java -cp .:../console-mgr-classes.jar:../jbossall-client.jar bshdeploy $1 $2 $3 $4 $5
