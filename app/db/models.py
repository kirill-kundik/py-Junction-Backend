import enum

from sqlalchemy import Column, Integer, String, ForeignKey, Enum, Numeric, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class PeriodType(enum.Enum):
    daily = 0
    weekly = 1
    monthly = 2
    half_yearly = 3
    yearly = 4


class Category(Base):
    __tablename__ = "category"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    description = Column(String)
    color = Column(String(10))


class SubCategory(Base):
    __tablename__ = "sub_category"
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    description = Column(String)
    color = Column(String(10))
    period = Column(Enum(PeriodType))

    category = relationship("Category")

    category_fk = Column(Integer, ForeignKey('category.id', onupdate='CASCADE', ondelete='RESTRICT'), nullable=False)


class Item(Base):
    __tablename__ = "item"

    id = Column(Integer, primary_key=True)
    price = Column(Numeric, nullable=False)
    amount = Column(Integer, nullable=False)
    name = Column(String, nullable=False)
    date = Column(DateTime, nullable=False)

    sub_category = relationship("SubCategory")

    sub_category_fk = Column(Integer, ForeignKey('sub_category.id', onupdate='CASCADE', ondelete='RESTRICT'),
                             nullable=False)
