import firebase_admin
from firebase_admin import credentials, firestore
from pytrends.request import TrendReq
import feedparser
import os

# 1. Configuración de Firebase
# Debes subir el archivo 'serviceAccountKey.json' a tu repo (privado) o Termux
if not firebase_admin._apps:
    cred = credentials.Certificate('serviceAccountKey.json')
    firebase_admin.initialize_app(cred)

db = firestore.client()

def get_real_trends():
    trends_list = []
    
    # A. Obtener tendencias de búsqueda de Google (Lo que la gente busca ahora)
    try:
        pytrends = TrendReq(hl='es-MX', tz=360)
        df = pytrends.trending_searches(pn='mexico') # Puedes cambiar a 'united_states'
        google_trend = df[0].iloc[0]
        trends_list.append({
            "title": f"Tendencia masiva: {google_trend}",
            "impact": "Muy Alto",
            "category": "General",
            "source": "Google Trends"
        })
    except Exception as e:
        print(f"Error en Google Trends: {e}")

    # B. Obtener tendencias tecnológicas vía RSS (Noticias frescas)
    try:
        # Usamos el feed de TechCrunch o sitios similares para jóvenes emprendedores
        feed = feedparser.parse('https://techcrunch.com/feed/')
        for i in range(2): # Tomamos las 2 noticias más nuevas
            entry = feed.entries[i]
            trends_list.append({
                "title": entry.title,
                "impact": "Alto",
                "category": "Tech/Business",
                "source": "TechCrunch"
            })
    except Exception as e:
        print(f"Error en RSS: {e}")

    return trends_list

def upload_to_zent():
    real_data = get_real_trends()
    
    if real_data:
        # Guardamos la lista completa en la colección para que la app la lea
        doc_ref = db.collection('daily_trends').document('latest')
        doc_ref.set({
            "trends": real_data,
            "last_update": firestore.SERVER_TIMESTAMP
        })
        print(f"ZENT: {len(real_data)} tendencias reales actualizadas con éxito.")

if __name__ == "__main__":
    upload_to_zent()
