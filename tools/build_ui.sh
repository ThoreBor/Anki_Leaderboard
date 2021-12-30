#!/bin/bash

set -e

# Argument parsing
# https://stackoverflow.com/a/14203146
POSITIONAL=()
while [[ $# -gt 0 ]]; do
    key="$1"

    case $key in
        -b|--build-tool)
            TOOL="$2"
            shift # past argument
            shift # past value
            ;;
        *)    # unknown option
            POSITIONAL+=("$1") # save it in an array for later
            shift # past argument
            ;;
    esac
done

set -- "${POSITIONAL[@]}" # restore positional parameters

if [ ! "${TOOL}" ]; then
    TOOL="pyuic5"
elif [[ ! "${TOOL}" = "pyuic5" && ! "${TOOL}" = "pyuic6" ]]; then
    echo "Only 'pyuic5' or 'pyuic6' are permitted for -b|--build-tool. Defaults to 'pyuic5' when omitted."
    echo "Exiting..."
    exit 1
fi

if [ "${TOOL}" = "pyuic5" ]; then
    OPTIONS="--from-imports"
fi

if [ ! -d "designer" ]
then
    echo "Please run this from the project root"
    exit
fi

mkdir -p forms

echo "Generating forms..."
for i in designer/*.ui
do
    base=$(basename $i .ui)
    py="forms/${base}.py"
    if [ $i -nt $py ]; then
        echo " * "$py
        ${TOOL} ${OPTIONS} $i -o $py
    fi
done

echo "Building resources.."
pyrcc5 designer/icons.qrc -o forms/icons_rc.py
