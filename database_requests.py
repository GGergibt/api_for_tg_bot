from dotenv import dotenv_values
import dotenv
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

config = dict(dotenv.dotenv_values(".env"))
password = next(iter(config.values()))
connection_to_database = psycopg2.connect(
    host="localhost", database="personal_chat_history", user="gosha", password=password
)
connection_to_database.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
cursor = connection_to_database.cursor()






