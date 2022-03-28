import os
import psycopg2

from dotenv import load_dotenv

load_dotenv() 

def connectionDB():
    try:
        return psycopg2.connect(host     = os.getenv("POSTGRES_URL"),
                                database = os.getenv("POSTGRES_DB"),
                                user     = os.getenv("POSTGRES_USER"),
                                password = os.getenv("POSTGRES_PW"),
                                port     = os.getenv("POSTGRES_PORT")
        )
    except:                     
        print("can't connect to database ")

