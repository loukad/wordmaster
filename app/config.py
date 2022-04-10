import os

SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI', 'sqlite:///words.db')
SQLALCHEMY_TRACK_MODIFICATIONS = False

DB_POOL_SIZE = int(os.getenv('DB_POOL_SIZE', '10'))
DB_POOL_RECYCLE = int(os.getenv('DB_POOL_RECYCLE', '60'))
SQLALCHEMY_ENGINE_OPTIONS = {
    'pool_size': DB_POOL_SIZE,
    'pool_recycle': DB_POOL_RECYCLE,
}
