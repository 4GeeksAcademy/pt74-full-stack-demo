rm -R -f ./migrations;
pipenv run init;
dropdb -h localhost -U gitpod example;
createdb -h localhost -U gitpod example;
psql -h localhost example -U gitpod -c 'CREATE EXTENSION unaccent;';
pipenv run migrate;
pipenv run upgrade;
