import psycopg2
from psycopg2.extras import RealDictCursor
import time
from .config import settings

while True:
    try:
        conn = psycopg2.connect(host = settings.database_hostname, database = settings.database_name, user = settings.database_username,
        password = settings.database_password, cursor_factory=RealDictCursor)
        cur = conn.cursor()
        print("Connection Established")
        break
    except Exception as err:
        print("Connection Failed")
        print("Error:",err)
        time.sleep(2)