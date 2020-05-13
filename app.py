from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

# Disable the tracking of modifications to objects
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Configure the database type, username, host, port and database name
app.config['SQLALCHEMY_DATABASE_URI'] = 'cockroachdb://maxroach@localhost:26257/pairs'

# Configure an insecure connection since we are using an
# insecure CockroachDB cluster
connect_args = {'sslmode' : 'disable'}
engine_options = {"connect_args" : connect_args}

# Bind the ORM to this specific Flask application,
# using the specified engine options
db = SQLAlchemy(app,engine_options=engine_options)


from views import *

if __name__ == "__main__":
  db.create_all()     # Create the Pairs table
  app.run()


