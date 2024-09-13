from bokeh.plotting import figure, show
from bokeh.layouts import gridplot
from bokeh.io import output_notebook
import pandas as pd

# Initialize notebook output for Bokeh
output_notebook()


def visualize_data(
    df_train: pd.DataFrame,
    df_ideal: pd.DataFrame,
    df_test: pd.DataFrame,
    selected_ideals: dict,
    mapped_data: pd.DataFrame,
) -> None:
    """
    Visualize the training data, ideal functions, test data, and deviations using Bokeh.

    :param df_train: Training data as a Pandas DataFrame.
    :param df_ideal: Ideal function data as a Pandas DataFrame.
    :param df_test: Test data as a Pandas DataFrame.
    :param selected_ideals: Dictionary of selected ideal functions for training data.
    :param mapped_data: Mapped test data with deviations.
    """

    # Create a Bokeh figure for training data and ideal functions
    p = figure(
        title="Training Data and Ideal Functions",
        x_axis_label="x",
        y_axis_label="y",
        width=800,
        height=600,
    )

    # Plot the training data (4 functions)
    colors = ["blue", "green", "orange", "purple"]
    for idx, col in enumerate(df_train.columns[1:]):  # Skip 'x' column
        p.line(
            df_train["x"],
            df_train[col],
            legend_label=f"Training {col}",
            color=colors[idx],
            line_width=2,
        )

    # Plot the selected ideal functions (best fit)
    for idx, (train_col, ideal_col) in enumerate(selected_ideals.items()):
        p.line(
            df_ideal["x"],
            df_ideal[ideal_col],
            legend_label=f"Ideal {ideal_col} for {train_col}",
            line_dash="dashed",
            color=colors[idx],
            line_width=2,
        )

    # Show the plot for training data and ideal functions
    show(p)

    # Create a separate figure for Test Data and Deviations
    p_test = figure(
        title="Test Data Mapping",
        x_axis_label="x",
        y_axis_label="y",
        width=800,
        height=600,
    )

    # Plot the test data points
    p_test.scatter(
        df_test["x"], df_test["y"], size=8, color="red", legend_label="Test Data"
    )

    # Plot the mapped ideal points and show deviations
    for _, row in mapped_data.iterrows():
        if row["mapped_ideal"] is not None:
            # Draw a line from test data to ideal function for each test point
            p_test.line(
                [row["x"], row["x"]],
                [row["y_test"], row["ideal_y"]],
                color="black",
                line_width=2,
                legend_label="Deviation",
            )
            p_test.scatter(
                row["x"],
                row["ideal_y"],
                size=8,
                color="green",
                legend_label=f"Ideal {row['mapped_ideal']}",
            )

    # Show the plot for test data and deviations
    show(p_test)

    # Optionally, combine the plots into a grid for better visualization
    grid = gridplot([[p, p_test]])
    show(grid)
