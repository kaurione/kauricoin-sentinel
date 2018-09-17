#!/bin/bash
set -evx

mkdir ~/.kauricoincore

# safety check
if [ ! -f ~/.kauricoincore/.kauricoin.conf ]; then
  cp share/kauricoin.conf.example ~/.kauricoincore/kauricoin.conf
fi
