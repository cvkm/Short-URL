import os 

SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:password@localhost/database'   #os.environ.get('DATABASE_URL')
SQLALCHEMY_TRACK_MODIFICATIONS = False

ADMIN_USERNAME = os.environ.get('ADMIN_USERNAME')
ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD')
