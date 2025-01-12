from dotenv import load_dotenv
from WeatherDashboard import WeatherDashboard

# Load environment variables
load_dotenv()


def main():
    dashboard = WeatherDashboard()

    # Create bucket if needed
    dashboard.create_bucket_if_not_exists()

    cities = ["Accra", "Kumasi", "Tamale"]

    for city in cities:
        print(f"\nFetching weather for {city}...")
        weather_data = dashboard.fetch_weather(city)
        if weather_data:
            temp = weather_data["main"]["temp"]
            feels_like = weather_data["main"]["feels_like"]
            humidity = weather_data["main"]["humidity"]
            description = weather_data["weather"][0]["description"]

            print(f"Temperature: {temp}°F")
            print(f"Feels like: {feels_like}°F")
            print(f"Humidity: {humidity}%")
            print(f"Conditions: {description}")

            # Save to S3
            success = dashboard.save_to_s3(weather_data, city)
            if success:
                print(f"Weather data for {city} saved to S3!")
        else:
            print(f"Failed to fetch weather data for {city}")


if __name__ == "__main__":
    main()
