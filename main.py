import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Konfiguracja strony
st.set_page_config(page_title="Kalkulator Handlarza - Gerard S.", layout="wide")

# --- CSS (TYLKO TE ZMIANY, KTÓRE CHCIAŁEŚ) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700&display=swap');
    * { font-family: 'Montserrat', sans-serif !important; }

    /* Usuwanie błędów technicznych */
    header, footer, #MainMenu { visibility: hidden !important; }

    /* Ciemny sidebar */
    [data-testid="stSidebar"] { background-color: #111111; color: white !important; }
    [data-testid="stSidebar"] label, [data-testid="stSidebar"] p { color: #ffffff !important; }

    /* Zacieśnienie sekcji Akcyza -> Rejestracja -> Transport */
    [data-testid="stSidebar"] hr {
        margin: 10px 0 !important;
        border-top: 1px solid rgba(255, 255, 255, 0.2) !important;
    }
    
    /* Podciągnięcie Transportu i innych pól wyżej */
    [data-testid="stSidebar"] .stNumberInput {
        margin-top: -10px !important;
    }

    /* Karty i tabele (Twoje oryginalne kolory) */
    .metric-card { background-color: white; padding: 20px; border-radius: 5px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); border: 1px solid #ddd; text-align: center; }
    .table-header { background-color: #cc0000; color: white; padding: 10px; font-weight: bold; border-radius: 5px 5px 0 0; }
    .table-container { background: white; padding: 15px; border: 1px solid #eee; border-radius: 0 0 5px 5px; }
    .row { display: flex; justify-content: space-between; padding: 5px 0; border-bottom: 1px solid #f9f9f9; }
    .total-row { display: flex; justify-content: space-between; padding-top: 10px; font-weight: bold; color: #28a745; }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    st.markdown('<div style="margin-top: -50px;"></div>', unsafe_allow_html=True)
    st.image("logo gerard s białe .png", width=180)
    
    kurs_eur = st.number_input("Kurs Euro", value=4.27, step=0.01)
    cena_eur = st.number_input("Cena auta w EURO", value=0)
    
    kwota_przeliczona = cena_eur * kurs_eur
    st.markdown(f"<p style='font-size: 12px; color: #aaa; margin-top: -15px;'>{kwota_przeliczona:,.2f} zł</p>", unsafe_allow_html=True)
    
    cena_pln_auto = st.number_input("Cena auta w PLN", value=float(kwota_przeliczona))
    cena_do_akcyzy = st.number_input("Cena auta do akcyzy", value=float(cena_pln_auto))
    
    # SEKCJA DO PODCIĄGNIĘCIA W GÓRĘ
    st.markdown("---")
    st.markdown("**Stawka Akcyzy**")
    akcyza_opcja = st.radio("akcyza", ["bez akcyzy", "do 2.0 l", "powyżej 2.0 l"], index=1, label_visibility="collapsed")
    
    st.markdown("---")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("**Rejestracja**")
        rejestracja_check = st.checkbox("Rej", value=True, label_visibility="collapsed")
    with c2:
        st.markdown("**Przegląd**")
        przeglad_opcja = st.radio("Prz", ["bez gazu", "z gazem"], index=0, label_visibility="collapsed")
    
    st.markdown("---")
    # TRANSPORT (teraz podciągnięty wyżej przez CSS margin-top)
    transport = st.number_input("Transport", value=1700)
    
    # RESZTA POL (LAKIEROWANIE ITD.)
    cena_lakieru = st.number_input("Cena lakierowania za element", value=500)
    ilosc_lakieru = st.number_input("Ilość elementów", value=0)
    koszt_lakiernika = cena_lakieru * ilosc_lakieru
    
    cena_czesci = st.number_input("Cena części", value=300)
    mechanik = st.number_input("Mechanik", value=700)
    myjnia = st.number_input("Myjnia", value=200)
    ogloszenia = st.number_input("Ogłoszenia", value=300)
    pozostale = st.number_input("Pozostałe", value=200)
    
    st.markdown("---")
    cena_sprzedazy = st.number_input("CENA SPRZEDAŻY", value=25000)

# --- OBLICZENIA I PANEL GŁÓWNY (BEZ ZMIAN) ---
stawka_akc = 0.031 if akcyza_opcja == "do 2.0 l" else (0.186 if akcyza_opcja == "powyżej 2.0 l" else 0)
koszt_akcyzy = cena_do_akcyzy * stawka_akc
suma_wydatki = (cena_pln_auto + koszt_akcyzy + transport + koszt_lakiernika + cena_czesci + mechanik + myjnia + ogloszenia + pozostale + (162 if rejestracja_check else 0) + (150 if przeglad_opcja == "bez gazu" else 245))
dochod = cena_sprzedazy - suma_wydatki

st.markdown(f"<h2 style='text-align: center; margin-top: -40px;'>Kalkulator Handlarza</h2>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align: center; margin-top: -15px;'>by Gerard S Digital Agency</p>", unsafe_allow_html=True)

# ... (Dalsza część Twoich wykresów i tabel bez zmian) ...

# Metryki
col_m1, col_m2, col_m3 = st.columns(3)
with col_m1:
    st.markdown(f"<div class='metric-card'><div class='metric-label'>Inwestycja Total</div><div class='metric-value'>{suma_wydatki:,.0f} zł</div></div>", unsafe_allow_html=True)
with col_m2:
    st.markdown(f"<div class='metric-card'><div class='metric-label'>Zysk Sprzedaży</div><div class='metric-value' style='color:#28a745;'>{zysk:,.0f} zł</div></div>", unsafe_allow_html=True)
with col_m3:
    st.markdown(f"<div class='metric-card'><div class='metric-label'>Marża</div><div class='metric-value'>{marza:.1f}%</div></div>", unsafe_allow_html=True)

# Tabele i wykres
st.markdown("<br>", unsafe_allow_html=True)
t1, t2 = st.columns([2, 1])

with t1:
    st.markdown("<div class='table-header'>Szczegółowe Koszty</div>", unsafe_allow_html=True)
    st.markdown(f"""
    <div class='table-container'>
        <div class='row'><span>Zakup auta</span><span>{cena_pln_auto:,.2f} zł</span></div>
        <div class='row'><span>Akcyza ({akcyza_opcja})</span><span>{koszt_akcyzy:,.2f} zł</span></div>
        <div class='row'><span>Transport</span><span>{transport:,.2f} zł</span></div>
        <div class='row'><span>Lakierowanie ({ilosc_lakieru} el.)</span><span>{koszt_lakiernika:,.2f} zł</span></div>
        <div class='row'><span>Serwis i Inne</span><span>{mechanik + pozostale:,.2f} zł</span></div>
        <div class='row'><span>Opłaty (Rej + Prz)</span><span>{koszt_rej + koszt_prz:,.2f} zł</span></div>
        <div class='total-row'><span>SUMA KOSZTÓW</span><span>{suma_wydatki:,.2f} zł</span></div>
    </div>
    """, unsafe_allow_html=True)

with t2:
    fig = go.Figure(data=[go.Pie(labels=['Auto', 'Koszty', 'Zysk'], values=[cena_pln_auto, suma_wydatki-cena_pln_auto, zysk], hole=.4)])
    fig.update_layout(margin=dict(t=0, b=0, l=0, r=0), height=250, showlegend=False)
    st.plotly_chart(fig, use_container_width=True)
