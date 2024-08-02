from database import DEmployment, DProject, DUsers
from sqlalchemy import create_engine

engi = create_engine(
    "mysql+pymysql://db_user:db_password@localhost/orm_test"
)


def create_table():
    DEmployment.metadata.create_all(engi)
    DProject.metadata.create_all(engi)
    DUsers.metadata.create_all(engi)


create_table()
