# config.py
'''
import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'Hemanth1234')
    
    # MySQL Database URI (for mysqlclient)
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://hemanth:Hem%402000@localhost/Hem_database'



    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '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')

'''
import os
from datetime import timedelta



class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'Hemanth1234')
    SQLALCHEMY_DATABASE_URI = 'SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://sql5777226:n6zpuWa3Jw@sql5.freesqldatabase.com:3306/sql5777226'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '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')
    PERMANENT_SESSION_LIFETIME = timedelta(minutes=30)

