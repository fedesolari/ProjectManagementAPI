# Setting up our environment

**THIS IS TRULY IMPORTANT**
We must be using python 3.10.6
Too check wich version of python we have we can use the command *python --version*

## This is for linux
python3 -m venv env

source env/bin/activate

**IMPORTANT**
Before we install our requirements we must add this dependency
- psycopg2-binary==2.9.3

pip install -r requirements.txt

## This is for windows

You need to know that if you are using git bash this following commands won't be useful, you must use the commands above

Once you have installed python you must install pip and we get that with the next 2 commands:
- curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
- python get-pip.py

And now we set up our application environment
- python -m venv env
- env\Scripts\activate or .\env\Scripts\activate

**IMPORTANT**
Before we install our requirements we must add this dependency
- psycopg2==2.9.6

pip install -r requirements.txt

# We must install docker

- windows: [link](https://docs.docker.com/desktop/install/windows-install/)
- linux: [link](https://phoenixnap.com/kb/install-docker-on-ubuntu-20-04)

## Useful commands:

- build: docker-compose build
- get up: docker-compose up -d
- build and up: docker-compose -f docker-compose.yml up -d --build
- turn down: docker-compose down

# Connect to local postgres db

## First of all we must install postgresql

- windows: [link](https://www.enterprisedb.com/downloads/postgres-postgresql-downloads)
- linux: sudo apt-get install postgresql

## Local
### For linux
psql -p 5434 -U postgres -h 0.0.0.0

### [For windows](https://stackoverflow.com/questions/56993263/connect-to-dockerized-postgres-from-windows-docker-host)


## Remote 
PGPASSWORD=0aFeWQNYnsFSpYDeaW9jwpDhxKfQXRC2 psql -h dpg-chsk4uhmbg57s5r5m1d0-a.oregon-postgres.render.com -U support main_070f
