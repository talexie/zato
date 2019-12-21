#!/bin/bash

CURDIR="${BASH_SOURCE[0]}";RL="readlink";([[ `uname -s`=='Darwin' ]] || RL="$RL -f")
while([ -h "${CURDIR}" ]) do CURDIR=`$RL "${CURDIR}"`; done
N="/dev/null";pushd .>$N;cd `dirname ${CURDIR}`>$N;CURDIR=`pwd`;popd>$N

echo "*** Downloading updates ***"
if [[ -n "$(git --help|grep '\-C')" ]]; then
    git -C $CURDIR pull
else
    pushd $CURDIR
    git pull
    popd
fi

# Uninstall old dependencies
$CURDIR/bin/pip uninstall -y sec-wall
$CURDIR/bin/pip uninstall -y springpython
$CURDIR/bin/pip uninstall -y zato-apitest

echo "*** Installing updates ***"
$CURDIR/bin/pip install -e $CURDIR/zato-cy
$CURDIR/bin/pip install -r $CURDIR/requirements.txt
