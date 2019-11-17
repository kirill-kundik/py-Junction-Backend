from contextlib import contextmanager
from typing import List

from sqlalchemy import and_, create_engine, func, or_
from sqlalchemy.orm import sessionmaker, subqueryload

import app
from app.utilities import Singleton
from .exceptions import *
from .models import *


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

    def add_user(self, user: User) -> bool or UserAlreadyExistsException:
        with self._session_scope() as s:
            check_user = s.query(User).filter(
                or_(User.username == user.username, User.email == user.email)).one_or_none()
            if check_user is not None:
                s.add(user)
            else:
                raise UserAlreadyExistsException
            return True

    def get_user_by_id(self, user_id: int) -> User or UserIsNotExistException:
        with self._session_scope() as s:
            user = s.query(User).filter(User.id == user_id).one_or_none()
            if user is None:
                raise UserIsNotExistException
        return user

    def get_user_by_username(self, username: str) -> User or UserIsNotExistException:
        with self._session_scope() as s:
            user = s.query(User).filter(User.username == username).one_or_none()
            if user is None:
                raise UserIsNotExistException
        return user

    def get_all_users(self) -> List[User]:
        with self._session_scope() as s:
            users = s.query(User).all()
        return users

    def update_user(self, user: User) -> bool or UserIsNotExistException:
        with self._session_scope() as s:
            not_updated_user: User = s.query(User).filter(User.id == user.id).one_or_none()
            if not_updated_user is None:
                raise UserIsNotExistException
            not_updated_user.username = user.username
            not_updated_user.email = user.email
            # not_updated_user.items = user.items
            not_updated_user.pass_hash = user.pass_hash
            not_updated_user.photo_url = user.photo_url
            not_updated_user.recommended_challenges = user.recommended_challenges
            # not_updated_user.wish_list = user.wish_list
            # not_updated_user.challenges = user.challenges
        return True

    def add_wish_list_item(self, item: WishList) -> WishList:
        with self._session_scope() as s:
            s.add(item)
        return item

    def get_wish_list_item(self, item_id: int) -> WishList or WishListItemIsNotExistException:
        with self._session_scope() as s:
            check_item = s.query(WishList).filter(WishList.id == item_id).one_or_none()
            if check_item is None:
                raise WishListItemIsNotExistException
        return check_item

    def update_wish_list_item(self, item: WishList) -> bool or WishListItemIsNotExistException:
        with self._session_scope() as s:
            not_updated_item: WishList = s.query(WishList).filter(WishList.id == item.id).one_or_none()
            if not_updated_item is None:
                raise WishListItemIsNotExistException
            not_updated_item.photo_url = item.photo_url
            not_updated_item.name = item.name
            not_updated_item.description = item.description
            not_updated_item.challenges = item.challenges
            not_updated_item.amount = item.amount
            not_updated_item.price = item.price
        return True

    def delete_wish_list_item(self, item: WishList) -> bool or WishListItemIsNotExistException:
        with self._session_scope() as s:
            check_item = s.query(WishList).filter(WishList.id == item.id).one_or_none()
            if check_item is None:
                raise WishListItemIsNotExistException
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

    def get_item(self, item_id: int) -> Item or ItemIsNotExistException:
        with self._session_scope() as s:
            check_item = s.query(Item).filter(Item.id == item_id).one_or_none()
            if check_item is None:
                raise ItemIsNotExistException
        return check_item

    def update_item(self, item: Item) -> bool or ItemIsNotExistException:
        with self._session_scope() as s:
            not_updated_item: Item = s.query(Item).filter(Item.id == item.id).one_or_none()
            if not_updated_item is None:
                raise ItemIsNotExistException
            not_updated_item.price = item.price
            not_updated_item.amount = item.amount
            not_updated_item.description = item.description
            not_updated_item.name = item.name
            not_updated_item.date = item.date
            not_updated_item.sub_category_fk = item.sub_category_fk
        return True

    def delete_item(self, item: Item) -> bool or ItemIsNotExistException:
        with self._session_scope() as s:
            check_item = s.query(Item).filter(Item.id == item.id).one_or_none()
            if check_item is None:
                raise ItemIsNotExistException
            s.query(Item).filter(Item.id == item.id).delete(synchronize_session=False)
        return True

    def get_user_items(self, user_id: int) -> List[Item]:
        with self._session_scope() as s:
            items = s.query(Item).join(SubCategory) \
                .options(subqueryload(Item.sub_category)) \
                .filter(Item.user_fk == user_id).all()
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

    def add_challenge(self, challenge: Challenge) -> bool:
        with self._session_scope() as s:
            s.add(challenge)
        return True

    def get_challenge_by_id(self, challenge_id: int) -> Challenge or ChallengeIsNotExistException:
        with self._session_scope() as s:
            check_challenge = s.query(Challenge) \
                .options(subqueryload(Challenge.sub_category)) \
                .filter(Challenge.id == challenge_id).one_or_none()
            if check_challenge is None:
                raise ChallengeIsNotExistException
        return check_challenge

    def update_challenge(self, challenge: Challenge) -> bool or ChallengeIsNotExistException:
        with self._session_scope() as s:
            not_updated_challenge: Challenge = s.query(Challenge).filter(Challenge.id == challenge.id).one_or_none()
            if not_updated_challenge is None:
                raise ChallengeIsNotExistException
            not_updated_challenge.sub_category_fk = challenge.sub_category_fk
            not_updated_challenge.name = challenge.name
            not_updated_challenge.photo_url = challenge.photo_url
            not_updated_challenge.difficulty = challenge.difficulty
            not_updated_challenge.brief_description = challenge.brief_description
            not_updated_challenge.earn_amount = challenge.earn_amount
            not_updated_challenge.full_description = challenge.full_description
        return True

    def get_challenges_by_wish_list_item(self, wish_list_item: int) -> List[Challenge]:
        with self._session_scope() as s:
            challenges = s.query(Challenge).join(wish_list_to_challenge).filter(
                wish_list_to_challenge.c.wish_list_fk == wish_list_item).all()
        return challenges

    def get_challenges_by_user(self, user_id: int) -> List[Challenge]:
        with self._session_scope() as s:
            challenges = s.query(Challenge).join(wish_list_to_challenge).join(User).join(SubCategory) \
                .options(subqueryload(Challenge.sub_category)) \
                .filter(User.id == user_id).all()
        return challenges

    def get_recommended_challenges_by_user(self, user_id: int) -> List[Challenge]:
        with self._session_scope() as s:
            challenges = s.query(Challenge).join(recommended_challenges).join(User).join(SubCategory) \
                .options(subqueryload(Challenge.sub_category)) \
                .filter(User.id == user_id).all()
        return challenges

    def get_challenges_by_user_and_category(self, user_id: int, category_id: int) -> List[Challenge]:
        with self._session_scope() as s:
            challenges = s.query(Challenge).join(wish_list_to_challenge).join(WishList).join(
                SubCategory).filter(and_(WishList.user_fk == user_id, SubCategory.category_fk == category_id))
        return challenges

    def get_challenges_by_user_and_subcategory(self, user_id: int, sub_category_id: int) -> List[Challenge]:
        with self._session_scope() as s:
            challenges = s.query(Challenge).join(wish_list_to_challenge).join(WishList).filter(
                and_(WishList.user_fk == user_id, Challenge.sub_category_fk == sub_category_id))
        return challenges

    def create_sub_category(self, sub_category: SubCategory) -> bool:
        with self._session_scope() as s:
            s.add(sub_category)
        return True

    def get_sub_category(self, sub_category_id: int) -> SubCategory or SubCategoryIsNotExistException:
        with self._session_scope() as s:
            check_subcategory = s.query(SubCategory).filter(SubCategory.id == sub_category_id).one_or_none()
            if check_subcategory is None:
                raise SubCategoryIsNotExistException
        return check_subcategory

    def update_sub_category(self, sub_category: SubCategory) -> bool or SubCategoryIsNotExistException:
        with self._session_scope() as s:
            not_updated_subcategory: SubCategory = s.query(SubCategory).filter(
                SubCategory.id == sub_category.id).one_or_none()
            if not_updated_subcategory is None:
                raise SubCategoryIsNotExistException
            not_updated_subcategory.category_fk = sub_category.category_fk
            not_updated_subcategory.name = sub_category.name
            not_updated_subcategory.description = sub_category.description
            not_updated_subcategory.color = sub_category.color
            not_updated_subcategory.period = sub_category.period

    def get_user_subcategory(self, user_id: int) -> List[SubCategory]:
        with self._session_scope() as s:
            subcategories = s.query(SubCategory).join(Item).filter(Item.user_fk == user_id).all()
        return subcategories

    def create_category(self, category: Category) -> bool:
        with self._session_scope() as s:
            s.add(category)
        return True

    def get_category(self, category_id: int) -> Category or CategoryIsNotExistException:
        with self._session_scope() as s:
            check_category = s.query(Category).filter(Category.id == category_id).one_or_none()
            if check_category is None:
                raise CategoryIsNotExistException
        return check_category

    def update_category(self, category: Category) -> bool or CategoryIsNotExistException:
        with self._session_scope() as s:
            not_updated_category: Category = s.query(Category).filter(
                Category.id == category.id).one_or_none()
            if not_updated_category is None:
                raise SubCategoryIsNotExistException
            not_updated_category.name = category.name
            not_updated_category.description = category.description
            not_updated_category.color = category.color

    def get_user_category(self, user_id: int) -> List[Category]:
        with self._session_scope() as s:
            categories = s.query(Category).join(SubCategory).join(Item).filter(Item.user_fk == user_id).all()
        return categories

    def unapply_user(self, user_id: int, challenge_id: int) -> bool or DatabaseException:
        with self._session_scope() as s:
            user = s.query(User).filter(User.id == user_id).one_or_none()
            if user is None:
                raise UserIsNotExistException
            challenge = s.query(Challenge).filter(Challenge.id == challenge_id).one_or_none()
            if challenge is None:
                raise ChallengeIsNotExistException
            user.challenges.remove(challenge)
        return True

    def apply_user(self, user_id: int, challenge_id: int, wishlist_item_id: int) -> bool or DatabaseException:
        with self._session_scope() as s:
            user = s.query(User).filter(User.id == user_id).one_or_none()
            if user is None:
                raise UserIsNotExistException
            challenge = s.query(Challenge).filter(Challenge.id == challenge_id).one_or_none()
            if challenge is None:
                raise ChallengeIsNotExistException
            user.challenges.append(challenge)
            if wishlist_item_id is not None:
                item = s.query(WishList).filter(
                    and_(WishList.id == wishlist_item_id, WishList.user_fk == user.id)).one_or_none()
                if item is None:
                    raise WishListItemIsNotExistException
        conn = self.engine.connect()
        stmt = wish_list_to_challenge.update().values(wish_list_fk=item.id) \
            .where(and_(wish_list_to_challenge.c.challenge_fk == challenge.id,
                        wish_list_to_challenge.c.user_fk == user.id))
        conn.execute(stmt)
        return True

    def get_wish_list_by_user_and_challenge(self, challenge_id: int, user_fk: int) -> List[WishList]:
        with self._session_scope() as s:
            items = s.query(WishList).join(wish_list_to_challenge).filter(
                and_(wish_list_to_challenge.c.user_fk == user_fk,
                     wish_list_to_challenge.c.challenge_fk == challenge_id)).all()
        return items

    def get_user_items_count(self, user_id: int) -> int:
        with self._session_scope() as s:
            count = s.query(Item).filter(Item.user_fk == user_id).count()
        return count

    def get_user_items_sum_by_period(self, user_id: int, period_first_day):
        with self._session_scope() as s:
            sum_costs = s.query(func.sum(Item.price * Item.amount)).filter(
                and_(Item.user_fk == user_id, Item.date >= period_first_day)).first()[0]
        return sum_costs

    def get_all_subcategories(self) -> List[SubCategory]:
        with self._session_scope() as s:
            subcategories = s.query(SubCategory).all()
        return subcategories

    def get_pie_chart_data(self, user_id: int):
        with self._session_scope() as s:
            result = s.query(func.sum(Item.price * Item.amount), Category.name) \
                .join(SubCategory, Item.sub_category_fk == SubCategory.id) \
                .join(Category, SubCategory.category_fk == Category.id).group_by(
                Category.name).filter(Item.user_fk == user_id).all()
        return result

    def add_user_recommended_challenge(self, user_fk: int, challenge_fk: int):
        conn = self.engine.connect()
        stmt = recommended_challenges.insert().values(user_fk=user_fk, challenge_fk=challenge_fk)
        conn.execute(stmt)

    def generate_challenge_progress(self, user_id: int, challenge_id: int):
        with self._session_scope() as s:
            total_amount, created_at, sub_category_id = s.query(Challenge.earn_amount,
                                                                wish_list_to_challenge.c.created_at,
                                                                Challenge.sub_category_fk) \
                .join(wish_list_to_challenge) \
                .filter(and_(wish_list_to_challenge.c.user_fk == user_id,
                             wish_list_to_challenge.c.challenge_fk == challenge_id)).first()
            sum_costs = s.query(func.sum(Item.price * Item.amount)) \
                .filter(and_(and_(Item.user_fk == user_id, Item.date >= created_at)),
                        Item.sub_category_fk == sub_category_id).one_or_none()[0]
            if sum_costs is None:
                sum_costs = 0
            dt = datetime.datetime.utcnow() - created_at
            sub_category_period = s.query(SubCategory.period).filter(SubCategory.id == sub_category_id).first()[0]
            if sub_category_period == PeriodType.daily:
                sub_category_period = 86400
            elif sub_category_period == PeriodType.weekly:
                sub_category_period = 7 * 86400
            elif sub_category_period == PeriodType.monthly:
                sub_category_period = 30 * 86400
            elif sub_category_period == PeriodType.half_yearly:
                sub_category_period = 182 * 86400
            elif sub_category_period == PeriodType.yearly:
                sub_category_period = 365 * 86400
        return {
            "created_at": created_at,
            "challenge_price_progress": sum_costs / total_amount,
            "challenge_time_progress": dt.seconds / sub_category_period,
        }
