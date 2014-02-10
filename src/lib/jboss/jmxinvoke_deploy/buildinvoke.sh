#!/bin/sh

#
# This application is part of the clusterd attack framework.
# 
# This file builds the JMXInvokerServlet deployer.
#
javac -cp ..:../jbossall-client.jar:../console-mgr-classes.jar invkdeploy.java TrustModifier.java
