#!/bin/bash

set -e

if [ ! -d "designer" ]
then
    echo "Please run this from the project root"
    exit
fi

mkdir -p forms/pyqt5UI
mkdir -p forms/pyqt6UI

#pyqt5

echo "Generating pyqt5 forms..."
for i in designer/*.ui
do
    base=$(basename $i .ui)
    py="forms/pyqt5UI/${base}.py"
    if [ $i -nt $py ]; then
        echo " * "$py
        pyuic5 $i -o $py
    fi
done

#pyqt6

echo "Generating pyqt6 forms..."
for i in designer/*.ui
do
    base=$(basename $i .ui)
    py="forms//pyqt6UI/${base}.py"
    if [ $i -nt $py ]; then
        echo " * "$py
        pyuic6 $i -o $py
    fi
done