import argparse
import pandas as pd
import numpy as np
from database_manager import DatabaseManager
from least_squares_selector import LeastSquaresSelector
from test_data_mapper import TestDataMapper
from visualizer import visualize_data


def main():
    """
    Command-line interface (CLI) for loading data, performing least-squares selection, mapping test data,
    and visualizing the results. Results are saved to an SQLite database.
    """

    # Set up argument parsing
    parser = argparse.ArgumentParser(
        description="CLI for data analysis: Training, Ideal Function Matching, and Test Data Mapping."
    )

    # Arguments for file paths
    parser.add_argument(
        "--train",
        type=str,
        required=True,
        help="Path to the CSV file containing the training data.",
    )
    parser.add_argument(
        "--ideal",
        type=str,
        required=True,
        help="Path to the CSV file containing the ideal functions data.",
    )
    parser.add_argument(
        "--test",
        type=str,
        required=True,
        help="Path to the CSV file containing the test data.",
    )
    parser.add_argument(
        "--db",
        type=str,
        default="localDB.db",
        help="Name of the SQLite database file (default: localDB.db).",
    )

    # Argument for enabling visualization
    parser.add_argument(
        "--visualize",
        action="store_true",
        help="If set, will generate visualizations for training, ideal, and test data.",
    )

    # Parse the arguments
    args = parser.parse_args()

    # Load the data from the provided file paths
    df_train = pd.read_csv(args.train)
    df_ideal = pd.read_csv(args.ideal)
    df_test = pd.read_csv(args.test)

    # Step 1: Initialize DatabaseManager and save data to the database
    db_manager = DatabaseManager(db_name=args.db)
    db_manager.create_table("train_data", df_train)
    db_manager.create_table("ideal_functions", df_ideal)

    # Step 2: Perform Least-Squares Selection
    selector = LeastSquaresSelector(df_train, df_ideal)
    selected_ideals = selector.select_best_fit()

    # Compute max deviations between training data and selected ideal functions
    max_devs = {
        train_col: np.max(
            np.abs(df_train[train_col] - df_ideal[selected_ideals[train_col]])
        )
        for train_col in df_train.columns[1:]
    }

    # Step 3: Map test data to the ideal functions
    mapper = TestDataMapper(df_test, df_ideal, selected_ideals, max_devs)
    mapped_data = mapper.map_test_data()

    # Save the mapped test data to the database
    db_manager.create_table("test_results", mapped_data)

    # Step 4: Optionally visualize the data
    if args.visualize:
        visualize_data(df_train, df_ideal, df_test, selected_ideals, mapped_data)


if __name__ == "__main__":
    main()
