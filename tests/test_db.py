import unittest
from peewee import *

from app import TimelinePost

MODELS = [TimelinePost]

# Use in-memory SQLite database for testing
test_db = SqliteDatabase(':memory:')

class TestTimelinePost(unittest.TestCase):
  def setUp(self):
    # Bind model classes to test db
    # No need to recursively bind dependencies, b/c we have a complete list of all models
    test_db.bind(MODELS, bind_refs=False, bind_backrefs=False)

    test_db.connect()
    test_db.create_tables(MODELS)

  def tearDown(self):
    # Not strictly necessary since the DB is only in memory and dropped at end of connection
    # But good practice
    test_db.drop_tables(MODELS)

    test_db.close()
  
  def test_timeline_post(self):
    first_post = TimelinePost.create(name="Ethan Jin", email="example@gmail.com", content="Hello world, I'm Ethan!")
    assert first_post.id == 1

    second_post = TimelinePost.create(name="Bob Smith", email="bob@smith.com", content="Hello World, I'm Bob!")
    assert second_post.id == 2

    first_post_from_db = TimelinePost.get(TimelinePost.id == 1)
    assert first_post_from_db.name == "Ethan Jin" and first_post_from_db.email == "example@gmail.com" and first_post_from_db.content == "Hello world, I'm Ethan!"

    second_post_from_db = TimelinePost.get(TimelinePost.id == 2)
    assert second_post_from_db.name == "Bob Smith" and second_post_from_db.email == "bob@smith.com" and second_post_from_db.content == "Hello World, I'm Bob!"
    

