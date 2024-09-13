from task_modules.database_manager import DatabaseManager
from task_modules.least_squares_selector import LeastSquaresSelector
from task_modules.test_data_mapper import TestDataMapper
import unittest
import os
import pandas as pd


class TestDatabaseManager(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.db_manager = DatabaseManager(db_name="test_localDB.db")
        cls.df_train = pd.DataFrame({
            "x": [1, 2, 3],
            "y1": [10, 20, 30],
            "y2": [15, 25, 35],
        })

    def test_create_and_load_table(self):
        # Test if a table can be created and data loaded
        self.db_manager.create_table("train_data", self.df_train)
        result_df = self.db_manager.load_data("train_data")
        pd.testing.assert_frame_equal(result_df, self.df_train)

    def test_create_table_with_empty_df(self):
        # Test if an exception is raised when trying to create a table with an empty DataFrame
        with self.assertRaises(ValueError):
            self.db_manager.create_table("empty_table", pd.DataFrame())

    @classmethod
    def tearDownClass(cls):
        # Clean up the test database file
        os.remove("test_localDB.db")


class TestLeastSquaresSelector(unittest.TestCase):
    def setUp(self):
        # Sample training and ideal function data
        self.df_train = pd.DataFrame({
            "x": [1, 2, 3],
            "y1": [10, 20, 30],
            "y2": [15, 25, 35],
        })
        self.df_ideal = pd.DataFrame({
            "x": [1, 2, 3],
            "y1": [9, 21, 31],
            "y2": [14, 26, 34],
            "y3": [10, 20, 30],  # Perfect match for y1
        })
        self.selector = LeastSquaresSelector(
            self.df_train, self.df_ideal, db_name="test_localDB.db"
        )

    def test_least_squares_mismatched_lengths(self):
        # Test least squares calculation with mismatched lengths
        with self.assertRaises(ValueError):
            self.selector.least_squares(self.df_train["y1"], self.df_ideal["y1"][:2])

    def test_select_best_fit(self):
        # Test selecting the best fit ideal function
        selected_ideals = self.selector.select_best_fit()
        self.assertEqual(
            selected_ideals["y1"], "y3"
        )  # y3 should be the best fit for y1


class TestTestDataMapper(unittest.TestCase):
    def setUp(self):
        # Sample test data, ideal functions, and selected fits
        self.df_test = pd.DataFrame({"x": [1, 2], "y": [10, 22]})
        self.df_ideal = pd.DataFrame({"x": [1, 2], "y1": [9, 21], "y2": [11, 23]})
        self.selected_ideals = {"y1": "y1", "y2": "y2"}
        self.max_devs = {"y1": 1, "y2": 1}
        self.mapper = TestDataMapper(
            self.df_test,
            self.df_ideal,
            self.selected_ideals,
            self.max_devs,
            db_name="test_localDB.db",
        )

    def test_map_test_data(self):
        # Test mapping of test data within deviation threshold
        mapped_data = self.mapper.map_test_data()
        expected_mapped = pd.DataFrame({
            "x": [1, 2],
            "y_test": [10, 22],
            "mapped_ideal": ["y1", "y1"],
            "ideal_y": [9, 21],
            "deviation": [1, 1],
        })
        pd.testing.assert_frame_equal(mapped_data, expected_mapped)


if __name__ == "__main__":
    unittest.main(argv=[""], exit=False)
