# Imports

from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Instantiating

engine = create_engine('sqlite:///diAL_users.db')
db_session = scoped_session(sessionmaker(autocommit=False, bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()


# Table

class User(Base):
    """User table"""
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    login = Column(String(20), nullable=False, unique=True)
    name = Column(String(50), nullable=False)
    email = Column(String(200), nullable=False, unique=True)
    password = Column(String(20), nullable=False)
    user_type = Column(Integer, default="user", nullable=False)

    def __repr__(self):
        return f"User(id={self.id}, login={self.login}, password={self.password}, name={self.name}," \
               f" email={self.email}, user_type={self.user_type})"

    def save(self):
        db_session.add(self)
        db_session.commit()
        db_session.remove()

    def delete(self):
        db_session.delete(self)
        db_session.commit()
        db_session.remove()


def init_db():
    Base.metadata.create_all(bind=engine)


if __name__ == '__main__':
    init_db()  # Create DB
