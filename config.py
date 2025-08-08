import os
from box import Box

MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017')
MONGO_DB = os.getenv('MONGO_DB', 'data01')

config = Box({'db': {'mongo': {'uri': MONGO_URI, 'db': MONGO_DB}}})
