import os

from sqlalchemy import create_engine, insert, select
from sqlalchemy.orm import declarative_base, sessionmaker, subqueryload

from .filter_models import Make, Model, Region
from .managers import DatabaseAbstract
from .utils.decorators import close_session_after_execution


class RegionManager(DatabaseAbstract):
    def __init__(self):
        super().__init__()

    @close_session_after_execution
    def insert_region(self, name: str):
        self.session.execute(insert(Region).values(name=name))
        self.session.commit()

    @close_session_after_execution
    def get_or_create(self, name: str):
        region = self.get_region(name)
        if not region:
            self.insert_region(name)
        return region

    @close_session_after_execution
    def get_region(self, name: str):
        return self.session.query(Region).filter(Region.name == name).first()

    @close_session_after_execution
    def get_all_regions(self):
        return self.session.query(Region.id, Region.name).order_by(Region.id).all()


class MakeManager(DatabaseAbstract):
    def __init__(self):
        super().__init__()

    @close_session_after_execution
    def insert_make(self, name: str):
        self.session.execute(insert(Make).values(name=name))
        self.session.commit()

    @close_session_after_execution
    def get_or_create(self, name: str):
        make = self.get_make(name)
        if not make:
            print(f"Inserting make: {name}")
            self.insert_make(name)
        return make

    @close_session_after_execution
    def get_make(self, name: str):
        return self.session.query(Make).filter(Make.name == name).first()

    @close_session_after_execution
    def get_all_makes(self):
        return self.session.query(Make.id, Make.name).order_by(Make.name).all()

    @close_session_after_execution
    def check_make_exists(self, name: str):
        return self.session.query(Make).filter(Make.name == name).first()


class ModelManager(DatabaseAbstract):
    def __init__(self):
        super().__init__()

    @close_session_after_execution
    def insert_model(self, make_id: int, make_name: str, name: str):
        self.session.execute(
            insert(Model).values(make_id=make_id, make_name=make_name, name=name)
        )
        self.session.commit()

    @close_session_after_execution
    def get_or_create(self, make_id: int, make_name: str, name: str):
        model = self.get_model(name)
        if not model:
            self.insert_model(make_id, make_name, name)
        return model

    @close_session_after_execution
    def get_model(self, name: str):
        return self.session.query(Model).filter(Model.name == name).first()

    @close_session_after_execution
    def get_all_models_by_make_id(self, make_id: int):
        return (
            self.session.query(Model.id, Model.name)
            .filter(Model.make_id == make_id)
            .all()
        )

    @close_session_after_execution
    def get_all_models(self):
        return self.session.query(Model.id, Model.name).order_by(Model.name).all()
