import os
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = str(os.getenv('BOT_TOKEN'))
PGUSER = str(os.getenv('PGUSER'))
PGPASSWORD = str(os.getenv('PGPASSWORD'))
DATABASE = str(os.getenv('DATABASE'))
ADMIN_ID = [
    str(os.getenv('ADMIN_ID'))
    ]
DBHOST = str(os.getenv('DBHOST'))
POSTGRES_URI = f"postgres://{PGUSER}:{PGPASSWORD}@{DBHOST}/{DATABASE}"
