import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Konfiguracja strony
st.set_page_config(page_title="Kalkulator Handlarza - Gerard S.", layout="wide")

# --- CSS (Rozszerzony o style kafelków) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700&display=swap');
    * { font-family: 'Montserrat', sans-serif !important; }
    header, footer, #MainMenu { visibility: hidden !important; }

    /* Sidebar */
    [data-testid="stSidebar"] { background-color: #111111; color: white !important; }
    [data-testid="stSidebar"] label, [data-testid="stSidebar"] p { color: #ffffff !important; }
    [data-testid="stSidebar"] hr { margin: 10px 0 !important; border-top: 1px solid rgba(255, 255, 255, 0.2) !important; }

    /* Dashboard Cards */
    .metric-card { background-color: white; padding: 15px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); border: 1px solid #eee; text-align: center; margin-bottom: 10px; }
    .metric-label { font-size: 11px; color: #666; font-weight: bold; text-transform: uppercase; letter-spacing: 0.5px; }
    .metric-value { font-size: 22px; color: #000; font-weight: bold; margin: 5px 0; }
    .metric-sub { font-size: 12px; color: #28a745; font-weight: bold; }

    /* Tables */
    .table-header { background-color: #cc0000; color: white; padding: 10px; font-weight: bold; border-radius: 5px 5px 0 0; }
    .table-container { background: white; padding: 15px; border: 1px solid #eee; border-radius: 0 0 5px 5px; }
    .row { display: flex; justify-content: space-between; padding: 6px 0; border-bottom: 1px solid #f0f0f0; color: #333; font-size: 14px; }
    .total-row { display: flex; justify-content: space-between; padding-top: 10px; font-weight: bold; color: #28a745; font-size: 16px; border-top: 2px solid #eee; }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    st.markdown('<div style="margin-top: -50px;"></div>', unsafe_allow_html=True)
    st.image("logo gerard s białe .png", width=180)
    
    kurs_eur = st.number_input("Kurs Euro", value=4.27, step=0.01)
    cena_eur = st.number_input("Cena auta w EURO", value=0.0)
    
    kwota_z_euro = cena_eur * kurs_eur
    if cena_eur > 0:
        st.markdown(f"<p style='font-size: 12px; color: #28a745; margin-top: -15px;'>Przeliczono z Euro: {kwota_z_euro:,.2f} zł</p>", unsafe_allow_html=True)
        cena_pln_auto = st.number_input("Cena auta w PLN", value=float(kwota_z_euro))
    else:
        cena_pln_auto = st.number_input("Cena auta w PLN", value=0.0)

    finalna_cena_samochodu = cena_pln_auto
    cena_do_akcyzy = st.number_input("Cena auta do akcyzy", value=float(finalna_cena_samochodu))
    
    st.markdown("---")
    akcyza_opcja = st.radio("Akcyza", ["bez akcyzy", "do 2.0 l", "powyżej 2.0 l"], index=1)
    
    st.markdown("---")
    c_rej, c_prz = st.columns(2)
    with c_rej:
        rejestracja_check = st.checkbox("Rejestracja", value=True)
    with c_prz:
        przeglad_opcja = st.radio("Przegląd", ["bez gazu", "z gazem"], index=0)
    
    st.markdown("---")
    transport = st.number_input("Transport", value=1700)
    cena_lakieru = st.number_input("Lakier/elem", value=500)
    ilosc_lakieru = st.number_input("Ilość elem", value=0)
    koszt_lakiernika = cena_lakieru * ilosc_lakieru
    
    cena_czesci = st.number_input("Części", value=300)
    mechanik = st.number_input("Mechanik", value=700)
    myjnia = st.number_input("Myjnia", value=200)
    ogloszenia = st.number_input("Ogłoszenia", value=300)
    pozostale = st.number_input("Pozostałe", value=200)
    
    st.markdown("---")
    cena_sprzedazy = st.number_input("CENA SPRZEDAŻY", value=25000)

# --- OBLICZENIA ---
stawka_akc = 0.031 if akcyza_opcja == "do 2.0 l" else (0.186 if akcyza_opcja == "powyżej 2.0 l" else 0)
wartosc_akcyzy = cena_do_akcyzy * stawka_akc
koszt_rej = 162 if rejestracja_check else 0
koszt_prz = 150 if przeglad_opcja == "bez gazu" else 245

suma_wydatki = (finalna_cena_samochodu + wartosc_akcyzy + transport + koszt_lakiernika + 
                cena_czesci + mechanik + myjnia + ogloszenia + pozostale + koszt_rej + koszt_prz)

przychod_roznica = cena_sprzedazy - suma_wydatki

if przychod_roznica > 0:
    vat_kwota = przychod_roznica * (0.23 / 1.23)
    baza_po_vat = przychod_roznica - vat_kwota
    skladka_zdrowotna = baza_po_vat * 0.049
    podstawa_dochodowy = baza_po_vat - skladka_zdrowotna
    podatek_dochodowy = podstawa_dochodowy * 0.19
else:
    vat_kwota = podatek_dochodowy = skladka_zdrowotna = 0

podatki_razem = vat_kwota + podatek_dochodowy + skladka_zdrowotna
dochod_na_czysto = przychod_roznica - podatki_razem

# Procenty względem ceny zakupu auta
procent_przychod = (przychod_roznica / finalna_cena_samochodu * 100) if finalna_cena_samochodu > 0 else 0
procent_dochod = (dochod_na_czysto / finalna_cena_samochodu * 100) if finalna_cena_samochodu > 0 else 0

# --- PANEL GŁÓWNY ---
st.markdown(f"<h2 style='text-align: center; margin-top: -30px;'>Kalkulator Handlarza</h2>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align: center; color: #666; margin-bottom: 30px;'>by Gerard S Digital Agency</p>", unsafe_allow_html=True)

# GŁÓWNY UKŁAD DASHBOARDU (Siatka kafelków po środku)
dash_col_1, dash_col_2, dash_col_3 = st.columns([1, 4, 1])

with dash_col_2:
    # RZĄD 1: Przychód i Dochód
    r1_1, r1_2 = st.columns(2)
    r1_1.markdown(f"""<div class='metric-card'>
        <div class='metric-label'>Przychód (Zysk)</div>
        <div class='metric-value' style='color:#28a745;'>{przychod_roznica:,.2f} zł</div>
        <div class='metric-sub'>{procent_przychod:.1f}% ceny auta</div>
    </div>""", unsafe_allow_html=True)
    r1_2.markdown(f"""<div class='metric-card'>
        <div class='metric-label'>Dochód (Na czysto)</div>
        <div class='metric-value' style='color:#28a745;'>{dochod_na_czysto:,.2f} zł</div>
        <div class='metric-sub'>{procent_dochod:.1f}% ceny auta</div>
    </div>""", unsafe_allow_html=True)

    # RZĄD 2: VAT, Dochodowy, Zdrowotna
    r2_1, r2_2, r2_3 = st.columns(3)
    r2_1.markdown(f"""<div class='metric-card'>
        <div class='metric-label'>VAT</div>
        <div class='metric-value' style='font-size:18px;'>{vat_kwota:,.2f} zł</div>
    </div>""", unsafe_allow_html=True)
    r2_2.markdown(f"""<div class='metric-card'>
        <div class='metric-label'>Dochodowy (19%)</div>
        <div class='metric-value' style='font-size:18px;'>{podatek_dochodowy:,.2f} zł</div>
    </div>""", unsafe_allow_html=True)
    r2_3.markdown(f"""<div class='metric-card'>
        <div class='metric-label'>Zdrowotna (4,9%)</div>
        <div class='metric-value' style='font-size:18px;'>{skladka_zdrowotna:,.2f} zł</div>
    </div>""", unsafe_allow_html=True)

    # RZĄD 3: Inwestycja i Podatki Razem
    r3_1, r3_2 = st.columns(2)
    r3_1.markdown(f"""<div class='metric-card'>
        <div class='metric-label'>Inwestycja (Suma Wydatków)</div>
        <div class='metric-value' style='color:#000;'>{suma_wydatki:,.2f} zł</div>
    </div>""", unsafe_allow_html=True)
    r3_2.markdown(f"""<div class='metric-card'>
        <div class='metric-label'>Podatki Razem</div>
        <div class='metric-value' style='color:#cc0000;'>{podatki_razem:,.2f} zł</div>
    </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# TABELE NA DOLE
t1, t2 = st.columns(2)
with t1:
    st.markdown("<div class='table-header'>Wydatki - szczegóły</div>", unsafe_allow_html=True)
    st.markdown(f"""<div class='table-container'>
        <div class='row'><span>Samochód</span><span>{finalna_cena_samochodu:,.2f} zł</span></div>
        <div class='row'><span>Akcyza</span><span>{wartosc_akcyzy:,.2f} zł</span></div>
        <div class='row'><span>Transport</span><span>{transport:,.2f} zł</span></div>
        <div class='row'><span>Lakiernik</span><span>{koszt_lakiernika:,.2f} zł</span></div>
        <div class='row'><span>Mechanik</span><span>{mechanik:,.2f} zł</span></div>
        <div class='row'><span>Części</span><span>{cena_czesci:,.2f} zł</span></div>
        <div class='row'><span>Przegląd</span><span>{koszt_prz:,.2f} zł</span></div>
        <div class='row'><span>Rejestracja</span><span>{koszt_rej:,.2f} zł</span></div>
        <div class='row'><span>Myjnia</span><span>{myjnia:,.2f} zł</span></div>
        <div class='row'><span>Ogłoszenia</span><span>{ogloszenia:,.2f} zł</span></div>
        <div class='row'><span>Pozostałe</span><span>{pozostale:,.2f} zł</span></div>
        <div class='total-row' style='color:#000;'><span>SUMA WYDATKÓW</span><span>{suma_wydatki:,.2f} zł</span></div>
    </div>""", unsafe_allow_html=True)

with t2:
    st.markdown("<div class='table-header'>Przychody - szczegóły</div>", unsafe_allow_html=True)
    st.markdown(f"""<div class='table-container'>
        <div class='row'><span>Przychód (Różnica)</span><span>{przychod_roznica:,.2f} zł</span></div>
        <div class='row'><span>Dochód (Na czysto)</span><span style='color:#28a745; font-weight:bold;'>{dochod_na_czysto:,.2f} zł</span></div>
        <div class='row'><span>Vat (23% w marży)</span><span>{vat_kwota:,.2f} zł</span></div>
        <div class='row'><span>Podatek dochodowy 19%</span><span>{podatek_dochodowy:,.2f} zł</span></div>
        <div class='row'><span>Składka zdrowotna 4,90%</span><span>{skladka_zdrowotna:,.2f} zł</span></div>
        <div class='total-row' style='color:#cc0000;'><span>Podatki razem</span><span>{podatki_razem:,.2f} zł</span></div>
    </div>""", unsafe_allow_html=True)
