import enum

from sqlalchemy import Column, Integer, String, ForeignKey, Enum, Numeric, DateTime, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

wish_list_to_challenge = Table(
    'wish_list_to_challenge',
    Base.metadata,
    Column('wish_list_fk', Integer, ForeignKey('wish_list.id', onupdate='CASCADE', ondelete='CASCADE'), nullable=True),
    Column('challenge_fk', Integer, ForeignKey('challenge.id', onupdate='CASCADE', ondelete='RESTRICT'),
           nullable=False),
    Column('user_fk', Integer, ForeignKey('user.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
)

recommended_challenges = Table(
    'recommended_challenges',
    Base.metadata,
    Column('challenge_fk', Integer, ForeignKey('challenge.id', onupdate='CASCADE', ondelete='RESTRICT'),
           nullable=False),
    Column('user_fk', Integer, ForeignKey('user.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
)


class PeriodType(enum.Enum):
    daily = 0
    weekly = 1
    monthly = 2
    half_yearly = 3
    yearly = 4


class ChallengeDifficulty(enum.Enum):
    easy = 0
    medium = 1
    hard = 2
    insane = 3


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    username = Column(String(255), nullable=False, unique=True)
    email = Column(String, nullable=False)
    pass_hash = Column(String(64), nullable=False)
    photo_url = Column(String)

    items = relationship("Item", lazy="dynamic")
    wish_list = relationship("WishList", lazy="dynamic")
    challenges = relationship(
        "Challenge",
        secondary=wish_list_to_challenge,
        lazy='subquery',
    )
    recommended_challenges = relationship(
        "Challenge",
        secondary=recommended_challenges,
        lazy='subquery',
    )


class Category(Base):
    __tablename__ = "category"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False, unique=True)
    description = Column(String)
    color = Column(String(10))

    def dump(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "color": self.color,
        }


class SubCategory(Base):
    __tablename__ = "sub_category"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    description = Column(String)
    color = Column(String(10))
    period = Column(Enum(PeriodType))

    category = relationship("Category", lazy='subquery')

    category_fk = Column(Integer, ForeignKey('category.id', onupdate='CASCADE', ondelete='RESTRICT'), nullable=False)

    def dump(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "color": self.color,
            "period": self.period.name,
            "category": self.category.dump(),
        }


class Item(Base):
    __tablename__ = "item"

    id = Column(Integer, primary_key=True)
    price = Column(Numeric, nullable=False)
    amount = Column(Numeric, nullable=False)
    name = Column(String, nullable=False)
    date = Column(DateTime, nullable=False)
    description = Column(String)

    sub_category = relationship("SubCategory")

    sub_category_fk = Column(Integer, ForeignKey('sub_category.id', onupdate='CASCADE', ondelete='RESTRICT'),
                             nullable=False)
    user_fk = Column(Integer, ForeignKey('user.id', onupdate='CASCADE', ondelete='CASCADE'), nullable=False)


class Challenge(Base):
    __tablename__ = "challenge"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    photo_url = Column(String)
    full_description = Column(String)
    brief_description = Column(String)
    earn_amount = Column(Numeric)
    difficulty = Column(Enum(ChallengeDifficulty))

    sub_category = relationship("SubCategory")
    wish_list = relationship(
        "WishList",
        secondary=wish_list_to_challenge,
        back_populates="challenges"
    )

    sub_category_fk = Column(Integer, ForeignKey('sub_category.id', onupdate='CASCADE', ondelete='CASCADE'),
                             nullable=False)

    def dump(self):
        return {
            "id": self.id,
            "name": self.name,
            "photo_url": self.photo_url,
            "full_description": self.full_description,
            "brief_description": self.brief_description,
            "earn_amount": self.earn_amount,
            "difficulty": self.difficulty.name,
            "sub_category": self.sub_category.dump(),
        }


class WishList(Base):
    __tablename__ = "wish_list"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    photo_url = Column(String)
    amount = Column(Numeric)
    price = Column(Numeric, nullable=False)
    description = Column(String)

    challenges = relationship(
        "Challenge",
        secondary=wish_list_to_challenge,
        back_populates="wish_list",
    )

    user_fk = Column(Integer, ForeignKey('user.id', onupdate='CASCADE', ondelete='CASCADE'), nullable=False)

    def dump(self):
        return {
            "id": self.id,
            "name": self.name,
            "photo_url": self.photo_url,
            "amount": self.amount,
            "price": self.price,
            "description": self.description,
        }
