#!/usr/bin/env bash

# pylint
pylint --rcfile .pylintrc src/api/


#pytest
cd src
coverage run --source='.' manage.py test
coverage html
