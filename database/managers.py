import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import declarative_base, joinedload, sessionmaker, subqueryload

from .models import Filter, Product, User
from .utils.decorators import close_session_after_execution

load_dotenv()


class DatabaseAbstract:
    def __init__(self):
        self.engine = create_engine(
            os.environ.get("DATABASE_URL", "sqlite:///turbot_db.db"),
        )
        Session = sessionmaker(bind=self.engine)
        self.session = Session()


class UserManager(DatabaseAbstract):
    def __init__(self):
        super().__init__()

    @close_session_after_execution
    def insert_user(self, tg_id: int, **kwargs):
        self.session.execute(insert(User).values(tg_id=tg_id, **kwargs))
        self.session.commit()

    @close_session_after_execution
    def update_user(self, tg_id: int, **kwargs):
        user = self.get_user(tg_id)
        if user:
            self.session.query(User).filter(User.tg_id == tg_id).update(kwargs)
            self.session.commit()

    @close_session_after_execution
    def get_or_create(self, tg_id: int, **kwargs):
        user = self.get_user(tg_id)
        if not user:
            self.insert_user(tg_id, **kwargs)
        return user

    @close_session_after_execution
    def get_user(self, tg_id: int):
        return (
            self.session.query(User)
            .options(joinedload(User.filter))
            .filter(User.tg_id == tg_id)
            .first()
        )

    @close_session_after_execution
    def get_user_filter(self, tg_id: int):
        return (
            self.session.query(User)
            .options(joinedload(User.filter))
            .filter(User.tg_id == tg_id)
            .first()
            .filter
        )

    @close_session_after_execution
    def get_all_users(self):
        return self.session.query(User).options(joinedload(User.filter)).all()

    @close_session_after_execution
    def get_all_active_users(self):
        return (
            self.session.query(User)
            .options(joinedload(User.filter))
            .filter(User.is_active == True)
            .all()
        )

    @close_session_after_execution
    def check_user_is_active(self, tg_id: int):
        result = self.session.query(User.is_active).filter(User.tg_id == tg_id).first()
        return result[0] if result else False

    @close_session_after_execution
    def check_user_notification(self, tg_id: int):
        result = (
            self.session.query(User.notification).filter(User.tg_id == tg_id).first()
        )
        return result[0] if result else False


class FilterManager(DatabaseAbstract):
    def __init__(self):
        super().__init__()

    @close_session_after_execution
    def insert_filter(self, tg_id: int, **kwargs):
        self.session.execute(
            insert(Filter).values(
                user_tg_id=tg_id,
                **kwargs,
            )
        )
        self.session.commit()

    @close_session_after_execution
    def update_filter(self, tg_id: str, **kwargs):
        filter = self.get_filter(tg_id)
        if not filter:
            self.insert_filter(tg_id, **kwargs)

        else:
            self.session.query(Filter).filter(Filter.user_tg_id == tg_id).update(kwargs)
            self.session.commit()

    @close_session_after_execution
    def get_filter(self, tg_id: int):
        return (
            self.session.query(Filter)
            .options(subqueryload(Filter.user))
            .filter(Filter.user_tg_id == tg_id)
            .first()
        )

    @close_session_after_execution
    def get_all_filters(self):
        return self.session.query(Filter).all()

    @close_session_after_execution
    def get_or_create(self, tg_id: int, **kwargs):
        filter = self.get_filter(tg_id)
        if not filter:
            self.insert_filter(tg_id, **kwargs)
        return filter


class ProductManager(DatabaseAbstract):
    def __init__(self):
        super().__init__()

    @close_session_after_execution
    def insert_product(self, **kwargs):
        stmt = (
            insert(Product)
            .values(**kwargs)
            .on_conflict_do_nothing(index_elements=["product_id"])
        )
        self.session.execute(stmt)
        self.session.commit()

    @close_session_after_execution
    def product_exists(self, product_id):
        return (
            self.session.query(Product.id)
            .filter(Product.product_id == product_id)
            .first()
            is not None
        )

    @close_session_after_execution
    def get_product(self, product_id: int):
        return (
            self.session.query(Product).filter(Product.product_id == product_id).first()
        )

    @close_session_after_execution
    def get_all_products(self):
        return self.session.query(Product.id).all()

    @close_session_after_execution
    def update_product(self, product_id: int, **kwargs):
        product = self.get_product(product_id)
        if product:
            for key, value in kwargs.items():
                setattr(product, key, value)
            self.session.commit()
