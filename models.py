from app import db

class Pairs(db.Model):
  """The class is used to define and manipulate the SQL table it corresponds to"""

  #: the primary key and holding integer values
  id = db.Column(db.Integer, primary_key=True)

  #: the column holding the keys, must be unique, not null
  #  and no bigger than 64 chars
  key = db.Column(db.String(64),nullable=False)

  #: the column holding the values, must be unique, not null
  #  and no bigger than 256 chars
  value = db.Column(db.String(256),nullable=False)
