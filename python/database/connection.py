import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()
DATABASE = os.getenv("DATABASE_URL")

def connect():
    conn = psycopg2.connect(DATABASE)
    return conn