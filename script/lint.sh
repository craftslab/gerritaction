#!/bin/bash

list="gerritaction,tests"

old=$IFS IFS=$','
for item in $list; do
  black --line-length=88 $item
  flake8 --ignore=E501,F841,W503,W605 --max-line-length=88 $item
done
IFS=$old
