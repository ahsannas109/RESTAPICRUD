class User:
  def __init__(self, id, username, password, active):
    self.id = id
    self.username = username
    self.password = password
    self.active = active

  def __repr__(self):
    return '<id {}>'.format(self.id)

  def serialize(self):
    return {
    #   you can ge tid if required not in this case
       'id': self.id,
      'username': self.username,
      'password': self.password,
      'active':self.active
    }