from sqlalchemy import create_engine
import pandas as pd


class DataHandler:
    """
    Base class to handle database interactions using SQLAlchemy.
    Provides methods to load and save data to SQLite database.
    """

    def __init__(self, db_name: str = "localDB.db") -> None:
        """
        Initialize the DataHandler with the database name.

        :param db_name: Name of the SQLite database file.
        """
        try:
            self.engine = create_engine(f"sqlite:///{db_name}")
        except Exception as e:
            raise ConnectionError(f"Failed to connect to the database: {e}")

    def load_data(self, table_name: str) -> pd.DataFrame:
        """
        Load data from the specified table in the database.

        :param table_name: Name of the table to load data from.
        :return: Data as a Pandas DataFrame.
        """
        try:
            return pd.read_sql(table_name, self.engine)
        except Exception as e:
            raise ValueError(f"Failed to load data from table '{table_name}': {e}")

    def save_data(self, df: pd.DataFrame, table_name: str) -> None:
        """
        Save a DataFrame to the specified table in the database.

        :param df: Pandas DataFrame to be saved.
        :param table_name: Name of the table to save data to.
        """
        try:
            df.to_sql(table_name, self.engine, if_exists="replace", index=False)
        except Exception as e:
            raise ValueError(f"Failed to save data to table '{table_name}': {e}")
