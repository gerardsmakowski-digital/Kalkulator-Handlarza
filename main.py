import streamlit as st
import pandas as pd

# Ustawienia strony - Branding Gerard S.
st.set_page_config(page_title="Kalkulator Importu - Gerard S.", layout="wide")

# --- STYLIZACJA WIZUALNA (Ciemny motyw i układ) ---
st.markdown("""
    <style>
    [data-testid="stSidebar"] { background-color: #1E1E1E; color: white; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; border: 1px solid #eee; }
    .main-title { color: #1E1E1E; font-size: 28px; font-weight: bold; margin-bottom: 20px; }
    </style>
    """, unsafe_allow_html=True)

# --- PASEK BOCZNY (Ciemna listwa po lewej) ---
with st.sidebar:
    st.image("https://via.placeholder.com/150x50?text=GERARD+S.", use_container_width=True) # Tu wstawisz swoje logo
    st.header("Dane wejściowe")
    
    kurs_eur = st.number_input("Kurs EUR (PLN)", value=4.32, step=0.01)
    cena_eur = st.number_input("Cena auta (EUR)", value=5000, step=100)
    
    st.divider()
    
    akcyza_opcja = st.selectbox("Stawka Akcyzy", 
                                ["Niska (3.1%)", "Wysoka (18.6%)", "Zwolniony (0%)"])
    
    transport = st.number_input("Transport (PLN)", value=1500)
    
    with st.expander("Inne koszty (PLN)"):
        mechanik = st.number_input("Mechanik", value=0)
        lakiernik = st.number_input("Blacharz/Lakiernik", value=0)
        rejestracja = st.number_input("Rejestracja/Tłumaczenia", value=256)

# --- LOGIKA OBLICZEŃ (Z Twojego arkusza) ---
cena_pln = cena_eur * kurs_eur
stawka = 0.031 if "3.1%" in akcyza_opcja else (0.186 if "18.6%" in akcyza_opcja else 0)
wartosc_akcyzy = cena_pln * stawka
suma_wszystkich_kosztow = cena_pln + wartosc_akcyzy + transport + mechanik + lakiernik + rejestracja

# --- PANEL GŁÓWNY (Wyniki po prawej) ---
st.markdown("<div class='main-title'>Podsumowanie Importu</div>", unsafe_allow_html=True)

c1, c2 = st.columns(2)
with c1:
    st.metric("ŁĄCZNY KOSZT (PLN)", f"{suma_wszystkich_kosztow:,.2f} PLN")
with c2:
    zysk_szacowany = st.number_input("Twoja cena sprzedaży (PLN)", value=int(suma_wszystkich_kosztow + 5000))
    marza = zysk_szacowany - suma_wszystkich_kosztow
    st.metric("SZACOWANY ZYSK", f"{marza:,.2f} PLN", delta=f"{marza/suma_wszystkich_kosztow*100:.1f}% marży")

st.divider()

# Wykres struktury kosztów (bardziej pro)
df_wiz = pd.DataFrame({
    'Kategoria': ['Auto (Netto)', 'Akcyza', 'Transport', 'Pozostałe'],
    'Koszt': [cena_pln, wartosc_akcyzy, transport, mechanik + lakiernik + rejestracja]
})
st.write("### Gdzie idą pieniądze?")
st.bar_chart(df_wiz.set_index('Kategoria'))
