import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()
DATABASE = os.getenv("DATABASE_URL")
TEST_DATABASE = os.getenv("TEST_DATABASE_URL")
EMAIL_KEY = os.getenv("EMAIL_KEY")
#return connection to database
def connect():
    conn = psycopg2.connect(TEST_DATABASE)
    return conn
#return email key
def email_key():
    return EMAIL_KEY