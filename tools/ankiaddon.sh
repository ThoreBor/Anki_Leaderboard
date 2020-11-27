#!/bin/bash

set -e

target="build/anki_leaderboard.ankiaddon"

if [ ! -e "manifest.json" ]
then
    echo "manifest.json is missing."
    echo "Make sure you are running this script from the project root."
    exit
fi

if [ -e $target ]
then
    rm -rf $target
fi

mkdir -p build

echo "Building ankiaddon file..."

zip $target *.py forms/*.py *.json README.md LICENSE

echo "Saved package at $target"