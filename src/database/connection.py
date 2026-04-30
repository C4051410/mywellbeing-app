import ssl
from urllib.parse import urlparse

import pg8000
import os
from dotenv import load_dotenv

load_dotenv()
DATABASE = os.getenv("DATABASE_URL")
TEST_DATABASE = os.getenv("TEST_DATABASE_URL")
EMAIL_KEY = os.getenv("EMAIL_KEY")
#return connection to database
def connect():
    url = urlparse(DATABASE)
    #checks to determine if the destination is a local postgresSQL
    is_local = url.hostname in ("localhost", "127.0.0.1")

    ssl_code = None
    if not is_local:
        ssl_code = ssl.create_default_context()
    #returns connection, using urlparse to split the connection string correctly
    return pg8000.connect(
        user=url.username,
        password=url.password,
        host=url.hostname,
        port=url.port or 5432,
        database=url.path[1:],
        ssl_context=ssl_code,
        timeout=20
    )
#return email key
def email_key():
    return EMAIL_KEY