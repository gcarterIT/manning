# Import the necessary libraries
# Read the following dataset into a pandas dataframe: '../source/tourist_arrivals_countries.csv' and parse the Date field as a date
# Filter out rows before 1994 and after 2018
# Extract the year from the Date field and create a new column called Year
# Group the data by Year and calculate the sum of tourist arrivals for each year

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Read the dataset into a pandas dataframe and parse the Date field as a date
df = pd.read_csv('E:/docs/book_reviews/manning/Data_Storytelling_duca/review_2_20240213/github_materials/Data-Storytelling-with-Python-Altair-and-Generative-AI/CaseStudies/tourist-arrivals/source/tourist_arrivals_countries.csv', parse_dates=['Date'])

# Filter out rows before 1994 and after 2018
df = df[(df['Date'].dt.year >= 1994) & (df['Date'].dt.year <= 2018)]

# Extract the year from the Date field and create a new column called Year
df['Year'] = df['Date'].dt.year

# Group the data by Year and calculate the sum of tourist arrivals for each year
df = df.groupby('Year').agg({'Tourist Arrivals': np.sum}).reset_index()

# Add a new column to the DataFrame called PI containing the difference for each country between the number of tourist arrivals in the year and 1994
df['PI'] = df['Tourist Arrivals'] - df['Tourist Arrivals'][0]

# Use the Altair library to plot the PI column for each country versus the Year
import altair as alt
alt.Chart(df).mark_line().encode(
    x='Year',
    y='PI'
).properties(
    title='Tourist Arrivals vs. Year'
)

# Create a new chart with the following text: 'Thanks to the introduction\n of low-cost flights,\nPortugal has experienced\nan increase\nin tourist arrivals\nof over 200% in 25 years,\neven surpassing the increase\nin the other countries.' Use the \n as a line break to format the text. Set the font size to 14. 
# Place the two graphs side by side. Set title to 'Tourist Arrivals in Portugal (1994-2018)'
# Save the chart as an HTML. Name the file chart.html

text = 'Thanks to the introduction\n of low-cost flights,\nPortugal has experienced\nan increase\nin tourist arrivals\nof over 200% in 25 years,\neven surpassing the increase\nin the other countries.'



