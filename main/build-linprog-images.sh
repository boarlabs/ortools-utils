#!/bin/bash

TAG=1.0-cbc-glpk



build() {
    NAME=$1
    IMAGE=linprog-$NAME:$TAG
    # FILE=./linprog-$NAME/Dockerfile
    WD=./linprog-$NAME
    echo '--------------------------' building $IMAGE in $WD 
    cd $WD
    docker build -t $IMAGE .
    cd ..
}

#

build service
build extensions
