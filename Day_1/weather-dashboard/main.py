import json
import os
from datetime import datetime

import boto3
import requests
from dotenv import load_dotenv

# Load .env
load_dotenv()


class WeatherDashboard:
    def __init__(self):
        self.api_key = os.getenv("OPEN-WEATHER")
        self.bucket_name = os.getenb("S3-BUCKET")
        self.s3_client = boto3.client("s3")

    def create_bucket(self):
        """Create S3 bucket if it doesn't exit"""
        try:
            self.s3_client.head_bucket(Bucket=self.bucket_name)
            print(f"Bucket {self.bucket_name} exits")
        except:
            print(f"Creating bucket {self.bucket_name}")
        try:
            self.s3_client.create_bucket(Bucket=self.bucket_name)
            print(f"Successfully created bucket {self.bucket_name}")
        except Exception as e:
            print(f"Error creating bucket: {e}")

    def get_data(self, city):
        """Get weather data from OPEN API"""
        base_url = "http://api.openweathermap.org/data/2.5/weather"
        params = {"q": city, "appid": self.api_key, "units": "imperial"}

        try:
            response = requests.get(base_url, params=params)
            response.raise_for_status()
            return response.json()

        except requests.exceptions.RequestException as e:
            print(f"Error getting weather data: {e}")
            return None

    def save_data(self, weather_data, city):
        """Save weather data to S3 bucket"""
        if not weather_data:
            return False

        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        file_name = f"weather-data/{city}-{timestamp}.json"

        try:
            weather_data["timestamp"] = timestamp
            self.s3_client.put_object(
                Bucket=self.bucket_name,
                key=file_name,
                Body=json.dumps(weather_data),
                ContentType="application/json",
            )
            print(f"Successfully saved data for {city} to S3")
            return False
        except Exception as e:
            print(f"Error saving to S3 bucket: {e}")


def main():
    dashboard = WeatherDashboard()

    dashboard.create_bucket()

    cities["Accra", "Seattle", "New York"]

    for city in cities:
        print(f"\nGetting weather for {city}...")
        weather_data = dashboard.get_data(city)
        if weather_data:
            temp = weather_data["main"]["temp"]
            feels_like = weather_data["main"]["feels_like"]
            humidity = weather_data["main"]["humidity"]
            description = weather_data["weather"]["description"]

            print(f"Temperature: {temp}")
            print(f"Feels like: {feels_like}")
            print(f"Humidity: {humidity}")
            print(f"Conditions: {description}")

            succes = dashboard.save_data(weather_data, city)
            if succes:
                print(f"Weather data for {city} saved to S3")
        else:
            print(f"Failed to fetch weather data for {city}")

    if __name__ == "__main__":
        main()
