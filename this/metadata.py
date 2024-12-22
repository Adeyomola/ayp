from sqlalchemy import MetaData, Table, Column, Integer, String, TIMESTAMP, Text, ForeignKey, NVARCHAR, Boolean, VARCHAR
import datetime

def metadata():
    md = MetaData()

    users = Table(
    'users', md, 
    Column('id', Integer, primary_key = True, autoincrement=True),
    Column('username', String(255), unique=True),
    Column('password', String(255)),
    Column('email', String(255), unique=True),
    Column('image_url', String(255)),
    Column('bio', String(500))
        )
    post = Table(
    'post', md,
    Column('id', Integer, primary_key = True, autoincrement=True),
    Column('author_id', Integer, ForeignKey('users.id'), nullable=False),
    Column('firstname', String(255)),
    Column('created', TIMESTAMP, default=datetime.datetime.now),
    Column('title', VARCHAR(255), nullable=False),
    Column('body', Text, nullable=False),
    Column('image_url', String(255)),
    Column('category', VARCHAR(255), nullable=False),
    Column('fragment', VARCHAR(255), nullable=False, unique=True),
    Column('image_credit', VARCHAR(200)),
    Column('meta', VARCHAR(140)),
    )
    comments = Table(
    'comments', md,
    Column('id', Integer, primary_key = True, autoincrement=True),
    Column('post', Integer),
    Column('name', Text, nullable=False),
    Column('comment', Text, nullable=False),
    )
    return md