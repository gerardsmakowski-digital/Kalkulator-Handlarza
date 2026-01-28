import streamlit as st
import pandas as pd

# Ustawienia strony - Branding Twojej Agencji
st.set_page_config(page_title="Kalkulator Gerard S.", page_icon="📈", layout="centered")

# --- POPRAWIONA STYLIZACJA CSS ---
st.markdown("""
    <style>
    .stApp { background-color: #f8f9fa; }
    .main-header { color: #1E1E1E; text-align: center; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True) # Poprawiony parametr z Twojego błędu

st.markdown("<h1 class='main-header'>Gerard S. Digital Agency</h1>", unsafe_allow_html=True)
st.subheader("Kalkulator Importu Aut")

# --- LOGIKA KALKULATORA (Z Twojego Arkusz2) ---
with st.container():
    col1, col2 = st.columns(2)
    
    with col1:
        cena_eur = st.number_input("Cena auta (EUR)", value=5000, step=100)
        kurs_eur = st.number_input("Aktualny Kurs EUR", value=4.32, step=0.01)
    
    with col2:
        akcyza_opcja = st.selectbox("Wybierz Akcyzę", 
                                    ["Niska (3.1%)", "Wysoka (18.6%)", "Brak (0%)"])
        transport = st.number_input("Koszt transportu (PLN)", value=1500)

# Obliczenia
cena_pln = cena_eur * kurs_eur
stawka = 0.031 if "3.1%" in akcyza_opcja else (0.186 if "18.6%" in akcyza_opcja else 0)
wartosc_akcyzy = cena_pln * stawka
suma_kosztow = cena_pln + wartosc_akcyzy + transport

# --- WYNIK ---
st.divider()
st.metric(label="ŁĄCZNY KOSZT (PLN)", value=f"{suma_kosztow:,.2f} PLN")

# --- WYKRES (Zastępuje statyczne wykresy z Sheets) ---
chart_data = pd.DataFrame({
    'Kategoria': ['Auto', 'Akcyza', 'Transport'],
    'Koszt': [cena_pln, wartosc_akcyzy, transport]
})
st.bar_chart(chart_data.set_index('Kategoria'))
