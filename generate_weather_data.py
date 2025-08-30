import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

# Create data folder if it doesn't exist
if not os.path.exists('data'):
    os.makedirs('data')
    print("📁 Created 'data' folder")

def generate_weather_data():
    print("🌤️ Starting weather data generation...")
    
    # 8 Indian cities
    cities = ['Delhi', 'Mumbai', 'Bangalore', 'Chennai', 
              'Kolkata', 'Hyderabad', 'Ahmedabad', 'Pune']
    
    # Realistic weather parameters for each city
    city_weather_profiles = {
        'Delhi': {
            'temp_min': 5, 'temp_max': 45, 'temp_avg': 25,
            'humidity_avg': 60, 'rain_days': 60, 'wind_avg': 8
        },
        'Mumbai': {
            'temp_min': 18, 'temp_max': 36, 'temp_avg': 28,
            'humidity_avg': 80, 'rain_days': 120, 'wind_avg': 12
        },
        'Bangalore': {
            'temp_min': 15, 'temp_max': 32, 'temp_avg': 23,
            'humidity_avg': 65, 'rain_days': 90, 'wind_avg': 6
        },
        'Chennai': {
            'temp_min': 22, 'temp_max': 38, 'temp_avg': 29,
            'humidity_avg': 75, 'rain_days': 100, 'wind_avg': 10
        },
        'Kolkata': {
            'temp_min': 12, 'temp_max': 38, 'temp_avg': 26,
            'humidity_avg': 70, 'rain_days': 110, 'wind_avg': 7
        },
        'Hyderabad': {
            'temp_min': 16, 'temp_max': 42, 'temp_avg': 26,
            'humidity_avg': 55, 'rain_days': 80, 'wind_avg': 9
        },
        'Ahmedabad': {
            'temp_min': 10, 'temp_max': 44, 'temp_avg': 28,
            'humidity_avg': 50, 'rain_days': 45, 'wind_avg': 11
        },
        'Pune': {
            'temp_min': 12, 'temp_max': 38, 'temp_avg': 24,
            'humidity_avg': 60, 'rain_days': 85, 'wind_avg': 8
        }
    }
    
    # Weather conditions
    conditions = ['Clear', 'Cloudy', 'Rainy', 'Partly Cloudy', 'Thunderstorm', 'Foggy']
    
    all_data = []
    start_date = datetime(2024, 1, 1)
    
    # Generate data for each city and each day
    for city in cities:
        print(f"Generating data for {city}...")
        profile = city_weather_profiles[city]
        
        for day in range(365):  # 365 days in 2024
            current_date = start_date + timedelta(days=day)
            
            # Add seasonal variation (winter=cold, summer=hot)
            season_factor = np.sin(2 * np.pi * day / 365)  # -1 to 1
            
            # Generate realistic temperature
            base_temp = profile['temp_avg']
            seasonal_variation = season_factor * 8  # ±8°C seasonal change
            daily_variation = np.random.normal(0, 3)  # Daily randomness
            temperature = base_temp + seasonal_variation + daily_variation
            
            # Ensure temperature stays in realistic range
            temperature = max(profile['temp_min'], min(profile['temp_max'], temperature))
            
            # Generate humidity (higher in monsoon season)
            monsoon_boost = 15 if 5 <= current_date.month <= 9 else 0  # May to Sept
            humidity = profile['humidity_avg'] + monsoon_boost + np.random.normal(0, 10)
            humidity = max(20, min(100, humidity))  # Keep between 20-100%
            
            # Generate rainfall (more likely in monsoon)
            is_monsoon = 6 <= current_date.month <= 9  # June to September
            rain_probability = 0.4 if is_monsoon else 0.1
            if np.random.random() < rain_probability:
                rainfall = np.random.exponential(8)  # Exponential distribution for rain
            else:
                rainfall = 0
            
            # Generate wind speed
            wind_speed = profile['wind_avg'] + np.random.normal(0, 3)
            wind_speed = max(0, wind_speed)
            
            # Generate atmospheric pressure
            pressure = 1013 + np.random.normal(0, 12)  # Standard pressure ± variation
            
            # Choose weather condition based on rainfall and other factors
            if rainfall > 10:
                condition = np.random.choice(['Rainy', 'Thunderstorm'], p=[0.7, 0.3])
            elif rainfall > 0:
                condition = 'Cloudy'
            elif humidity > 80:
                condition = np.random.choice(['Cloudy', 'Foggy'], p=[0.8, 0.2])
            else:
                condition = np.random.choice(['Clear', 'Partly Cloudy'], p=[0.6, 0.4])
            
            # Add record to dataset
            all_data.append({
                'Date': current_date.strftime('%Y-%m-%d'),
                'City': city,
                'Temperature_C': round(temperature, 1),
                'Humidity_%': round(humidity, 1),
                'Rainfall_mm': round(rainfall, 1),
                'Wind_Speed_kmh': round(wind_speed, 1),
                'Pressure_hPa': round(pressure, 1),
                'Weather_Condition': condition
            })
    
    # Convert to DataFrame
    df = pd.DataFrame(all_data)
    
    # Save to CSV file
    output_path = os.path.join('data', 'weather_data_8_cities_2024.csv')
    df.to_csv(output_path, index=False)
    
    print(f"✅ SUCCESS! Generated {len(df)} weather records")
    print(f"📁 Saved to: {output_path}")
    print(f"🏙️ Cities: {len(cities)} cities")
    print(f"📅 Date range: {df['Date'].min()} to {df['Date'].max()}")
    print(f"📊 Parameters: {list(df.columns)}")
    
    # Display sample data
    print("\n📋 SAMPLE DATA (First 10 rows):")
    print(df.head(10).to_string(index=False))
    
    print("\n📈 DATA SUMMARY:")
    print(df.describe())
    
    return df

# FIXED: Direct function call (no if __name__ needed)
print("🚀 Starting Weather Data Generation Script...")
weather_df = generate_weather_data()
print("\n🎉 Weather data generation completed successfully!")
print(f"📊 Final dataset shape: {weather_df.shape}")
print("✅ Ready for analysis!")