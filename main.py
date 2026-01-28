import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# 1. Konfiguracja strony
st.set_page_config(
    page_title="Kalkulator Handlarza - Gerard S.", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. CSS - ROZWIĄZANIE PROBLEMU NAPISU I STYLIZACJA
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700&display=swap');
    * { font-family: 'Montserrat', sans-serif !important; }
    
    /* ODBLOKOWANY NAGŁÓWEK - biały i czysty */
    header[data-testid="stHeader"] {
        visibility: visible !important;
        background-color: white !important;
        border-bottom: 1px solid #f0f0f0;
    }

    /* ELIMINACJA NAPISU 'keyboard...' I WSTAWIENIE IKONY */
    /* Wywalamy tekst poza ekran */
    [data-testid="stSidebarCollapsedControl"] {
        text-indent: -9999px !important;
        overflow: hidden !important;
        width: 45px !important;
        height: 45px !important;
        background-color: #f8f9fa !important;
        border-radius: 50% !important;
        margin: 5px !important;
        position: relative !important;
    }

    /* Wstawiamy własny symbol strzałki w puste miejsce */
    [data-testid="stSidebarCollapsedControl"]::after {
        content: '❯' !important;
        text-indent: 0px !important;
        position: absolute !important;
        left: 50% !important;
        top: 50% !important;
        transform: translate(-50%, -50%) !important;
        font-size: 18px !important;
        color: #111111 !important;
        font-weight: bold !important;
        visibility: visible !important;
    }

    /* Ukrywamy oryginalny wadliwy symbol SVG */
    [data-testid="stSidebarCollapsedControl"] svg {
        display: none !important;
    }

    /* Ukrycie menu Streamlit i stopki */
    #MainMenu { visibility: hidden !important; }
    footer { visibility: hidden !important; }

    /* Sidebar - Stylizacja */
    [data-testid="stSidebar"] { background-color: #111111; color: white !important; }
    [data-testid="stSidebar"] label, [data-testid="stSidebar"] p { color: #ffffff !important; font-size: 14px !important; }
    [data-testid="stSidebar"] hr { border-top: 1px solid rgba(255, 255, 255, 0.2) !important; }
    
    /* Dashboard - Karty */
    .metric-card { 
        background-color: white; padding: 20px; border-radius: 12px; 
        box-shadow: 0 4px 6px rgba(0,0,0,0.05); border: 1px solid #eee; 
        text-align: center; margin-bottom: 15px; min-height: 120px;
        display: flex; flex-direction: column; justify-content: center;
    }
    .metric-label { font-size: 11px; color: #888; font-weight: bold; text-transform: uppercase; letter-spacing: 0.5px; }
    .metric-value { font-size: 24px; color: #000; font-weight: 800; margin: 5px 0; }
    .metric-sub { font-size: 13px; color: #28a745; font-weight: bold; }

    /* Tabele */
    .table-header { background-color: #cc0000; color: white; padding: 12px; font-weight: bold; border-radius: 8px 8px 0 0; }
    .table-container { background: white; padding: 20px; border: 1px solid #eee; border-radius: 0 0 8px 8px; margin-bottom: 20px; }
    .row { display: flex; justify-content: space-between; padding: 10px 0; border-bottom: 1px solid #f9f9f9; color: #333; }
    .total-row { display: flex; justify-content: space-between; padding-top: 15px; font-weight: bold; border-top: 2px solid #eee; font-size: 18px; }
    </style>
    """, unsafe_allow_html=True)

# 3. SIDEBAR - WPROWADZANIE DANYCH
with st.sidebar:
    st.markdown('<div style="margin-top: -50px;"></div>', unsafe_allow_html=True)
    # Upewnij się, że logo jest w tym samym folderze co skrypt
    try:
        st.image("logo gerard s białe .png", width=180)
    except:
        st.markdown("### GERARD S DIGITAL AGENCY")
    
    st.markdown("---")
    kurs_eur = st.number_input("Kurs Euro", value=4.27, step=0.01)
    cena_eur = st.number_input("Cena auta w EURO", value=3550.0)
    
    kwota_z_euro = cena_eur * kurs_eur
    st.markdown(f"<p style='font-size: 12px; color: #28a745; margin-top: -15px;'>Przeliczono: {kwota_z_euro:,.2f} zł</p>", unsafe_allow_html=True)
    
    cena_pln_auto = st.number_input("Cena auta w PLN", value=float(kwota_z_euro))
    cena_do_akcyzy = st.number_input("Cena do akcyzy", value=float(cena_pln_auto))
    
    st.markdown("---")
    akcyza_opcja = st.radio("Stawka akcyzy", ["do 2.0 l", "powyżej 2.0 l", "bez akcyzy"], index=0)
    
    col_rej, col_prz = st.columns(2)
    with col_rej:
        rejestracja_check = st.checkbox("Rejestracja", value=True)
    with col_prz:
        gaz_check = st.checkbox("LPG / Gaz", value=False)
    
    st.markdown("---")
    transport = st.number_input("Transport", value=1700)
    mechanik = st.number_input("Mechanik + Części", value=1000)
    lakiernik = st.number_input("Lakiernik", value=0)
    myjnia_inne = st.number_input("Myjnia i inne", value=400)
    
    st.markdown("---")
    cena_sprzedazy = st.number_input("CENA SPRZEDAŻY", value=25000)

# 4. LOGIKA OBLICZEŃ
stawka_akc = 0.031 if akcyza_opcja == "do 2.0 l" else (0.186 if akcyza_opcja == "powyżej 2.0 l" else 0)
wartosc_akcyzy = cena_do_akcyzy * stawka_akc
koszt_rej = 162 if rejestracja_check else 0
koszt_prz = 245 if gaz_check else 150

suma_wydatki = cena_pln_auto + wartosc_akcyzy + transport + mechanik + lakiernik + myjnia_inne + koszt_rej + koszt_prz
przychod_brutto = cena_sprzedazy - suma_wydatki

if przychod_brutto > 0:
    vat_marza = przychod_brutto * (0.23 / 1.23)
    baza_dochodu = przychod_brutto - vat_marza
    zdrowotna = baza_dochodu * 0.049
    podatek_dochodowy = (baza_dochodu - zdrowotna) * 0.19
else:
    vat_marza = zdrowotna = podatek_dochodowy = 0

podatki_suma = vat_marza + zdrowotna + podatek_dochodowy
dochod_netto = przychod_brutto - podatki_suma
roi = (dochod_netto / cena_pln_auto * 100) if cena_pln_auto > 0 else 0

# 5. PANEL GŁÓWNY
st.markdown(f"<h1 style='text-align: center; margin-top: -10px; font-weight: 800;'>Kalkulator Handlarza</h1>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align: center; color: #666; margin-bottom: 30px;'>by Gerard S Digital Agency</p>", unsafe_allow_html=True)

# Dashboard Metryki
m1, m2, m3, m4 = st.columns(4)
with m1:
    st.markdown(f"<div class='metric-card'><div class='metric-label'>Inwestycja</div><div class='metric-value'>{suma_wydatki:,.2f} zł</div></div>", unsafe_allow_html=True)
with m2:
    st.markdown(f"<div class='metric-card'><div class='metric-label'>Przychód</div><div class='metric-value' style='color:#28a745;'>{przychod_brutto:,.2f} zł</div></div>", unsafe_allow_html=True)
with m3:
    st.markdown(f"<div class='metric-card'><div class='metric-label'>Dochód Netto</div><div class='metric-value' style='color:#28a745;'>{dochod_netto:,.2f} zł</div><div class='metric-sub'>{roi:.1f}% ROI</div></div>", unsafe_allow_html=True)
with m4:
    st.markdown(f"<div class='metric-card'><div class='metric-label'>Podatki Razem</div><div class='metric-value' style='color:#cc0000;'>{podatki_suma:,.2f} zł</div></div>", unsafe_allow_html=True)

# Wykresy
c1, c2 = st.columns(2)
with c1:
    fig_pie = go.Figure(data=[go.Pie(
        labels=['Auto', 'Akcyza', 'Koszty', 'Zysk'],
        values=[cena_pln_auto, wartosc_akcyzy, (suma_wydatki-cena_pln_auto-wartosc_akcyzy), dochod_netto],
        hole=.4, marker_colors=['#cc0000', '#990000', '#dddddd', '#28a745']
    )])
    fig_pie.update_layout(title="Struktura kosztów", height=400, showlegend=True)
    st.plotly_chart(fig_pie, use_container_width=True)

with c2:
    fig_bar = go.Figure(data=[go.Bar(
        x=['Przychód', 'Dochód', 'VAT', 'Podatek'],
        y=[przychod_brutto, dochod_netto, vat_marza, podatek_dochodowy],
        marker_color=['#28a745', '#1e7e34', '#cc0000', '#990000']
    )])
    fig_bar.update_layout(title="Wynik finansowy", height=400)
    st.plotly_chart(fig_bar, use_container_width=True)

# Tabele
t1, t2 = st.columns(2)
with t1:
    st.markdown("<div class='table-header'>Szczegóły Wydatków</div>", unsafe_allow_html=True)
    st.markdown(f"""<div class='table-container'>
        <div class='row'><span>Samochód</span><span>{cena_pln_auto:,.2f} zł</span></div>
        <div class='row'><span>Akcyza</span><span>{wartosc_akcyzy:,.2f} zł</span></div>
        <div class='row'><span>Naprawy / Mechanik</span><span>{mechanik+lakiernik:,.2f} zł</span></div>
        <div class='row'><span>Transport</span><span>{transport:,.2f} zł</span></div>
        <div class='total-row'><span>SUMA</span><span>{suma_wydatki:,.2f} zł</span></div>
    </div>""", unsafe_allow_html=True)

with t2:
    st.markdown("<div class='table-header'>Podatki i Dochód</div>", unsafe_allow_html=True)
    st.markdown(f"""<div class='table-container'>
        <div class='row'><span>VAT (marża)</span><span>{vat_marza:,.2f} zł</span></div>
        <div class='row'><span>Podatek Dochodowy</span><span>{podatek_dochodowy:,.2f} zł</span></div>
        <div class='row'><span>Składka Zdrowotna</span><span>{zdrowotna:,.2f} zł</span></div>
        <div class='total-row' style='color:#28a745;'><span>DOCHÓD NA CZYSTO</span><span>{dochod_netto:,.2f} zł</span></div>
    </div>""", unsafe_allow_html=True)
