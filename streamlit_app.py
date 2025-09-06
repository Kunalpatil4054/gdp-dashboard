# Install required libraries (run once)
!pip install plotly

# Imports
import numpy as np
import pandas as pd
import plotly.express as px
import ipywidgets as widgets
from IPython.display import display

# Generate sample dataset
np.random.seed(42)
df = pd.DataFrame({
    "Category": np.random.choice(["A", "B", "C"], size=100),
    "Value1": np.random.randint(10, 100, size=100),
    "Value2": np.random.randint(50, 200, size=100)
})

# Dropdown for category filter
category_dropdown = widgets.Dropdown(
    options=["All"] + sorted(df["Category"].unique().tolist()),
    value="All",
    description="Category:"
)

# Slider for minimum Value1 filter
value_slider = widgets.IntSlider(
    value=20,
    min=10,
    max=100,
    step=5,
    description="Min Value1:",
    continuous_update=False
)

# Function to update dashboard
def update_dashboard(category, min_value):
    # Filter data
    if category != "All":
        filtered = df[df["Category"] == category]
    else:
        filtered = df.copy()
    
    filtered = filtered[filtered["Value1"] >= min_value]

    # Display filtered table
    display(filtered.head(10))  # show top 10 rows

    # Plot chart
    fig = px.scatter(
        filtered, 
        x="Value1", y="Value2", 
        color="Category",
        title=f"Scatter Plot (Category={category}, Min Value1={min_value})",
        height=500
    )
    fig.show()

# Create interactive dashboard
widgets.interact(
    update_dashboard, 
    category=category_dropdown, 
    min_value=value_slider
)
