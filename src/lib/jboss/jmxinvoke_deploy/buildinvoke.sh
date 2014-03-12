#!/bin/sh

#
# This application is part of the clusterd attack framework.
# 
# This file builds the JMXInvokerServlet deployer.
#

compare_result=`echo $1" > 4.0" | bc`

if [ $compare_result -gt 0 ] ; then
	echo "Compiling for JBOSS >= 5.x"
	javac -cp ..:../jbossall-client.jar:../console-mgr-classes.jar invkdeploy.java TrustModifier.java
else
	echo "Compiling for JBOSS < 5.x"
	javac -cp ..:../jbossall-client-old.jar invkdeploy.java TrustModifier.java

fi