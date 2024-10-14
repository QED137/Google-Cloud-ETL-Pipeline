import pandas as pd
from sqlalchemy.exc import SQLAlchemyError

def retrieve_from_db(table: str, engine) -> pd.DataFrame:
    """
    Retrieve data from the database.
    
    Args:
        table (str): The name of the table to retrieve data from.
        engine (Engine): The SQLAlchemy engine to use for the database connection.
    
    Returns:
        pd.DataFrame: The data retrieved from the database.
    """
    try:
        with engine.begin() as conn:
            df = pd.read_sql(f"SELECT * FROM {table}", con=conn)
        return df
    except SQLAlchemyError as e:
        print(f"Error while retrieving data from {table}: {e}")
        return pd.DataFrame()
