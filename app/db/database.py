from contextlib import contextmanager
from typing import List

from sqlalchemy import create_engine, or_, and_
from sqlalchemy.orm import sessionmaker

import app
from .models import *
from .exceptions import *
from app.utilities import Singleton


class Database(metaclass=Singleton):
    def __init__(self):
        self.engine = create_engine(app.Config.DATABASE_URI)
        self.Session = sessionmaker(bind=self.engine)

    @contextmanager
    def _session_scope(self):
        session = self.Session(expire_on_commit=False)
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    def add_user(self, user: User) -> bool or UserAlreadyExists:
        with self._session_scope() as s:
            check_user = s.query(User).filter(
                or_(User.username == user.username, User.email == user.email)).one_or_none()
            if check_user is not None:
                s.add(user)
            else:
                raise UserAlreadyExists
            return True

    def get_user_by_id(self, user_id: int) -> User or UserIsNotExist:
        with self._session_scope() as s:
            user = s.query(User).filter(User.id == user_id).one_or_none()
            if user is None:
                raise UserIsNotExist
        return user

    def get_user_by_username(self, username: str) -> User or UserIsNotExist:
        with self._session_scope() as s:
            user = s.query(User).filter(User.username == username).one_or_none()
            if user is None:
                raise UserIsNotExist
        return user

    def get_all_users(self) -> List[User]:
        with self._session_scope() as s:
            users = s.query(User).all()
        return users

    def update_user(self, user: User) -> bool or UserIsNotExist:
        with self._session_scope() as s:
            not_updated_user: User = s.query(User).filter(User.id == user.id).one_or_none()
            if not_updated_user is None:
                raise UserIsNotExist
            not_updated_user.username = user.username
            not_updated_user.email = user.email
            not_updated_user.items = user.items
            not_updated_user.pass_hash = user.pass_hash
            not_updated_user.photo_url = user.photo_url
            not_updated_user.wish_list = user.wish_list
        return True

    def add_wish_list_item(self, item: WishList) -> bool:
        with self._session_scope() as s:
            s.add(item)
        return True

    def get_wish_list_item(self, item_id: int) -> WishList or WishListItemIsNotExist:
        with self._session_scope() as s:
            check_item = s.query(WishList).filter(WishList.id == item_id).one_or_nonne()
            if check_item is None:
                raise WishListItemIsNotExist
        return check_item

    def update_wish_list_item(self, item: WishList) -> bool or WishListItemIsNotExist:
        with self._session_scope() as s:
            not_updated_item: WishList = s.query(WishList).filter(WishList.id == item.id).one_or_none()
            if not_updated_item is None:
                raise WishListItemIsNotExist
            not_updated_item.photo_url = item.photo_url
            not_updated_item.name = item.name
            not_updated_item.description = item.description
            not_updated_item.challenges = item.challenges
            not_updated_item.amount = item.amount
            not_updated_item.price = item.price
        return True

    def delete_wish_list_item(self, item: WishList) -> bool or WishListItemIsNotExist:
        with self._session_scope() as s:
            check_item = s.query(WishList).filter(WishList.id == item.id).one_or_none()
            if check_item is None:
                raise WishListItemIsNotExist
            s.query(WishList).filter(WishList.id == item.id).delete(synchronize_session=False)
        return True

    def get_user_wish_list(self, user_id: int) -> List[WishList]:
        with self._session_scope() as s:
            items = s.query(WishList).filter(WishList.user_fk == user_id).all()
        return items

    def get_user_challenge_wish_list(self, challenge_id: int, user_id: int) -> List[WishList]:
        with self._session_scope() as s:
            items = s.query(WishList).join(wish_list_to_challenge).filter(
                and_(WishList.user_fk == user_id, wish_list_to_challenge.c.challenge_fk == challenge_id))
            return items

    def add_item(self, item: Item) -> bool:
        with self._session_scope() as s:
            s.add(item)
        return True

    def get_item(self, item_id: int) -> Item or ItemIsNotExist:
        with self._session_scope() as s:
            check_item = s.query(Item).filter(Item.id == item_id).one_or_none()
            if check_item is None:
                raise ItemIsNotExist
        return check_item

    def update_item(self, item: Item) -> bool or ItemIsNotExist:
        with self._session_scope() as s:
            not_updated_item: Item = s.query(Item).filter(Item.id == item.id).one_or_none()
            if not_updated_item is None:
                raise ItemIsNotExist
            not_updated_item.price = item.price
            not_updated_item.amount = item.amount
            not_updated_item.description = item.description
            not_updated_item.name = item.name
            not_updated_item.date = item.date
            not_updated_item.sub_category_fk = item.sub_category_fk
        return True

    def delete_item(self, item: Item) -> bool or ItemIsNotExist:
        with self._session_scope() as s:
            check_item = s.query(Item).filter(Item.id == item.id).one_or_none()
            if check_item is None:
                raise ItemIsNotExist
            s.query(Item).filter(Item.id == item.id).delete(synchronize_session=False)
        return True

    def get_user_items(self, user_id: int) -> List[Item]:
        with self._session_scope() as s:
            items = s.query(Item).filter(Item.user_fk == user_id).all()
        return items

    def get_user_items_by_category(self, user_id: int, category_id: int) -> List[Item]:
        with self._session_scope() as s:
            items = s.query(Item).join(SubCategory).filter(
                and_(SubCategory.category_fk == category_id, Item.user_fk == user_id)).all()
        return items

    def get_user_items_by_subcategory(self, user_id: int, sub_category_id: int) -> List[Item]:
        with self._session_scope() as s:
            items = s.query(Item).filter(
                and_(Item.sub_category_fk == sub_category_id, Item.user_fk == user_id)).all()
        return items
