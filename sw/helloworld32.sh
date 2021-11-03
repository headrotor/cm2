#!/bin/bash

START=16

while [ $START -ge -128 ]
do
    curl -s "http://192.168.1.145:8000/?x=${START}&y=10&bright=2&text=Hello%20World"

    START=$((START -1))
    echo ${START}
done
