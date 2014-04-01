#!/bin/sh

#
# This application is part of the clusterd attack framework.
# 
# This file builds the JMXInvokerServlet deployer.
#

compare_result=`echo $1" > 4.0" | bc`

if [ "$compare_result" -gt 0 ]; then
	javac -cp ..:../jbossall-client.jar:../console-mgr-classes.jar invkdeploy.java TrustModifier.java
else
	javac -cp ..:../jbossall-client-old.jar invkdeploy.java TrustModifier.java

fi
