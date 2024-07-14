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

from .filter_models import Make, Model, Region

Base = declarative_base()
metadata = Base.metadata


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    tg_id = Column(Integer, unique=True, nullable=False)

    username = Column(String(255), unique=True, nullable=True)
    first_name = Column(String(255), nullable=True)
    last_name = Column(String(255), nullable=True)
    full_name = Column(String(255), nullable=True)

    is_active = Column(Boolean, default=True)
    notification = Column(Boolean, default=False)

    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    # One-to-one relationship with Filter
    filter = relationship("Filter", uselist=False, back_populates="user")

    def __repr__(self):
        return f"<User {self.username}>"


class Filter(Base):
    __tablename__ = "filters"

    id = Column(Integer, primary_key=True)
    user_tg_id = Column(Integer, ForeignKey("users.tg_id", ondelete="CASCADE"))
    user = relationship("User", back_populates="filter")

    # Qiymet
    min_price = Column(Integer, default=0)
    max_price = Column(Integer, default=100000)

    # Seher
    region_id = Column(Integer, ForeignKey(Region.id))
    region_name = Column(String(20), default="Hamısı")

    # Marka
    make_id = Column(Integer, ForeignKey(Make.id))
    make_name = Column(String(20), default="Hamısı")

    # Model
    model_id = Column(Integer, ForeignKey(Model.id))
    model_name = Column(String(20), default="Hamısı")

    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    # Check constraints to ensure min_price and max_price are non-negative
    __table_args__ = (
        CheckConstraint(min_price >= 0, name="min_price_non_negative"),
        CheckConstraint(max_price >= 0, name="max_price_non_negative"),
    )

    def __repr__(self):
        return f"<Filter {self.filter}>"


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True)

    product_id = Column(Integer, unique=True, nullable=False)

    created_at = Column(DateTime, default=func.now())

    def __repr__(self):
        return f"<Car {self.car_id}>"
