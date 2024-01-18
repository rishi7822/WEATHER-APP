import tkinter as tk
from tkinter import ttk, messagebox
import requests
from plyer import notification

def get_weather(api_key, city):
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        'q': city,
        'appid': api_key,
        'units': 'metric'
    }

    response = requests.get(base_url, params=params)

    if response.status_code == 200:
        data = response.json()
        return data
    else:
        return None

def display_weather(weather_data):
    if weather_data:
        city = weather_data['name']
        description = weather_data['weather'][0]['description']
        temperature = weather_data['main']['temp']
        air_quality = weather_data.get('main', {}).get('aqi', {}).get('value')

        result_text.set(f"Weather in {city}: {description}\nTemperature: {temperature}°C\nAir Quality Index: {air_quality}")
        make_recommendations(description)
        send_notification(f"Weather in {city}", f"{description}\nTemperature: {temperature}°C\nAir Quality Index: {air_quality}")
        check_for_alerts(temperature, air_quality)
    else:
        messagebox.showerror("Error", "Failed to fetch weather data.")

def make_recommendations(weather_description):
    recommendations = ""
    
    if "rain" in weather_description.lower():
        recommendations += "Don't forget your umbrella!\n"
    
    if "snow" in weather_description.lower():
        recommendations += "It might be a good day for some snow activities!\n"
    
    if "clear" in weather_description.lower():
        recommendations += "Enjoy the clear skies and go for a walk!\n"
    
    recommendation_text.set(recommendations)

def send_notification(title, message):
    notification.notify(
        title=title,
        message=message,
        timeout=10
    )

def check_for_alerts(temperature, air_quality):
    if temperature < 0:
        send_alert("Freezing Alert", "Extreme cold temperatures detected!")
    elif temperature > 30:
        send_alert("Heat Alert", "Extreme heat conditions detected!")
    
    if air_quality and air_quality > 100:  # You can adjust the threshold as needed
        send_alert("Air Quality Alert", f"High air pollution detected! (AQI: {air_quality})")

def send_alert(title, message):
    messagebox.showwarning(title, message)

def on_submit():
    city = city_entry.get()
    if not city:
        messagebox.showwarning("Warning", "Please enter a city name.")
        return

    weather_data = get_weather(api_key, city)
    display_weather(weather_data)

# GUI setup
api_key = "5d6e993a1c98edb203650e39708114ae"

root = tk.Tk()
root.title("Weather App")

style = ttk.Style()

# Configure style
style.configure("TFrame", background="#333")
style.configure("TLabel", background="#333", foreground="#ccc", font=("Helvetica", 12))
style.configure("TButton", background="#007BFF", foreground="white", font=("Helvetica", 12))
style.map("TButton", background=[("active", "#0056b3")])

frame = ttk.Frame(root)
frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
frame.columnconfigure(0, weight=1)
frame.rowconfigure(0, weight=1)

label = ttk.Label(frame, text="Enter city name:")
label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)

city_entry = ttk.Entry(frame)
city_entry.grid(row=0, column=1, padx=5, pady=5, sticky=(tk.W, tk.E))

submit_button = ttk.Button(frame, text="Get Weather", command=on_submit)
submit_button.grid(row=1, column=0, columnspan=2, pady=10, sticky=(tk.W, tk.E))

result_text = tk.StringVar()
result_label = ttk.Label(frame, textvariable=result_text, wraplength=400)
result_label.grid(row=2, column=0, columnspan=2, pady=10, sticky=(tk.W, tk.E))

recommendation_text = tk.StringVar()
recommendation_label = ttk.Label(frame, textvariable=recommendation_text, wraplength=400)
recommendation_label.grid(row=3, column=0, columnspan=2, pady=10, sticky=(tk.W, tk.E))

root.mainloop()
