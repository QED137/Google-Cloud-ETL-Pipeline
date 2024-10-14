# db/database.py
import configparser
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.engine.base import Engine


def load_config():
    config = configparser.ConfigParser()
    config.read('config/config.ini')
    return config


def connect_database(config) -> Engine:
    config = load_config()

    # Access credentials
    db_user = config['Database']['user']
    db_password = config['Database']['password']
    db_host = config['Database']['host']
    db_name = config['Database']['database']

    # Connection string
    connect_string = f'mysql+pymysql://{db_user}:{db_password}@{db_host}/{db_name}'

    try:
        engine = create_engine(connect_string)
        print("Database connection successful.")
    except SQLAlchemyError as e:
        raise ValueError(f"Database connection failed: {e}")

    return engine

def connectiontwo()-> Engine:
    
    config = load_config()
    
    db_user = config['DatabaseCloud']['user'] #database cloude has passowrd for cloud mysqlworkbench
    
    db_password = config['DatabaseCloud']['password']
    
    db_host = config['DatabaseCloud']['host']
    
    db_name = config['DatabaseCloud']['database']
    
        # Connection string
    connect_string = f'mysql+pymysql://{db_user}:{db_password}@{db_host}/{db_name}'

    try:
        engine = create_engine(connect_string)
        print("Database connection successful.")
    except SQLAlchemyError as e:
        raise ValueError(f"Database connection failed: {e}")

    return engine
    
