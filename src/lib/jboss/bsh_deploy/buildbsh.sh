#!/bin/sh

# 
# This application is part of the clusterd attack framework.
#
# This file builds the BSHDeploy deployer
#
javac -cp ..:../jbossall-client.jar:../console-mgr-classes.jar bshdeploy.java
