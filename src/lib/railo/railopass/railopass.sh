#!/bin/sh

#
# This application is part of the clusterd attack framework
#

# ensure we're compiled
if [ ! -f "RailoPasswordTool.class" ]; then
    ./buildpass.sh
fi

# invoke
java RailoPasswordTool d $1 
