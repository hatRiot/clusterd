#!/bin/sh

#
# This application is part of the clusterd attack framework.
#

# ensure we're compiled
./buildinvoke.sh $1

# invoke
compare_result=`echo $1" > 4.0" | bc`

if [ $compare_result -gt 0 ] ; then
	echo "Running for JBOSS >= 5.x"
	java -cp .:../jbossall-client.jar:../console-mgr-classes.jar invkdeploy $1 $2 $3 $4
else
	echo "Running for JBOSS < 5.x"
	java -cp .:../jbossall-client-old.jar invkdeploy $1 $2 $3 $4

fi
