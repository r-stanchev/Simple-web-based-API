from app import app,db
from flask import Flask, request, jsonify, make_response
from models import Pairs



@app.route('/')
def index():
  """Displays a welcome message on the home screen"""

  msg = f"Welcome to my simple web-based API.\
  Feel free to try out the different endpoints!"
  return make_response(jsonify(msg),200)


@app.route('/set')
def set_pair():
  """Adds a key-value pair to the database"""

  # Get the parameters entered in the request URI
  k = request.args.get('k')
  v = request.args.get('v')

  # Create a pair and add it to the database
  pair = Pairs(key=k,value=v)
  db.session.add(pair)
  db.session.commit()

  msg = f'The pair with key = { pair.key } and value = {pair.value} has been added!'
  return make_response(jsonify(msg),200)


@app.route('/get')
def get_value():
  """Retrieves the value coresponding to the specified key"""

  # Retrieve the key from the request URI and query the database
  # for the coresponding value
  k = request.args.get('k')
  pair = Pairs.query.filter_by(key=k).first()

  if pair is not None:
    msg = f'Value = { pair.value }'
    return make_response(jsonify(msg),200)
  else:
    msg = 'Error! Key not found.'
    return make_response(jsonify(msg),404)



@app.route('/rm')
def remove_pair():
  """Removes the pair with the specified key from the database"""

  # Retrieve the key from the request URI and extract the entire pair
  k = request.args.get('k')
  pair = Pairs.query.filter_by(key=k).first()

  if pair is not None:
    db.session.delete(pair)
    db.session.commit()
    msg = "Success! Key removed."
    return make_response(jsonify(msg),200)
  else:
    msg = "Error! The key you are trying to delete does not exist!"
    return make_response(jsonify(msg),404)



@app.route('/clear')
def remove_all():
  """Remove all key-value pairs from the database"""

  # Delete the contents of the Pairs table and
  # extract the numbers of records deleted
  record_count = Pairs.query.delete()
  db.session.commit()
  msg = f'Success! {record_count} record(s) deleted.' if record_count != 0 else f"{record_count} record(s) deleted - the table was already empty."
  return make_response(jsonify(msg),200)



@app.route('/is')
def exists():
  """Check if the specified key exists in the database"""

  # Retrieve the key from the request URI and see if it is part of an existing
  # pair in the database
  k = request.args.get('k')
  pair = Pairs.query.filter_by(key=k).first()
  if pair is not None:
    msg = "The key exists."
    return make_response(jsonify(msg),200)
  else:
    msg = "The key does not exist!"
    return make_response(jsonify(msg),404)



@app.route('/getKeys')
def get_all_keys():
  """Retrieves all keys from the database"""

  # Extract a list of tuples, each containing a key, from the database
  # and convert it to a list of keys
  keys = Pairs.query.with_entities(Pairs.key).all()
  keys = [key for key_tuple in keys for key in key_tuple]
  msg = f"The keys are: {keys}" if len(keys) != 0 else f"The table has no keys!"
  return make_response(jsonify(msg),200)



@app.route('/getValues')
def get_all_values():
  """Retrieves all values from the database"""

  # Extract a list of tuples, each containing a value, from the database
  # and convert it to a list of values
  values = Pairs.query.with_entities(Pairs.value).all()
  values = [value for values_tuple in values for value in values_tuple]
  msg = f"The values are: {values}" if len(values) != 0 else f"The table has no values!"
  return make_response(jsonify(msg),200)



@app.route('/getAll')
def get_all_pairs():
  """Retrieves all key-value pairs from the database"""

  # Extract a list of tuples, each containing a key-value pair, from the database
  # and convert it to a dictionary
  pairs = Pairs.query.all()
  list_of_pairs = { pair.key : pair.value for pair in pairs }
  msg = f"The values are: {list_of_pairs}" if len(list_of_pairs) != 0 else f"The table is empty!"
  return make_response(jsonify(msg),200)
