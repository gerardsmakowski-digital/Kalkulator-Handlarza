import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# 1. KONFIGURACJA STRONY
st.set_page_config(
    page_title="Kalkulator Handlarza - Gerard S.", 
    layout="wide",
    initial_sidebar_state="expanded" 
)

# 2. CSS - NAPRAWA CZCIONEK, PRZYCISKÓW I IKON
st.markdown("""
    <style>
    /* Ładowanie czcionek z Twojego folderu /fonts/ na GitHubie */
    @font-face {
        font-family: 'Montserrat';
        src: url('fonts/montserrat-v30-latin-latin-ext-regular.woff2') format('woff2');
        font-weight: 400;
    }
    @font-face {
        font-family: 'Montserrat';
        src: url('fonts/montserrat-v30-latin-latin-ext-700.woff2') format('woff2');
        font-weight: 700;
    }
    @font-face {
        font-family: 'Montserrat';
        src: url('fonts/montserrat-v30-latin-latin-ext-800.woff2') format('woff2');
        font-weight: 800;
    }

    /* Zastosowanie czcionki dla całej aplikacji */
    html, body, [class*="st-"], div, p, h1, h2, h3, h4, label, span {
        font-family: 'Montserrat', sans-serif !important;
    }

    /* Naprawa widoczności PLUS / MINUS w polach numerycznych */
    button[data-testid="stNumberInputStepUp"], 
    button[data-testid="stNumberInputStepDown"] {
        color: #111111 !important;
        background-color: #f0f2f6 !important;
        border: 1px solid #dcdfe4 !important;
        opacity: 1 !important;
    }

    /* Naprawa ikon Streamlit (strzałki sidebaru itp.) */
    [data-testid="stBaseButton-headerNoPadding"] span, 
    [data-testid="stExpandSidebarButton"] span {
        font-family: "Material Symbols Rounded" !important;
    }

    header[data-testid="stHeader"] { visibility: hidden; height: 0px; }
    footer { visibility: hidden !important; }
    #MainMenu { visibility: hidden !important; }
    .block-container { padding-top: 2rem !important; }

    /* Sidebar - Stylizacja */
    [data-testid="stSidebar"] { background-color: #111111; color: white !important; }
    [data-testid="stSidebar"] label, [data-testid="stSidebar"] p { color: #ffffff !important; }

    /* Dashboard Cards */
    .metric-card { 
        background-color: white; padding: 15px; border-radius: 10px; 
        box-shadow: 0 4px 6px rgba(0,0,0,0.07); border: 1px solid #eee; 
        text-align: center; margin-bottom: 10px; min-height: 110px; 
        display: flex; flex-direction: column; justify-content: center; 
    }
    .metric-label { font-size: 11px; color: #666; font-weight: bold; text-transform: uppercase; margin-bottom: 4px; }
    .metric-value { font-size: 22px; color: #000; font-weight: 800; margin: 2px 0; }
    .metric-sub { font-size: 12px; color: #28a745; font-weight: bold; }

    /* Tables */
    .table-header { background-color: #cc0000; color: white; padding: 12px; font-weight: bold; border-radius: 5px 5px 0 0; }
    .table-container { background: white; padding: 20px; border: 1px solid #eee; border-radius: 0 0 5px 5px; margin-bottom: 20px;}
    .row { display: flex; justify-content: space-between; padding: 8px 0; border-bottom: 1px solid #f0f0f0; color: #333; }
    .total-row { display: flex; justify-content: space-between; padding-top: 12px; font-weight: bold; color: #28a745; font-size: 18px; border-top: 2px solid #eee; }
    </style>
    """, unsafe_allow_html=True)

