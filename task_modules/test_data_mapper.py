from task_modules.data_handler import DataHandler
import pandas as pd
import numpy as np


# Custom exception for invalid test data mappings
class InvalidMappingError(Exception):
    """
    Custom exception for cases where test data cannot be mapped to an ideal function.
    """

    pass


class TestDataMapper(DataHandler):
    """
    Maps test data to ideal functions based on deviations.
    Inherits from DataHandler for database interaction.
    """

    def __init__(
        self,
        df_test: pd.DataFrame,
        df_ideal: pd.DataFrame,
        selected_ideals: dict,
        max_devs: dict,
        db_name: str = "localDB.db",
    ) -> None:
        """
        Initialize the mapper with test data, ideal functions, and selected mappings.

        :param df_test: Test data as a Pandas DataFrame.
        :param df_ideal: Ideal function data as a Pandas DataFrame.
        :param selected_ideals: Mapping of training functions to ideal functions.
        :param max_devs: Maximum deviations for each training function.
        :param db_name: Name of the SQLite database file.
        """
        super().__init__(db_name)
        if df_test.empty or df_ideal.empty:
            raise ValueError("Test or Ideal DataFrame cannot be empty.")
        self.df_test = df_test
        self.df_ideal = df_ideal
        self.selected_ideals = selected_ideals
        self.max_devs = max_devs

    def map_test_data(self) -> pd.DataFrame:
        """
        Map test data to ideal functions and ensure the deviations are within the allowed threshold.

        :return: DataFrame containing the mapped test data with deviations.
        """
        mapped_data = []
        for _, test_point in self.df_test.iterrows():
            x, y_test = test_point["x"], test_point["y"]
            mapped = False
            for train_col, ideal_col in self.selected_ideals.items():
                try:
                    ideal_y = self.df_ideal[self.df_ideal["x"] == x][ideal_col].values[
                        0
                    ]
                    if abs(y_test - ideal_y) <= self.max_devs[train_col] * np.sqrt(2):
                        mapped_data.append((
                            x,
                            y_test,
                            ideal_col,
                            ideal_y,
                            y_test - ideal_y,
                        ))
                        mapped = True
                        break
                except IndexError:
                    raise InvalidMappingError(
                        f"No ideal function value found for x = {x}"
                    )
            if not mapped:
                mapped_data.append((x, y_test, None, None, None))
        return pd.DataFrame(
            mapped_data, columns=["x", "y_test", "mapped_ideal", "ideal_y", "deviation"]
        )
