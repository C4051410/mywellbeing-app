import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()
DATABASE = os.getenv("DATABASE_URL")
EMAIL_KEY = os.getenv("EMAIL_KEY")
#return connection to database
def connect():
    conn = psycopg2.connect(DATABASE)
    return conn
#return email key
def email_key():
    return EMAIL_KEY