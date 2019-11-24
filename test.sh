#!/usr/bin/env bash

# pylint
pylint --rcfile .pylintrc src/api_rest/


#pytest
cd src
coverage run --source='.' manage.py test
coverage html
