from flask import Flask, render_template
import pandas as pd
import datetime
from hijri_converter import convert
import locale
import os

app = Flask(__name__)

def configure_locale():
    try:
        # Définir la locale à partir de la variable d'environnement LC_TIME, avec une valeur par défaut ''
        locale.setlocale(locale.LC_TIME, os.getenv('LC_TIME', ''))
    except locale.Error as e:
        print(f"Failed to set locale: {e}")
        # En cas d'échec, utiliser une gestion de fallback ou afficher un message d'erreur

configure_locale()

def get_prayer_times():
    # Votre logique pour récupérer les horaires de prière reste inchangée
    pass

@app.route('/')
def index():
    prayer_times = get_prayer_times()
    
    today = datetime.date.today()
    formatted_today = today.strftime('%A, %d %B %Y')
    hijri_date = convert.Gregorian.today().to_hijri()

    return render_template('index.html', prayer_times=prayer_times, today=formatted_today, hijri_date=hijri_date)

if __name__ == '__main__':
    app.run(debug=True)
