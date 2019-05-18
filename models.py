from sqlalchemy import Column, Boolean, Integer, Text
from database import Base
from flask_login import UserMixin

# user class
class User(UserMixin, Base):
    __tablename__ = 'users'
    id = Column(Text, nullable=False, unique=True, primary_key=True)
    username = Column(Text, nullable=False, unique=True)
    password = Column(Text, nullable=False)
    active = Column(Boolean, nullable=False, default=True)

    def __init__(self, id=None, username=None, password=None, active=False):
        self.id = id
        self.username = username
        self.password = password
        self.active = active

    def is_active(self):
        return self.active

    def get(id):
        if self.id == id:
            return self
        else:
            return None

    def __repr__(self):
        return '<%s(%r, %r)>' % (self.__class__.__name__, self.id, self.username)