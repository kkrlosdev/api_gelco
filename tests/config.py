from dotenv import load_dotenv
import os

load_dotenv()

SERVER_SIESA = os.getenv("SERVER")
SERVER_GI = os.getenv("SERVER_GI")