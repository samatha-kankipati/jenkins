#!/bin/bash
rm -rf ../docs/api-doc/*
rmdir ../docs/api-doc
mkdir ../docs/api-doc
rm -rf ../docs/repo-doc/*
rmdir ../docs/repo-doc
mkdir ../docs/repo-doc
epydoc --html -v --inheritance grouped --url https://github.rackspace.com/Cloud-QE/CloudCAFE-Python --name "CloudCAFE-Pythoni API" -o ../docs/api-doc ../lib/ccengine
epydoc --html -v --inheritance grouped --url https://github.rackspace.com/Cloud-QE/CloudCAFE-Python --name "CloudCAFE-Pythoni Test Repository" -o ../docs/repo-doc ../lib/testrepo
