from dotenv import load_dotenv
import os

load_dotenv()

USER = os.getenv("USER")
PASSWORD = os.getenv("PASSWORD")
SERVER = os.getenv("SERVER")
DATABASE = os.getenv("DATABASE")
SERVER_GI = os.getenv("SERVER_GI")
DATABASE_GI = os.getenv("DATABASE_GI")