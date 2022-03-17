#!/bin/sh -e

if [ -d 'dist' ] ; then
    rm -r dist
fi
if [ -d 'build' ] ; then
    rm -r build
fi
if [ -d 'supervisor_gateway.egg-info' ] ; then
    rm -r supervisor_gateway.egg-info
fi