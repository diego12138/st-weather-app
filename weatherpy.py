import streamlit as st
import requests
import datetime
import folium
from streamlit_folium import st_folium
from config import api_key

st.title('Weather App')



city = st.text_input('Enter city:')

if city:
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}'
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        temp_k = data['main']['temp']
        humidity = data['main']['humidity']
        description = data['weather'][0]['description']
        sunset_time = datetime.datetime.fromtimestamp(data['sys']['sunset']).strftime('%Y-%m-%d %H:%M:%S')
        sunrise_time = datetime.datetime.fromtimestamp(data['sys']['sunrise']).strftime('%Y-%m-%d %H:%M:%S')
        windspeed = data['wind']['speed']
        
        temp_c = round(temp_k - 273.15, 2)
        temp_f = round((temp_k - 273.15) * 9/5 + 32, 2)
        st.write(f'Temperature: {temp_c}°C | {temp_f}°F')
        st.write(f'Humidity: {humidity}%')
        st.write(f'Description: {description}')
        st.write(f"Sunset Time: {sunset_time}")
        st.write(f"Sunrise Time: {sunrise_time}")
        st.write(f"Wind Speed: {windspeed} m/s")
        if 'alerts' in data:
            for alert in data['alerts']:
                sender_name = alert['sender_name']
                event = alert['event']
                start_time = datetime.datetime.fromtimestamp(alert['start']).strftime('%Y-%m-%d %H:%M:%S')
                end_time = datetime.datetime.fromtimestamp(alert['end']).strftime('%Y-%m-%d %H:%M:%S')
                description = alert['description']
                tags = ', '.join(alert['tags'])
                
                st.write(f"Alert from {sender_name}: {event}")
                st.write(f"Start Time: {start_time}")
                st.write(f"End Time: {end_time}")
                st.write(f"Description: {description}")
                st.write(f"Tags: {tags}")
        else:
            st.write("No alerts for this area.")
    
        lat = data['coord']['lat']
        lon = data['coord']['lon']
        map = folium.Map(location=[lat, lon], zoom_start=12)
        folium.Marker([lat, lon], popup=city).add_to(map)
        st_folium(map,width=600,height=500)
    
    else:
        st.write(f"Error: {response.status_code}")
        st.write(f"Response: {response.text}")
        
