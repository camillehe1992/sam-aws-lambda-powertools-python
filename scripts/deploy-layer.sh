#!/bin/sh

ZIP_NAME=aws-lambda-powertools-python

echo "Build and deploy $ZIP_NAME.zip"

rm -rf .build

pip3 install -r layers/requirements.txt -t .build/$ZIP_NAME/python

cd .build/$ZIP_NAME

zip -r ../$ZIP_NAME.zip python

cd ..

aws s3 cp $ZIP_NAME.zip s3://aws-lambda-powertools-python-756143471679
