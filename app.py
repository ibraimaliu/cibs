from flask import Flask, render_template
import pandas as pd
import datetime
from hijri_converter import convert
import locale
import os

app = Flask(__name__)

def configure_locale():
    try:
        # Définir la locale à partir de la variable d'environnement LC_TIME, avec une valeur par défaut 'fr_FR.utf8'
        locale.setlocale(locale.LC_TIME, os.getenv('LC_TIME', 'fr_FR.utf8'))
    except locale.Error as e:
        print(f"Failed to set locale: {e}")
        # En cas d'échec, utiliser une gestion de fallback ou afficher un message d'erreur

configure_locale()

def get_prayer_times():
    try:
        # Lire le fichier Excel
        df = pd.read_excel('data/prayer_times.csv')
        print("Excel file loaded successfully.")
        
        # Convertir la colonne 'Date' en type datetime
        df['Date'] = pd.to_datetime(df['Date'])
        print(f"DataFrame after converting 'Date':\n{df}")
        
        # Filtrer les horaires pour la date actuelle
        today = datetime.date.today()
        print(f"Today's date: {today}")
        
        todays_times = df[df['Date'] == pd.to_datetime(today)]
        print(f"Filtered data for today: {todays_times}")

        if not todays_times.empty:
            prayer_times = todays_times.iloc[0].to_dict()
            # Formater les horaires sans les secondes
            for prayer in ['Fajr', 'Dhuhr', 'Asr', 'Maghrib', 'Isha', 'Levé du soleil']:
                if prayer in prayer_times and isinstance(prayer_times[prayer], pd.Timestamp):
                    # Convertir en chaîne de caractères et enlever les secondes
                    prayer_times[prayer] = prayer_times[prayer].strftime('%H:%M')
            print(f"Prayer times for today: {prayer_times}")
            return prayer_times
        else:
            print("No prayer times found for today.")
            return {}
    except Exception as e:
        print(f"Error in get_prayer_times: {e}")
        return {}

@app.route('/')
def index():
    try:
        prayer_times = get_prayer_times()

        # Obtenir la date actuelle
        today = datetime.date.today()
        # Formater la date en français
        formatted_today = today.strftime('%A, %d %B %Y')
        # Convertir en date hégirienne
        hijri_date = convert.Gregorian.today().to_hijri()

        return render_template('index.html', prayer_times=prayer_times, today=formatted_today, hijri_date=hijri_date)
    except Exception as e:
        print(f"Error in index route: {e}")
        return "An error occurred", 500

if __name__ == '__main__':
    app.run(debug=True)