# 3. SIDEBAR
with st.sidebar:
    st.markdown('<div style="margin-top: -50px;"></div>', unsafe_allow_html=True)
    try:
        st.image("logo gerard s białe .png", width=180)
    except:
        st.markdown("### GERARD S.")
    
    kurs_eur = st.number_input("Kurs Euro", value=4.27, step=0.01)
    cena_eur = st.number_input("Cena auta w EURO", value=3550.0)
    
    kwota_z_euro = cena_eur * kurs_eur
    st.markdown(f"<p style='font-size: 12px; color: #28a745; margin-top: -15px;'>Przeliczono: {kwota_z_euro:,.2f} zł</p>", unsafe_allow_html=True)
    
    cena_pln_auto = st.number_input("Cena auta w PLN", value=float(kwota_z_euro))
    cena_do_akcyzy = st.number_input("Cena auta do akcyzy", value=float(cena_pln_auto))
    
    st.markdown("---")
    akcyza_opcja = st.radio("Akcyza", ["bez akcyzy", "do 2.0 l", "powyżej 2.0 l"], index=1)
    
    st.markdown("---")
    rejestracja_check = st.checkbox("Rejestracja", value=True)
    przeglad_opcja = st.radio("Przegląd", ["bez gazu", "z gazem"], index=0)
    
    st.markdown("---")
    transport = st.number_input("Transport", value=1700)
    cena_lakieru = st.number_input("Lakier/elem", value=500)
    ilosc_lakieru = st.number_input("Ilość elem", value=0)
    koszt_lakiernika = cena_lakieru * ilosc_lakieru
    
    mechanik = st.number_input("Mechanik", value=700)
    cena_czesci = st.number_input("Części", value=300)
    myjnia = st.number_input("Myjnia", value=200)
    ogloszenia = st.number_input("Ogłoszenia", value=300)
    pozostale = st.number_input("Pozostałe", value=200)
    
    st.markdown("---")
    cena_sprzedazy = st.number_input("CENA SPRZEDAŻY", value=35000)

    st.markdown("---")
    st.markdown("<div style='text-align: center;'><a href='https://gerard-s.pl' target='_blank' style='color: white; text-decoration: none; font-weight: bold;'>www.gerard-s.pl</a></div>", unsafe_allow_html=True)

# 4. OBLICZENIA (LOGIKA)
stawka_akc = 0.031 if akcyza_opcja == "do 2.0 l" else (0.186 if akcyza_opcja == "powyżej 2.0 l" else 0)
wartosc_akcyzy = cena_do_akcyzy * stawka_akc
koszt_rej = 162 if rejestracja_check else 0
koszt_prz = 150 if przeglad_opcja == "bez gazu" else 245

suma_wydatki = (cena_pln_auto + wartosc_akcyzy + transport + koszt_lakiernika + 
                cena_czesci + mechanik + myjnia + ogloszenia + pozostale + koszt_rej + koszt_prz)

pozostale_suma = suma_wydatki - cena_pln_auto - wartosc_akcyzy
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

# Definicja brakujących zmiennych dla ROI
procent_przychod = (przychod_roznica / suma_wydatki * 100) if suma_wydatki > 0 else 0
procent_dochod = (dochod_na_czysto / cena_pln_auto * 100) if cena_pln_auto > 0 else 0

# 5. PANEL GŁÓWNY
st.markdown(f"<h1 style='text-align: center; margin-top: 50px; font-weight: 800;'>Kalkulator Handlarza</h1>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align: center; color: #666; margin-bottom: 30px;'>by Gerard S Digital Agency</p>", unsafe_allow_html=True)

col_left, col_mid, col_right = st.columns([2.5, 3, 2.5])

with col_left:
    fig_left = go.Figure(data=[go.Pie(
        labels=['Samochód', 'Akcyza', 'Pozostałe koszty', 'Przychód'],
        values=[cena_pln_auto, wartosc_akcyzy, pozostale_suma, max(0, przychod_roznica)],
        hole=.4, marker_colors=['#cc0000', '#990000', '#dddddd', '#28a745']
    )])
    fig_left.update_layout(title={'text': "Struktura wydatków", 'x': 0.5, 'xanchor': 'center'}, font=dict(family="Montserrat"), height=400, showlegend=False)
    st.plotly_chart(fig_left, use_container_width=True)

