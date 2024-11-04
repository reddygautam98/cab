import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Configure Seaborn aesthetics
sns.set(style="whitegrid")

# Load the dataset (with the fixed file path)
uber_data = pd.read_csv(r"C:\Users\reddy\Downloads\cab\uber_data.csv")

# Convert 'Date/Time' column to datetime format
if 'Date/Time' in uber_data.columns:
    uber_data['Date/Time'] = pd.to_datetime(uber_data['Date/Time'], errors='coerce')
else:
    print("Error: 'Date/Time' column not found in the dataset.")
    print("Available columns:", uber_data.columns)

# Check for missing values
print("Missing values in each column:")
print(uber_data.isnull().sum())

# Drop any duplicate rows
uber_data = uber_data.drop_duplicates()

# Verify changes
print("Data after processing:")
print(uber_data.head())
print(uber_data.info())

# Extract new features from the 'Date/Time' column if it exists
if 'Date/Time' in uber_data.columns:
    # Extract day, hour, and weekday from 'Date/Time'
    uber_data['day'] = uber_data['Date/Time'].dt.day
    uber_data['hour'] = uber_data['Date/Time'].dt.hour
    uber_data['weekday'] = uber_data['Date/Time'].dt.day_name()

    # Display the first few rows to check the new columns
    print(uber_data[['Date/Time', 'day', 'hour', 'weekday']].head())
else:
    print("Error: 'Date/Time' column not found for feature extraction.")

# Check if 'hour' column exists and plot rides per hour
if 'hour' in uber_data.columns:
    plt.figure(figsize=(10, 6))
    sns.countplot(data=uber_data, x='hour', palette='viridis')
    plt.title('Rides by Hour')
    plt.xlabel('Hour of Day')
    plt.ylabel('Number of Rides')
    plt.show()
else:
    print("Error: 'hour' column not found in the DataFrame. Please ensure the 'hour' feature is extracted from 'Date/Time'.")

# Check if 'weekday' column exists and plot rides per day of the week
if 'weekday' in uber_data.columns:
    plt.figure(figsize=(10, 6))
    sns.countplot(data=uber_data, x='weekday', 
                  order=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'], 
                  palette='coolwarm')
    plt.title('Rides by Day of the Week')
    plt.xlabel('Day of the Week')
    plt.ylabel('Number of Rides')
    plt.show()
else:
    print("Error: 'weekday' column not found in the DataFrame. Please ensure the 'weekday' feature is extracted from 'Date/Time'.")

# Check if 'Lon' and 'Lat' columns exist and plot pickup locations
if 'Lon' in uber_data.columns and 'Lat' in uber_data.columns:
    plt.figure(figsize=(10, 6))
    plt.scatter(uber_data['Lon'], uber_data['Lat'], alpha=0.4, s=1, c='blue')
    plt.title('Geographical Distribution of Uber Rides')
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.show()
else:
    print("Error: 'Lon' and/or 'Lat' columns not found in the DataFrame. Please ensure longitude and latitude data are correctly labeled.")

# Check if required columns are present for the heatmap
if 'hour' in uber_data.columns and 'weekday' in uber_data.columns and 'Base' in uber_data.columns:
    # Ensure 'weekday' has a consistent order from Monday to Sunday
    weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    uber_data['weekday'] = pd.Categorical(uber_data['weekday'], categories=weekdays, ordered=True)

    # Create pivot table
    hour_day = uber_data.pivot_table(index='hour', columns='weekday', values='Base', aggfunc='count').fillna(0)

    # Plot the heatmap
    plt.figure(figsize=(12, 8))
    sns.heatmap(hour_day, cmap='YlGnBu', annot=True, fmt='.0f', cbar=True)
    plt.title('Heatmap of Rides by Hour and Day of Week')
    plt.xlabel('Day of the Week')
    plt.ylabel('Hour of the Day')
    plt.show()
else:
    print("Error: One or more required columns ('hour', 'weekday', 'Base') not found in the DataFrame.")
