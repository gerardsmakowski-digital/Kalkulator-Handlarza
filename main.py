import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Konfiguracja strony
st.set_page_config(
    page_title="Kalkulator Handlarza - Gerard S.", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CSS (ODBLOKOWANY NAGŁÓWEK + CZYSZCZENIE TEKSTU) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700&display=swap');
    * { font-family: 'Montserrat', sans-serif !important; }
    
    /* PRZYWRÓCENIE NAGŁÓWKA */
    header[data-testid="stHeader"] {
        visibility: visible !important;
        background-color: white !important;
        border-bottom: 1px solid #eee;
    }

    /* UKRYCIE SAMEGO TEKSTU W PRZYCISKU (zostawienie ikony) */
    [data-testid="stSidebarCollapsedControl"] {
        font-size: 0px !important; /* To powinno zabić napis keyboard_double... */
    }
    
    /* Stylizacja ikony SVG, żeby była widoczna */
    [data-testid="stSidebarCollapsedControl"] svg {
        fill: #000000 !important;
        width: 24px !important;
        height: 24px !important;
    }

    /* Ukrycie menu (trzy kropki) i stopki */
    #MainMenu { visibility: hidden !important; }
    footer { visibility: hidden !important; }

    /* Sidebar - tło i czcionki */
    [data-testid="stSidebar"] { background-color: #111111; color: white !important; }
    [data-testid="stSidebar"] label, [data-testid="stSidebar"] p { color: #ffffff !important; font-size: 14px !important; }
    
    /* Dashboard Cards */
    .metric-card { 
        background-color: white; padding: 15px; border-radius: 10px; 
        box-shadow: 0 4px 6px rgba(0,0,0,0.07); border: 1px solid #eee; 
        text-align: center; margin-bottom: 10px; min-height: 110px; 
        display: flex; flex-direction: column; justify-content: center; 
    }
    .metric-label { font-size: 11px; color: #666; font-weight: bold; text-transform: uppercase; letter-spacing: 0.5px; }
    .metric-value { font-size: 22px; color: #000; font-weight: 800; }
    .metric-sub { font-size: 12px; color: #28a745; font-weight: bold; }

    /* Tables */
    .table-header { background-color: #cc0000; color: white; padding: 12px; font-weight: bold; border-radius: 5px 5px 0 0; }
    .table-container { background: white; padding: 20px; border: 1px solid #eee; border-radius: 0 0 5px 5px; }
    .row { display: flex; justify-content: space-between; padding: 8px 0; border-bottom: 1px solid #f0f0f0; color: #333; }
    .total-row { display: flex; justify-content: space-between; padding-top: 12px; font-weight: bold; color: #28a745; font-size: 18px; border-top: 2px solid #eee; }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    st.markdown('<div style="margin-top: -50px;"></div>', unsafe_allow_html=True)
    st.image("logo gerard s białe .png", width=180)
    
    kurs_eur = st.number_input("Kurs Euro", value=4.27, step=0.01)
    cena_eur = st.number_input("Cena auta w EURO", value=3550.0)
    
    kwota_z_euro = cena_eur * kurs_eur
    st.markdown(f"<p style='font-size: 12px; color: #28a745; margin-top: -15px;'>Przeliczono z Euro: {kwota_z_euro:,.2f} zł</p>", unsafe_allow_html=True)
    cena_pln_auto = st.number_input("Cena auta w PLN", value=float(kwota_z_euro))

    finalna_cena_samochodu = cena_pln_auto
    cena_do_akcyzy = st.number_input("Cena auta do akcyzy", value=float(finalna_cena_samochodu))
    
    st.markdown("---")
    akcyza_opcja = st.radio("Akcyza", ["bez akcyzy", "do 2.0 l", "powyżej 2.0 l"], index=1)
    
    st.markdown("---")
    col_rej, col_prz = st.columns(2)
    with col_rej:
        rejestracja_check = st.checkbox("Rejestracja", value=True)
    with col_prz:
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
    podatek_dochodowy = (baza_po_vat - skladka_zdrowotna) * 0.19
else:
    vat_kwota = podatek_dochodowy = skladka_zdrowotna = 0

podatki_razem = vat_kwota + podatek_dochodowy + skladka_zdrowotna
dochod_na_czysto = przychod_roznica - podatki_razem 
procent_dochod = (dochod_na_czysto / finalna_cena_samochodu * 100) if finalna_cena_samochodu > 0 else 0

# --- PANEL GŁÓWNY ---
st.markdown(f"<h1 style='text-align: center; margin-top: 10px; font-weight: 800;'>Kalkulator Handlarza</h1>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align: center; color: #666; margin-bottom: 30px;'>by Gerard S Digital Agency</p>", unsafe_allow_html=True)

col_left, col_mid, col_right = st.columns([2.5, 3, 2.5])

with col_left:
    fig_left = go.Figure(data=[go.Pie(
        labels=['Auto', 'Akcyza', 'Koszty', 'Przychód'], 
        values=[finalna_cena_samochodu, wartosc_akcyzy, (suma_wydatki-finalna_cena_samochodu-wartosc_akcyzy), przychod_roznica], 
        hole=.4, marker_colors=['#cc0000', '#990000', '#dddddd', '#28a745']
    )])
    fig_left.update_layout(height=450, showlegend=False)
    st.plotly_chart(fig_left, use_container_width=True)

with col_mid:
    st.markdown(f"<div class='metric-card'><div class='metric-label'>Przychód</div><div class='metric-value' style='color:#28a745;'>{przychod_roznica:,.2f} zł</div></div>", unsafe_allow_html=True)
    st.markdown(f"<div class='metric-card'><div class='metric-label'>Dochód netto</div><div class='metric-value' style='color:#28a745;'>{dochod_na_czysto:,.2f} zł</div><div class='metric-sub'>{procent_dochod:.1f}% ROI</div></div>", unsafe_allow_html=True)
    st.markdown(f"<div class='metric-card'><div class='metric-label'>Podatki Razem</div><div class='metric-value' style='color:#cc0000;'>{podatki_razem:,.2f} zł</div></div>", unsafe_allow_html=True)

with col_right:
    fig_right = go.Figure(data=[go.Bar(
        x=['Przychód', 'Dochód', 'VAT', 'Podatek'], 
        y=[przychod_roznica, dochod_na_czysto, vat_kwota, podatek_dochodowy],
        marker_color=['#28a745', '#1e7e34', '#cc0000', '#990000']
    )])
    fig_right.update_layout(height=450)
    st.plotly_chart(fig_right, use_container_width=True)

st.markdown("<br>", unsafe_allow_html=True)

# --- TABELE ---
t1, t2 = st.columns(2)
with t1:
    st.markdown("<div class='table-header'>Wydatki</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='table-container'><div class='total-row' style='color:black;'><span>SUMA</span><span>{suma_wydatki:,.2f} zł</span></div></div>", unsafe_allow_html=True)

with t2:
    st.markdown("<div class='table-header'>Podatki</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='table-container'><div class='total-row' style='color:#cc0000;'><span>SUMA</span><span>{podatki_razem:,.2f} zł</span></div></div>", unsafe_allow_html=True)
