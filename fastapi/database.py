from datetime import date
from sqlalchemy import Column, Date, ForeignKey, Integer, String, create_engine, delete
import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

DATABASE_URL = "mysql+mysqlconnector://todolist:a153ru161@localhost:3306/todolist"

engine = create_engine(DATABASE_URL)

Base = declarative_base()
Session = sessionmaker(bind=engine)

session = Session()

class Task(Base):
    __tablename__ = 'todolist_app_task'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    description = Column(String)
    owner = Column(String)
    priority = Column(String)
    date_create = Column(String, default=date.today())
    date_of_staging = Column(String)
    executor_id = Column(Integer, ForeignKey('auth_user.id'))
    executor = relationship("User", primaryjoin="Task.executor_id == User.id", back_populates='todolist_app_task')

class License(Base):
    __tablename__ = 'todolist_app_license'
    id = Column(Integer, primary_key=True, autoincrement=True)
    token = Column(String)
    login_id = Column(Integer, ForeignKey('auth_user.id'))
    login = relationship("User")
    telegram_id = Column(Integer)
    war_token = Column(String)

class User(Base):
    __tablename__ = 'auth_user'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String)
    is_staff = Column(Integer)

    todolist_app_task = relationship("Task", back_populates="executor")



