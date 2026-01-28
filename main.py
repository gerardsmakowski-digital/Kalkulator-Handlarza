import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Konfiguracja strony
st.set_page_config(
    page_title="Kalkulator Handlarza - Gerard S.", 
    layout="wide",
    initial_sidebar_state="expanded" 
)

# --- CSS (Naprawa: Montserrat dla tekstu, Auto dla ikon) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700&display=swap');
    
    /* 1. Montserrat dla wszystkiego co NIE JEST ikoną */
    *:not(i):not(svg):not([class*="material"]):not([class*="icon"]):not([class*="Icon"]) {
        font-family: 'Montserrat', sans-serif !important;
    }

    /* 2. Zapewnienie, że ikony zachowują swoją czcionkę systemową */
    [data-testid="stIcon"], .material-icons, svg {
        font-family: inherit !important;
    }

    /* Ukrycie śmieci */
    footer, #MainMenu { visibility: hidden !important; }

    /* Sidebar Stylizacja */
    [data-testid="stSidebar"] { background-color: #111111; color: white !important; }
    [data-testid="stSidebar"] label, [data-testid="stSidebar"] p { color: #ffffff !important; font-size: 14px !important; }
    [data-testid="stSidebar"] hr { margin: 15px 0 !important; border-top: 1px solid rgba(255, 255, 255, 0.2) !important; }
    
    /* Karty Wyników */
    .metric-card { 
        background-color: white; padding: 15px; border-radius: 10px; 
        box-shadow: 0 4px 6px rgba(0,0,0,0.07); border: 1px solid #eee; 
        text-align: center; margin-bottom: 10px; min-height: 110px; 
        display: flex; flex-direction: column; justify-content: center; 
    }
    .metric-label { font-size: 11px; color: #666; font-weight: bold; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 4px; }
    .metric-value { font-size: 22px; color: #000; font-weight: 800; margin: 2px 0; }
    .metric-sub { font-size: 12px; color: #28a745; font-weight: bold; }

    /* Tabele */
    .table-header { background-color: #cc0000; color: white; padding: 12px; font-weight: bold; border-radius: 5px 5px 0 0; font-size: 16px; }
    .table-container { background: white; padding: 20px; border: 1px solid #eee; border-radius: 0 0 5px 5px; }
    .row { display: flex; justify-content: space-between; padding: 8px 0; border-bottom: 1px solid #f0f0f0; color: #333; font-size: 15px; }
    .total-row { display: flex; justify-content: space-between; padding-top: 12px; font-weight: bold; color: #28a745; font-size: 18px; border-top: 2px solid #eee; }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    st.markdown('<div style="margin-top: -50px;"></div>', unsafe_allow_html=True)
    try:
        st.image("logo gerard s białe .png", width=180)
    except:
        st.markdown("<h3 style='color:white;'>GERARD S</h3>", unsafe_allow_html=True)
    
    st.markdown("---")
    kurs_eur = st.number_input("Kurs Euro", value=4.27, step=0.01)
    cena_eur = st.number_input("Cena auta w EURO", value=3550.0)
    
    kwota_z_euro = cena_eur * kurs_eur
    st.markdown(f"<p style='font-size: 12px; color: #28a745; margin-top: -15px;'>Przeliczono: {kwota_z_euro:,.2f} zł</p>", unsafe_allow_html=True)
    
    cena_pln_auto = st.number_input("Cena auta w PLN", value=float(kwota_z_euro))
    cena_do_akcyzy = st.number_input("Cena auta do akcyzy", value=float(cena_pln_auto))
    
    st.markdown("---")
    akcyza_opcja = st.radio("Akcyza", ["do 2.0 l", "powyżej 2.0 l", "bez akcyzy"], index=0)
    
    col_rej, col_prz = st.columns(2)
    with col_rej:
        rejestracja_check = st.checkbox("Rejestracja", value=True)
    with col_prz:
        gaz_check = st.checkbox("LPG / Gaz", value=False)
    
    st.markdown("---")
    transport = st.number_input("Transport", value=1700)
    mechanik = st.number_input("Mechanik + Części", value=1000)
    myjnia_ogloszenia = st.number_input("Kosmetyka + Ogłoszenia", value=500)
    
    st.markdown("---")
    cena_sprzedazy = st.number_input("CENA SPRZEDAŻY", value=25000)

# --- LOGIKA ---
stawka_akc = 0.031 if akcyza_opcja == "do 2.0 l" else (0.186 if akcyza_opcja == "powyżej 2.0 l" else 0)
wartosc_akcyzy = cena_do_akcyzy * stawka_akc
koszt_rej = 162 if rejestracja_check else 0
koszt_prz = 245 if gaz_check else 150

suma_wydatki = cena_pln_auto + wartosc_akcyzy + transport + mechanik + myjnia_ogloszenia + koszt_rej + koszt_prz
przychod_brutto = cena_sprzedazy - suma_wydatki

if przychod_brutto > 0:
    vat_marza = przychod_brutto * (0.23 / 1.23)
    dochod_netto = (przychod_brutto - vat_marza) * 0.81 # Uproszczony dochodowy 19%
else:
    vat_marza = dochod_netto = 0

# --- PANEL GŁÓWNY ---
st.markdown("<h1 style='text-align: center; font-weight: 800;'>Kalkulator Handlarza</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #666;'>Gerard S Digital Agency</p>", unsafe_allow_html=True)

c1, c2, c3 = st.columns(3)
with c1:
    st.markdown(f"<div class='metric-card'><div class='metric-label'>Inwestycja</div><div class='metric-value'>{suma_wydatki:,.2f} zł</div></div>", unsafe_allow_html=True)
with c2:
    st.markdown(f"<div class='metric-card'><div class='metric-label'>Zysk Brutto</div><div class='metric-value' style='color:#28a745;'>{przychod_brutto:,.2f} zł</div></div>", unsafe_allow_html=True)
with c3:
    st.markdown(f"<div class='metric-card'><div class='metric-label'>Zysk Netto</div><div class='metric-value' style='color:#28a745;'>{dochod_netto:,.2f} zł</div></div>", unsafe_allow_html=True)

# Tabela
st.markdown("<div class='table-header'>Szczegóły Finansowe</div>", unsafe_allow_html=True)
st.markdown(f"""
<div class='table-container'>
    <div class='row'><span>Koszt zakupu i transportu:</span><span>{cena_pln_auto + transport:,.2f} zł</span></div>
    <div class='row'><span>Opłaty (Akcyza/Rej):</span><span>{wartosc_akcyzy + koszt_rej + koszt_prz:,.2f} zł</span></div>
    <div class='row'><span>Podatek VAT (marża):</span><span>{vat_marza:,.2f} zł</span></div>
    <div class='total-row'><span>SUMA KOSZTÓW:</span><span>{suma_wydatki:,.2f} zł</span></div>
</div>
""", unsafe_allow_html=True)
