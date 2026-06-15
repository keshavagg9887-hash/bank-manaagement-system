from dotenv import load_dotenv
import os
import psycopg2 as connector
load_dotenv()
def connection():
    return connector.connect(
     database=os.getenv('db'),
     user=os.getenv('user'),
     password=os.getenv('pass'),
     host=os.getenv('host'),
     port=os.getenv('port'),
    )