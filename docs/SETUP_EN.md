# HOW TO SETUP ENVIRONMENT AND RUN PROJECT LOCALLY

## Requirements

- python 3.8
- python3-pip
- virtualenv

## Installation

### Linux

```
    # remember run a generally update before installing new packages.
    sudo apt-get update

    # install python3
    sudo apt-get install python3
    # you can confirm instalation checking out the version with command: python3 --version

    # install pip3
    sudo apt-get install python3-pip
    # you can confirm instalation checking out the version with command: pip3 --version

    # install virtualenv
    sudo pip3 install virtualenv
    # you can confirm instalation checking out the version with command: virtualenv --version
```

### Mac

```
    [complete]
```

### Windows

```
    [complete]
```

## Setup

```
    # virtualenv encapsulates python dependencies so they affect only ACADEMIA_BLOCKCHAIN project.
    # if it is the first time you run the project, create a virtualenv for this project.
    virtualenv acbc_env

    # activate virtualenv.
    source acbc_env/bin/activate

    # Once virtualenv is active, install all libs listed in requirements.txt
    pip install -r requirements.txt

    # After libs are installed, env is ready. We use Django framework.
    # Run DB migrations.
    python manage.py migrate

    # postgresql is not needed (sqlite3 is enaugh), as postgres is used in server. See Django docs.

    # Run server locally.
    python manage.py runserver

    # Access to the project in localhost:8000. 

    # When you finish your work, deactivate virtualenv.
    deactivate
```

### Common errors

- Error: pg_config executable not found when installing psycopg2

    **Answer**: https://stackoverflow.com/questions/11618898/pg-config-executable-not-found

        `pg_config` is in `postgresql-devel` (`libpq-dev` in Debian/Ubuntu, `libpq-devel` on Centos/Cygwin/Babun). So, in Ubuntu:

        `sudo apt-get install libpq-dev python-dev`

- raise KeyError(key) from None. KeyError: 'ACADEMIA_BLOCKCHAIN_SKEY'

    **Answer**: you have to set environment variable ACADEMIA_BLOCKCHAIN_SKEY.

    ```
    # in root project folder create .env file and fill it with variables and values, for example:
    ACADEMIA_BLOCKCHAIN_SKEY="your-secret-key"

    # load .env file in your virtualenv postactivate script
    set -a; source ./.env; set +a

    # in console, check if variable was set correctly.
    echo $ACADEMIA_BLOCKCHAIN_SKEY
    ```
