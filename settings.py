import os

from dotenv import load_dotenv


load_dotenv()

POSTGRES_USER = os.getenv('POSTGRES_USER', default='postgres')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD', default='postgres')
DB_HOST = os.getenv('DB_HOST', default='postgres')
DB_NAME = os.getenv('DB_NAME', default='postgres')
DB_PORT = os.getenv('DB_PORT', default='5432')
ID_SHEETS = os.getenv(
    'ID_SHEETS',
    default='1CWLWekIwMsUSdLOPX4ayuASNSp5UUD8hO0vl-HEm4gY'
)
TELEGRAM_TOKEN = os.getenv(
    'TELEGRAM_TOKEN',
    default='5876058521:AAH5IKDRWQmc1r-XrCcL99ZtSrbqeuiFPog'
)
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

DB_PATH = (
    'postgresql+psycopg2://' 
    f'{POSTGRES_USER}:{POSTGRES_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
)

PERIOD = 60
