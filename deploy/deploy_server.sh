#!/bin/sh
set -e

SCRIPT=`realpath $0`
SCRIPTPATH=`dirname $SCRIPT`
#PYTHON="$SCRIPTPATH/../venv/bin/python"
#PIPENV="$SCRIPTPATH/../venv/bin/pip"
PYTHON="python"
PIPENV="pipenv"

echo "Deploying application ..."

#cd $(dirname $SCRIPTPATH)
cd /home/admin/app

# Update codebase
git fetch origin master
git reset --hard origin/master

$PIPENV install

# collect static stuff
$PYTHON manage.py collectstatic --noinput;

# Migrate database
$PYTHON manage.py migrate

systemctl --user restart django_deploy_test

echo "Application deployed!"

