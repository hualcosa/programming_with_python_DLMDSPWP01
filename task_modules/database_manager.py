from task_modules.data_handler import DataHandler
import pandas as pd


class DatabaseManager(DataHandler):
    """
    Manages database operations for loading and saving data.
    Inherits from DataHandler to perform database-related tasks.
    """

    def __init__(self, db_name: str = "localDB.db") -> None:
        """
        Initialize the DatabaseManager with the database name.
        """
        super().__init__(db_name)

    def create_table(self, table_name: str, df: pd.DataFrame) -> None:
        """
        Create a table in the database by saving the provided DataFrame.

        :param table_name: Name of the table to create.
        :param df: Pandas DataFrame to save as a table.
        """
        if df.empty:
            raise ValueError(f"DataFrame is empty. Cannot create table '{table_name}'.")
        self.save_data(df, table_name)
