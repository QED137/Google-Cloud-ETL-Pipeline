import pandas as pd
from sqlalchemy.exc import SQLAlchemyError

def push_to_database(df: pd.DataFrame, table: str, engine):
    """
    Push DataFrame to the database table.
    
    Args:
        df (DataFrame): The DataFrame to push to the database.
        table (str): The table name in the database.
        engine (Engine): The SQLAlchemy engine to use for the database connection.
    
    Returns:
        None
    """
    try:
        with engine.begin() as conn:
            df.to_sql(table, con=conn, if_exists='append', index=False)
        print(f"Data successfully pushed to {table} table.")
    except SQLAlchemyError as e:
        print(f"Error while pushing data to the database: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")    