with col_mid:
    r1_1, r1_2 = st.columns(2)
    r1_1.markdown(f"<div class='metric-card'><div class='metric-label'>Przychód</div><div class='metric-value' style='color:#28a745;'>{przychod_roznica:,.2f} zł</div><div class='metric-sub'>{procent_przychod:.1f}% ROI</div></div>", unsafe_allow_html=True)
    r1_2.markdown(f"<div class='metric-card'><div class='metric-label'>Dochód</div><div class='metric-value' style='color:#28a745;'>{dochod_na_czysto:,.2f} zł</div><div class='metric-sub'>{procent_dochod:.1f}% ROI</div></div>", unsafe_allow_html=True)
    
    r2_1, r2_2, r2_3 = st.columns(3)
    r2_1.markdown(f"<div class='metric-card'><div class='metric-label'>VAT</div><div class='metric-value' style='font-size:16px;'>{vat_kwota:,.2f} zł</div></div>", unsafe_allow_html=True)
    r2_2.markdown(f"<div class='metric-card'><div class='metric-label'>Dochodowy</div><div class='metric-value' style='font-size:16px;'>{podatek_dochodowy:,.2f} zł</div></div>", unsafe_allow_html=True)
    r2_3.markdown(f"<div class='metric-card'><div class='metric-label'>Zdrowotna</div><div class='metric-value' style='font-size:16px;'>{skladka_zdrowotna:,.2f} zł</div></div>", unsafe_allow_html=True)

    st.markdown(f"<div class='metric-card'><div class='metric-label'>Inwestycja Total</div><div class='metric-value'>{suma_wydatki:,.2f} zł</div></div>", unsafe_allow_html=True)

with col_right:
    data_bars = {'Przychód': przychod_roznica, 'Dochód': dochod_na_czysto, 'VAT': vat_kwota, 'Podatek': podatek_dochodowy, 'Zdrowotna': skladka_zdrowotna}
    fig_right = go.Figure(data=[go.Bar(x=list(data_bars.keys()), y=list(data_bars.values()), marker_color=['#28a745', '#1e7e34', '#cc0000', '#990000', '#660000'])])
    fig_right.update_layout(title={'text': "Zestawienie (PLN)", 'x': 0.5, 'xanchor': 'center'}, font=dict(family="Montserrat"), height=400)
    st.plotly_chart(fig_right, use_container_width=True)

# 6. TABELE SZCZEGÓŁOWE
t1, t2 = st.columns(2)
with t1:
    st.markdown("<div class='table-header'>Wydatki - szczegóły</div>", unsafe_allow_html=True)
    st.markdown(f"""<div class='table-container'>
        <div class='row'><span>Samochód</span><span>{cena_pln_auto:,.2f} zł</span></div>
        <div class='row'><span>Akcyza</span><span>{wartosc_akcyzy:,.2f} zł</span></div>
        <div class='row'><span>Transport</span><span>{transport:,.2f} zł</span></div>
        <div class='row'><span>Lakiernik</span><span>{koszt_lakiernika:,.2f} zł</span></div>
        <div class='row'><span>Mechanik</span><span>{mechanik:,.2f} zł</span></div>
        <div class='row'><span>Części</span><span>{cena_czesci:,.2f} zł</span></div>
        <div class='total-row' style='color:#000;'><span>SUMA WYDATKÓW</span><span>{suma_wydatki:,.2f} zł</span></div>
    </div>""", unsafe_allow_html=True)

with t2:
    st.markdown("<div class='table-header'>Przychody - szczegóły</div>", unsafe_allow_html=True)
    st.markdown(f"""<div class='table-container'>
        <div class='row'><span>Przychód</span><span>{przychod_roznica:,.2f} zł</span></div>
        <div class='row'><span>Dochód (na czysto)</span><span style='color:#28a745; font-weight:bold;'>{dochod_na_czysto:,.2f} zł</span></div>
        <div class='total-row' style='color:#cc0000;'><span>Podatki razem</span><span>{podatki_razem:,.2f} zł</span></div>
    </div>""", unsafe_allow_html=True)
