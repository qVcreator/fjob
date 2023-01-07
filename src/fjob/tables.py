from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    DateTime,
    ForeignKey,
    DECIMAL,
    CheckConstraint
)
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.sql import functions

Base = declarative_base()


class BaseUser(Base):
    __tablename__ = 'base-user'
    id = Column(Integer, primary_key=True)
    first_name = Column(String, nullable=False)
    second_name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    date_create = Column(DateTime(timezone=True), server_default=functions.now())
    date_update = Column(DateTime(timezone=True), onupdate=functions.now())
    role = Column(String, nullable=False)
    is_deleted = Column(Boolean)
    type = Column(String(50))

    __mapper_args__ = {
        "polymorphic_identity": "base-user",
        "polymorphic_on": type,
    }


class BasicUser(BaseUser):
    __tablename__ = 'users'
    id = Column(Integer, ForeignKey("base-user.id"), primary_key=True)

    __mapper_args__ = {
        "polymorphic_identity": "users",
    }


class Executors(BaseUser):
    __tablename__ = 'executors'
    id = Column(Integer, ForeignKey("base-user.id"), primary_key=True)

    __mapper_args__ = {
        "polymorphic_identity": "executors",
    }


class Suggestions(Base):
    __tablename__ = 'suggestions'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    executor_id = Column(Integer, ForeignKey("executors.id"))
    name = Column(String(50), nullable=False)
    description = Column(String(255), nullable=False)
    price = Column(DECIMAL, nullable=False)
    category = Column(String)
    status = Column(String, nullable=False)

    user = relationship("BasicUser", backref='suggestions')
    executor = relationship("Executors", backref='suggestions')


class Comments(Base):
    __tablename__ = 'comments'
    id = Column(Integer, primary_key=True)
    user_from_id = Column(Integer, ForeignKey('base-user.id'))
    user_to_id = Column(Integer, ForeignKey('base-user.id'))
    rating = Column(Integer, CheckConstraint("rating>0 and rating<=5"), nullable=False)
    text = Column(String, nullable=False)

    user_from = relationship("BaseUser", foreign_keys=[user_from_id])
    user_to = relationship("BaseUser", foreign_keys=[user_to_id])
