from flask import Flask, render_template
import pandas as pd
import datetime
from hijri_converter import convert
import locale

app = Flask(__name__)

def configure_locale():
    try:
        # Essayer de définir la locale à 'fr_FR.utf8'
        locale.setlocale(locale.LC_TIME, 'fr_FR.utf8')
    except locale.Error:
        try:
            # Si 'fr_FR.utf8' n'est pas disponible, essayer avec 'fr_FR.UTF-8'
            locale.setlocale(locale.LC_TIME, 'fr_FR.UTF-8')
        except locale.Error:
            try:
                # Si ni 'fr_FR.utf8' ni 'fr_FR.UTF-8' ne sont disponibles, utiliser la locale par défaut du système
                locale.setlocale(locale.LC_TIME, '')
            except locale.Error as e:
                # En cas d'échec, afficher un message d'erreur et configurer une locale par défaut connue
                print(f"Failed to set locale: {e}")
                locale.setlocale(locale.LC_TIME, 'en_US.UTF-8')

configure_locale()

def get_prayer_times():
    # Lire le fichier Excel
    df = pd.read_excel('data/prayer_times.xlsx')

    # Filtrer les horaires pour la date actuelle
    today = datetime.date.today()
    todays_times = df[df['Date'] == pd.to_datetime(today)]

    if not todays_times.empty:
        prayer_times = todays_times.iloc[0].to_dict()
        # Formater les horaires sans les secondes
        for prayer in ['Fajr', 'Dhuhr', 'Asr', 'Maghrib', 'Isha', 'Levé du soleil']:
            if prayer in prayer_times:
                # Convertir en chaîne de caractères et enlever les secondes
                prayer_times[prayer] = prayer_times[prayer].strftime('%H:%M')
        return prayer_times
    else:
        return {}

@app.route('/')
def index():
    prayer_times = get_prayer_times()
    
    # Obtenir la date actuelle
    today = datetime.date.today()
    # Formater la date en français
    formatted_today = today.strftime('%A, %d %B %Y')
    # Convertir en date hégirienne
    hijri_date = convert.Gregorian.today().to_hijri()

    return render_template('index.html', prayer_times=prayer_times, today=formatted_today, hijri_date=hijri_date)

if __name__ == '__main__':
    app.run(debug=True)
