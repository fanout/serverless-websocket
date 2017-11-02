#!/bin/sh
set -e

rm -rf lambda-package lambda-package.zip
mkdir lambda-package
cp -a venv/lib/python2.7/site-packages/* lambda-package
cp *.py lambda-package
cd lambda-package && zip -q -r ../lambda-package.zip *
