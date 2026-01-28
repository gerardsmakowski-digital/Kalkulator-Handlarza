import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Konfiguracja strony
st.set_page_config(
    page_title="Kalkulator Handlarza - Gerard S.", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CSS (NAPRAWA SIDEBARU PRZEZ TRANSPARENTNOŚĆ) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700&display=swap');
    * { font-family: 'Montserrat', sans-serif !important; }
    
    /* Zamiast ukrywać header (visibility: hidden), robimy go przezroczystym */
    header[data-testid="stHeader"] {
        background: rgba(0,0,0,0) !important;
        color: rgba(0,0,0,0) !important;
    }

    /* Stylizacja samej strzałki (przycisku) */
    [data-testid="stSidebarCollapsedControl"] {
        background-color: #111111 !important; /* Ciemne tło przycisku */
        color: white !important;               /* Biała strzałka */
        border-radius: 0 10px 10px 0 !important;
        top: 10px !important;
        left: 0px !important;
        padding: 5px !important;
    }

    /* Ukrycie menu Streamlit (kropki po prawej) */
    #MainMenu { visibility: hidden; }
    footer { visibility: hidden; }

    /* Reszta Twojej stylizacji Montserrat */
    [data-testid="stSidebar"] { background-color: #111111; color: white !important; }
    [data-testid="stSidebar"] label, [data-testid="stSidebar"] p { color: #ffffff !important; font-size: 14px !important; }
    
    .metric-card { 
        background-color: white; padding: 15px; border-radius: 10px; 
        box-shadow: 0 4px 6px rgba(0,0,0,0.07); border: 1px solid #eee; 
        text-align: center; margin-bottom: 10px; min-height: 110px; 
        display: flex; flex-direction: column; justify-content: center; 
    }
    .metric-label { font-size: 11px; color: #666; font-weight: bold; text-transform: uppercase; }
    .metric-value { font-size: 22px; color: #000; font-weight: 800; }

    .table-header { background-color: #cc0000; color: white; padding: 12px; font-weight: bold; border-radius: 5px 5px 0 0; }
    .table-container { background: white; padding: 20px; border: 1px solid #eee; border-radius: 0 0 5px 5px; }
    .row { display: flex; justify-content: space-between; padding: 8px 0; border-bottom: 1px solid #f0f0f0; }
    .total-row { display: flex; justify-content: space-between; padding-top: 12px; font-weight: bold; color: #28a745; border-top: 2px solid #eee; }
    </style>
    """, unsafe_allow_html=True)

# --- DANE I OBLICZENIA (Te same co wcześniej) ---
with st.sidebar:
    st.markdown('<div style="margin-top: -50px;"></div>', unsafe_allow_html=True)
    st.image("logo gerard s białe .png", width=180)
    
    kurs_eur = st.number_input("Kurs Euro", value=4.27, step=0.01)
    cena_eur = st.number_input("Cena auta w EURO", value=3550.0)
    cena_pln_auto = st.number_input("Cena auta w PLN", value=float(cena_eur * kurs_eur))
    cena_do_akcyzy = st.number_input("Cena auta do akcyzy", value=float(cena_pln_auto))
    
    st.markdown("---")
    akcyza_opcja = st.radio("Stawka", ["bez akcyzy", "do 2.0 l", "powyżej 2.0 l"], index=1)
    
    col_rej, col_prz = st.columns(2)
    with col_rej:
        rejestracja_check = st.checkbox("Rejestracja", value=True)
    with col_prz:
        przeglad_opcja = st.radio("Przegląd", ["bez gazu", "z gazem"], index=0)
    
    st.markdown("---")
    transport = st.number_input("Transport", value=1700)
    lakier = st.number_input("Lakier", value=0)
    czesci = st.number_input("Części", value=300)
    mechanik = st.number_input("Mechanik", value=700)
    inne = st.number_input("Pozostałe koszty", value=700)
    
    st.markdown("---")
    cena_sprzedazy = st.number_input("CENA SPRZEDAŻY", value=25000)

# Obliczenia
stawka_akc = 0.031 if akcyza_opcja == "do 2.0 l" else (0.186 if akcyza_opcja == "powyżej 2.0 l" else 0)
wartosc_akcyzy = cena_do_akcyzy * stawka_akc
koszt_rej = 162 if rejestracja_check else 0
koszt_prz = 150 if przeglad_opcja == "bez gazu" else 245
suma_wydatki = cena_pln_auto + wartosc_akcyzy + transport + lakier + czesci + mechanik + inne + koszt_rej + koszt_prz
przychod = cena_sprzedazy - suma_wydatki

if przychod > 0:
    vat = przychod * (0.23 / 1.23)
    baza = przychod - vat
    zdrowotna = baza * 0.049
    podatek = (baza - zdrowotna) * 0.19
else:
    vat = podatek = zdrowotna = 0

podatki_suma = vat + podatek + zdrowotna
dochod = przychod - podatki_suma

# --- PANEL GŁÓWNY ---
st.markdown(f"<h1 style='text-align: center; margin-top: -20px; font-weight: 800;'>Kalkulator Handlarza</h1>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align: center; color: #666; margin-bottom: 30px;'>by Gerard S Digital Agency</p>", unsafe_allow_html=True)

c1, c2, c3 = st.columns([2.5, 3, 2.5])

with c1:
    fig_pie = go.Figure(data=[go.Pie(
        labels=['Auto', 'Akcyza', 'Koszty', 'Przychód'],
        values=[cena_pln_auto, wartosc_akcyzy, (suma_wydatki-cena_pln_auto-wartosc_akcyzy), przychod],
        hole=.4, marker_colors=['#cc0000', '#990000', '#dddddd', '#28a745'],
        textinfo='percent+label'
    )])
    fig_pie.update_layout(height=480, margin=dict(t=50, b=80, l=10, r=10), showlegend=False)
    st.plotly_chart(fig_pie, use_container_width=True)

with c2:
    st.markdown(f"<div class='metric-card'><div class='metric-label'>Przychód</div><div class='metric-value' style='color:#28a745;'>{przychod:,.2f} zł</div></div>", unsafe_allow_html=True)
    st.markdown(f"<div class='metric-card'><div class='metric-label'>Dochód</div><div class='metric-value' style='color:#28a745;'>{dochod:,.2f} zł</div></div>", unsafe_allow_html=True)

with c3:
    fig_bar = go.Figure(data=[go.Bar(
        x=['Przychód', 'Dochód', 'VAT', 'Podatek'],
        y=[przychod, dochod, vat, podatek],
        marker_color=['#28a745', '#1e7e34', '#cc0000', '#990000']
    )])
    fig_bar.update_layout(height=480, margin=dict(t=50, b=80, l=10, r=10))
    st.plotly_chart(fig_bar, use_container_width=True)

st.markdown("<br>", unsafe_allow_html=True)

# TABELE (Przychód i Dochód)
t1, t2 = st.columns(2)
with t1:
    st.markdown("<div class='table-header'>Wydatki</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='table-container'><div class='row'><span>Auto</span><span>{cena_pln_auto:,.2f} zł</span></div><div class='row'><span>Akcyza</span><span>{wartosc_akcyzy:,.2f} zł</span></div><div class='total-row'><span>SUMA</span><span>{suma_wydatki:,.2f} zł</span></div></div>", unsafe_allow_html=True)

with t2:
    st.markdown("<div class='table-header'>Przychody</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='table-container'><div class='row'><span>Przychód</span><span>{przychod:,.2f} zł</span></div><div class='row'><span>Dochód</span><span>{dochod:,.2f} zł</span></div><div class='total-row' style='color:#cc0000;'><span>Podatki</span><span>{podatki_suma:,.2f} zł</span></div></div>", unsafe_allow_html=True)
