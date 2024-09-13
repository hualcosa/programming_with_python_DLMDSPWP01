import numpy as np
import pandas as pd
from task_modules.data_handler import DataHandler


class LeastSquaresSelector(DataHandler):
    """
    Selects the ideal functions that best fit the training data using the least-squares method.
    Inherits from DataHandler for database interaction.
    """

    def __init__(
        self,
        df_train: pd.DataFrame,
        df_ideal: pd.DataFrame,
        db_name: str = "localDB.db",
    ) -> None:
        """
        Initialize the selector with training and ideal function data.

        :param df_train: Training data as a Pandas DataFrame.
        :param df_ideal: Ideal functions data as a Pandas DataFrame.
        :param db_name: Name of the SQLite database file.
        """
        super().__init__(db_name)
        if df_train.empty or df_ideal.empty:
            raise ValueError("Training or Ideal DataFrame cannot be empty.")
        self.df_train = df_train
        self.df_ideal = df_ideal

    def least_squares(self, y_train: pd.Series, y_ideal: pd.Series) -> float:
        """
        Calculate the sum of squared errors between a training function and an ideal function.

        :param y_train: Training function values as a Pandas Series.
        :param y_ideal: Ideal function values as a Pandas Series.
        :return: Sum of squared errors.
        """
        if len(y_train) != len(y_ideal):
            raise ValueError(
                f"Mismatched lengths: y_train ({len(y_train)}) and y_ideal ({len(y_ideal)})"
            )
        return np.sum((y_train - y_ideal) ** 2)

    def select_best_fit(self) -> dict:
        """
        Select the best ideal function for each training function by minimizing the sum of squared deviations.

        :return: Dictionary with training function names as keys and best-fit ideal function names as values.
        """
        selected_ideals = {}
        for train_col in self.df_train.columns[1:]:  # Skip 'x' column
            min_sse = float("inf")
            best_ideal = None
            for ideal_col in self.df_ideal.columns[1:]:
                try:
                    sse = self.least_squares(
                        self.df_train[train_col], self.df_ideal[ideal_col]
                    )
                    if sse < min_sse:
                        min_sse = sse
                        best_ideal = ideal_col
                except ValueError as e:
                    print(
                        f"Skipping comparison between {train_col} and {ideal_col}: {e}"
                    )
            if best_ideal is None:
                raise ValueError(f"No valid ideal function found for {train_col}.")
            selected_ideals[train_col] = best_ideal
        return selected_ideals
