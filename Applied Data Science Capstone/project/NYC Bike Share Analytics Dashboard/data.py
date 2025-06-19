import pandas as pd

def load_and_prepare_data(filepath="bike_trips_data.parquet"):
    """Loads and prepares the bike trip data from a Parquet file."""
    
    # Define only the columns we need to reduce memory usage
    required_columns = [
        'day_of_week', 'hour', 'member_casual', 
        'start_lat', 'start_lng', 'end_lat', 'end_lng',
        'trip_duration_min', 'distance_km',
        'start_station_name', 'end_station_name'
    ]
    
    df = pd.read_parquet(filepath, columns=required_columns)
    
    # Drop rows where location data is missing
    df.dropna(subset=['start_lat', 'start_lng', 'end_lat', 'end_lng'], inplace=True)
    
    # Ensure day_of_week is an ordered categorical type
    days_ordered = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    df['day_of_week'] = pd.Categorical(df['day_of_week'], categories=days_ordered, ordered=True)
    
    return df