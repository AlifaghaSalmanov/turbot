from sqlalchemy import (
    VARCHAR,
    Boolean,
    CheckConstraint,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.dialects.mysql import LONGTEXT
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import backref, relationship, sessionmaker
from sqlalchemy.sql import func

Base = declarative_base()
metadata = Base.metadata


class Region(Base):
    __tablename__ = "regions"

    id = Column(Integer, primary_key=True)
    name = Column(VARCHAR(255), unique=True, nullable=False)

    created_at = Column(DateTime, default=func.now())

    def __repr__(self):
        return f"<Region {self.name}>"


class Make(Base):
    __tablename__ = "makes"

    id = Column(Integer, primary_key=True)
    name = Column(VARCHAR(255), unique=True, nullable=False)

    created_at = Column(DateTime, default=func.now())

    def __repr__(self):
        return f"<Make {self.name}>"


class Model(Base):
    __tablename__ = "models"

    id = Column(Integer, primary_key=True)

    make_id = Column(Integer, ForeignKey(Make.id))
    make = relationship("Make", backref="models")
    make_name = Column(VARCHAR(255), nullable=False)

    name = Column(VARCHAR(255), unique=True, nullable=False)

    created_at = Column(DateTime, default=func.now())

    def __repr__(self):
        return f"<Model {self.name}>"
