import psycopg2

DATABASE = "postgresql://neondb_owner:npg_sBJ4ToUmg0ke@ep-damp-butterfly-abybjm2l-pooler.eu-west-2.aws.neon.tech/neondb?sslmode=require&channel_binding=require"

def connect():
    conn = psycopg2.connect(DATABASE)
    return conn