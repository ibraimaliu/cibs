import pandas as pd
import datetime
from hijri_converter import convert
import locale
import os
from flask import Flask, render_template

app = Flask(__name__)

def configure_locale():
    try:
        # Définir la locale à partir de la variable d'environnement LC_TIME, avec une valeur par défaut 'fr_FR.utf8'
        locale.setlocale(locale.LC_TIME, os.getenv('LC_TIME', 'fr_FR.utf8'))
    except locale.Error as e:
        print(f"Échec de la configuration de la locale : {e}")

configure_locale()

def load_prayer_times():
    try:
        # Lire le fichier Excel
        df = pd.read_excel('data/prayer_times.xls')
        print("Fichier Excel chargé avec succès.")
        return df
    except Exception as e:
        print(f"Erreur lors du chargement du fichier Excel : {e}")
        return pd.DataFrame()

def get_prayer_times():
    try:
        df = load_prayer_times()

        # Obtenir la date actuelle
        today = datetime.date.today()

        # Filtrer les horaires pour la date actuelle
        todays_times = df[df['Date'] == pd.to_datetime(today)]

        if not todays_times.empty:
            prayer_times = todays_times.iloc[0].to_dict()
            # Formater les horaires sans les secondes
            for prayer in ['Fajr', 'Dhuhr', 'Asr', 'Maghrib', 'Isha', 'Levé du soleil']:
                if prayer in prayer_times and isinstance(prayer_times[prayer], pd.Timestamp):
                    prayer_times[prayer] = prayer_times[prayer].strftime('%H:%M')
            return prayer_times
        else:
            print("Aucun horaire de prière trouvé pour aujourd'hui.")
            return {}
    except Exception as e:
        print(f"Erreur dans get_prayer_times : {e}")
        return {}

@app.route('/')
def index():
    try:
        prayer_times = get_prayer_times()

        # Formater la date en français
        formatted_today = datetime.date.today().strftime('%A, %d %B %Y')

        # Convertir en date hégirienne
        hijri_date = convert.Gregorian.today().to_hijri()

        return render_template('index.html', prayer_times=prayer_times, today=formatted_today, hijri_date=hijri_date)
    except Exception as e:
        print(f"Erreur dans la route index : {e}")
        return "Une erreur s'est produite", 500

if __name__ == '__main__':
    app.run(debug=True)


# import pandas as pd
# import datetime
# from hijri_converter import convert
# import locale
# import os
# from flask import Flask, render_template

# app = Flask(__name__)

# def configure_locale():
#     try:
#         # Définir la locale à partir de la variable d'environnement LC_TIME, avec une valeur par défaut 'fr_FR.utf8'
#         locale.setlocale(locale.LC_TIME, os.getenv('LC_TIME', 'fr_FR.utf8'))
#     except locale.Error as e:
#         print(f"Échec de la configuration de la locale : {e}")

# configure_locale()

# def load_prayer_times():
#     try:
#         # Lire le fichier Excel
#         df = pd.read_excel('data/prayer_times.xls')
#         print("Fichier Excel chargé avec succès.")
#         return df
#     except Exception as e:
#         print(f"Erreur lors du chargement du fichier Excel : {e}")
#         return pd.DataFrame()

# def get_prayer_times():
#     try:
#         df = load_prayer_times()

#         # Obtenir la date actuelle
#         today = datetime.date.today()

#         # Filtrer les horaires pour la date actuelle
#         todays_times = df[df['Date'] == pd.to_datetime(today)]

#         if not todays_times.empty:
#             prayer_times = todays_times.iloc[0].to_dict()
#             # Formater les horaires sans les secondes
#             for prayer in ['Fajr', 'Dhuhr', 'Asr', 'Maghrib', 'Isha', 'Levé du soleil']:
#                 if prayer in prayer_times and isinstance(prayer_times[prayer], pd.Timestamp):
#                     prayer_times[prayer] = prayer_times[prayer].strftime('%H:%M')
#             return prayer_times
#         else:
#             print("Aucun horaire de prière trouvé pour aujourd'hui.")
#             return {}
#     except Exception as e:
#         print(f"Erreur dans get_prayer_times : {e}")
#         return {}

# @app.route('/')
# def index():
#     try:
#         prayer_times = get_prayer_times()

#         # Formater la date en français
#         formatted_today = datetime.date.today().strftime('%A, %d %B %Y')

#         # Convertir en date hégirienne
#         hijri_date = convert.Gregorian.today().to_hijri()

#         return render_template('index.html', prayer_times=prayer_times, today=formatted_today, hijri_date=hijri_date)
#     except Exception as e:
#         print(f"Erreur dans la route index : {e}")
#         return "Une erreur s'est produite", 500

# if __name__ == '__main__':
#     app.run(debug=True)
