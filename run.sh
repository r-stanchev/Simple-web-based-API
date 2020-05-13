#!/bin/bash

# NB: The sleep commands are there to make sure that there is enough time
# between each important command
echo "======START======"

echo "~~~~~~Checking if pre-requisites are installed~~~~~~"

DIR="./cockroach_folder"
if [ -d "$DIR" ]; then
    # If the directory exists, then the pre-requisites have been installed
    sleep 1
    echo "~~~~~~Bringing up the database~~~~~~"
    # cockroach start-single-node --insecure --background
    cockroach start-single-node --insecure >> /dev/null 2>&1 &

    sleep 2
    echo "~~~~~~Activating the virtual environment~~~~~~"
    source venv/bin/activate

    sleep 1
    echo "~~~~~~Running the application~~~~~~"
    python app.py

    echo "~~~~~~Shutting down~~~~~~"
    cockroach quit --insecure
    deactivate
else
    echo "~~~~~~Downloading requirements~~~~~~"
    echo "~~~~~~Downloading CockroachDB~~~~~~"
    mkdir cockroach_folder
    cd cockroach_folder
    # Download and install CockroachDB
    wget -qO- https://binaries.cockroachdb.com/cockroach-v19.2.6.linux-amd64.tgz | tar  xvz
    sleep 1
    cp -i cockroach-v19.2.6.linux-amd64/cockroach /usr/local/bin/

    echo "~~~~~~Setting up the database~~~~~~"
    # Start a single node and execute the SQL statements,
    # necessary for the application to run
    cockroach start-single-node --insecure >> /dev/null 2>&1 &
    sleep 2
    cockroach sql --insecure --execute="CREATE USER IF NOT EXISTS maxroach;CREATE DATABASE pairs;GRANT ALL ON DATABASE pairs TO maxroach;" --user=root --host=localhost --database=pairs
    sleep 2
    cockroach quit --insecure
    cd ..

    echo "~~~~~~Setting up a virtual environment~~~~~~"
    # Install python's virual environment, in case its not present
    python3 -m pip install virtualenv
    sleep 2
    python3 -m venv venv
    sleep 2

    echo "~~~~~~Activating the virtual environment~~~~~~"
    source venv/bin/activate

    echo "~~~~~~Installing requried python libraries~~~~~~"
    pip install -r requirements.txt

    echo "~~~~~~Deactivating the virtual environment~~~~~~"
    deactivate
fi
