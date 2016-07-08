#!/bin/bash
#############################################
# Assume that supervisor has been installed
#############################################
chmod +x superd
cp superd /etc/init.d
cp super.conf /etc/super.conf
mkdir /etc/superd
cp colorize.conf /etc/superd
