# from sqlalchemy import create_engine
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import sessionmaker
# import os

# engine = create_engine(
#     os.environ.get("SQLALCHEMY_DATABASE_URL"),
#     connect_args={"check_same_thread": False},
# )

# Base = declarative_base()


# def get_db():
#     engine = create_engine(
#         os.environ.get("SQLALCHEMY_DATABASE_URL"),
#         connect_args={"check_same_thread": False},
#     )

#     Base = declarative_base()

#     Base.metadata.create_all(bind=engine)

#     db_url = os.environ.get("SQLALCHEMY_DATABASE_URL")
#     engine = create_engine(db_url, connect_args={"check_same_thread": False})
#     SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()


import psycopg2
from psycopg2 import OperationalError


def create_connection(db_name, db_user, db_password, db_host, db_port):
    connection = None
    try:
        connection = psycopg2.connect(
            database=db_name,
            user=db_user,
            password=db_password,
            host=db_host,
            port=db_port,
        )
        print("Connection to PostgreSQL DB successful")
    except OperationalError as e:
        print(f"The error '{e}' occurred")
    return connection


def create_database(connection, query):
    connection.autocommit = True
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        print("Query executed successfully")
    except OperationalError as e:
        print(f"The error '{e}' occurred")


def execute_query(connection, query):
    connection.autocommit = True
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        print("Query executed successfully")
    except OperationalError as e:
        print(f"The error '{e}' occured")


create_users_table = """
CREATE TABLE IF NOT EXISTS users (
  id SERIAL PRIMARY KEY,
  email TEXT UNIQUE NOT NULL, 
  hashed_password TEXT NOT NULL,
  gender TEXT,
  nationality TEXT
)
"""


# execute_query(connection, create_users_table)

# create_database_query = "CREATE DATABASE fastapi_auth"
# create_database(connection, create_database_query)
