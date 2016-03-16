from peewee import *
from playhouse.sqlite_ext import SqliteExtDatabase

# Create the database.
db = SqliteExtDatabase('peewee.db')

# Use that connection to define a base class...
class BaseModel(Model):
    class Meta:
        database = db

# ...a class to represent users...
class User(BaseModel):
    username = CharField(unique=True)

# ...and a class to represents tweets.
class Tweet(BaseModel):
    user = ForeignKeyField(User, related_name='tweets')
    message = TextField()
    is_published = BooleanField(default=True)

# Connect to the database and create a few things.
db.connect()
try:
    db.create_tables([User, Tweet])
    charlie = User.create(username='charlie')
    huey = User.create(username='huey')
    Tweet.create(user=charlie, message='My first tweet')
except OperationalError:
    pass # tables already exist

# A simple query selecting a user.
u = User.get(User.username == 'charlie')
print('user is', u.username)

# "<<" corresponds to the SQL "IN" operator.
usernames = ['charlie', 'huey', 'mickey']
users = User.select().where(User.username << usernames)
print('all selected users', [u.username for u in users])
tweets = Tweet.select().where(Tweet.user << users)
print('all selected tweets', [(t.user.username, t.is_published) for t in tweets])

# We could accomplish the same using a JOIN:
tweets = Tweet.select().join(User).where(User.username << usernames)
print('all tweets via join', [(t.user.username, t.is_published) for t in tweets])
