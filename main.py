import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# 1. Konfiguracja strony - Sidebar na stałe otwarty (zdejmujemy problem strzałki)
st.set_page_config(
    page_title="Kalkulator Handlarza - Gerard S.", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. CSS - Minimalistyczny i stabilny
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700&display=swap');
    
    /* Globalne czcionki */
    html, body, [class*="st-"] {
        font-family: 'Montserrat', sans-serif !important;
    }

    /* Usuwamy TYLKO logo Streamlit i stopkę. Header zostawiamy standardowy, żeby nie psuć kodu */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Sidebar - Ciemny motyw */
    [data-testid="stSidebar"] {
        background-color: #111111;
        color: white;
    }
    [data-testid="stSidebar"] .stMarkdown p, [data-testid="stSidebar"] label {
        color: white !important;
    }

    /* Karty wyników (Dashboard) */
    .metric-card { 
        background-color: white; 
        padding: 20px; 
        border-radius: 12px; 
        box-shadow: 0 4px 12px rgba(0,0,0,0.1); 
        text-align: center; 
        margin-bottom: 15px;
    }
    .metric-label { font-size: 12px; color: #888; font-weight: bold; text-transform: uppercase; }
    .metric-value { font-size: 24px; color: #000; font-weight: 800; margin: 5px 0; }
    .metric-sub { font-size: 14px; color: #28a745; font-weight: bold; }

    /* Tabele */
    .table-header { background-color: #cc0000; color: white; padding: 12px; font-weight: bold; border-radius: 8px 8px 0 0; }
    .table-container { background: white; padding: 15px; border: 1px solid #eee; border-radius: 0 0 8px 8px; margin-bottom: 20px; }
    .row { display: flex; justify-content: space-between; padding: 10px 0; border-bottom: 1px solid #f9f9f9; color: #333; }
    .total-row { display: flex; justify-content: space-between; padding-top: 15px; font-weight: bold; border-top: 2px solid #eee; font-size: 18px; }
    </style>
    """, unsafe_allow_html=True)

# 3. DANE WEJŚCIOWE (SIDEBAR)
with st.sidebar:
    st.image("https://via.placeholder.com/180x60.png?text=LOGO+GERARD+S", width=180) # Tu wstaw ścieżkę do swojego logo
    st.markdown("### Konfiguracja")
    
    kurs_eur = st.number_input("Kurs Euro", value=4.27)
    cena_eur = st.number_input("Cena auta w EURO", value=3550.0)
    cena_pln_auto = st.number_input("Cena auta w PLN", value=float(cena_eur * kurs_eur))
    
    st.divider()
    akcyza_opcja = st.selectbox("Akcyza", ["do 2.0 l", "powyżej 2.0 l", "bez akcyzy"])
    
    col1, col2 = st.columns(2)
    with col1:
        rejestracja = st.checkbox("Rejestracja", value=True)
    with col2:
        gaz = st.checkbox("LPG", value=False)

    st.divider()
    transport = st.number_input("Transport", value=1700)
    mechanik = st.number_input("Mechanik + Części", value=1000)
    lakier = st.number_input("Lakiernik", value=0)
    inne = st.number_input("Inne koszty", value=500)
    
    st.divider()
    cena_sprzedazy = st.number_input("CENA SPRZEDAŻY", value=25000)

# 4. LOGIKA OBLICZEŃ
stawka_akc = 0.031 if akcyza_opcja == "do 2.0 l" else (0.186 if akcyza_opcja == "powyżej 2.0 l" else 0)
wartosc_akcyzy = cena_pln_auto * stawka_akc
koszt_rej = 162 if rejestracja else 0
koszt_prz = 245 if gaz else 150

suma_wydatki = cena_pln_auto + wartosc_akcyzy + transport + mechanik + lakier + inne + koszt_rej + koszt_prz
przychod_brutto = cena_sprzedazy - suma_wydatki

if przychod_brutto > 0:
    vat = przychod_brutto * (0.23 / 1.23)
    baza_opodatkowania = przychod_brutto - vat
    zdrowotna = baza_opodatkowania * 0.049
    podatek_dochodowy = (baza_opodatkowania - zdrowotna) * 0.19
else:
    vat = zdrowotna = podatek_dochodowy = 0

podatki_suma = vat + zdrowotna + podatek_dochodowy
dochod_netto = przychod_brutto - podatki_suma
roi = (dochod_netto / cena_pln_auto * 100) if cena_pln_auto > 0 else 0

# 5. WIDOK GŁÓWNY
st.title("Kalkulator Handlarza")
st.caption("by Gerard S Digital Agency")

# Dashboard - Metryki
m1, m2, m3, m4 = st.columns(4)
with m1:
    st.markdown(f"<div class='metric-card'><div class='metric-label'>Przychód</div><div class='metric-value' style='color:#28a745;'>{przychod_brutto:,.2f} zł</div></div>", unsafe_allow_html=True)
with m2:
    st.markdown(f"<div class='metric-card'><div class='metric-label'>Dochód (na czysto)</div><div class='metric-value' style='color:#28a745;'>{dochod_netto:,.2f} zł</div></div>", unsafe_allow_html=True)
with m3:
    st.markdown(f"<div class='metric-card'><div class='metric-label'>ROI</div><div class='metric-value'>{roi:.1f}%</div></div>", unsafe_allow_html=True)
with m4:
    st.markdown(f"<div class='metric-card'><div class='metric-label'>Podatki Razem</div><div class='metric-value' style='color:#cc0000;'>{podatki_suma:,.2f} zł</div></div>", unsafe_allow_html=True)

# Wykresy
c1, c2 = st.columns(2)
with c1:
    fig_pie = go.Figure(data=[go.Pie(
        labels=['Auto', 'Akcyza', 'Koszty', 'Zysk'],
        values=[cena_pln_auto, wartosc_akcyzy, (suma_wydatki-cena_pln_auto-wartosc_akcyzy), dochod_netto],
        hole=.4,
        marker_colors=['#cc0000', '#800000', '#dddddd', '#28a745']
    )])
    fig_pie.update_layout(title="Struktura Inwestycji", height=400)
    st.plotly_chart(fig_pie, use_container_width=True)

with c2:
    fig_bar = go.Figure(data=[go.Bar(
        x=['Przychód', 'Dochód', 'VAT', 'Podatek'],
        y=[przychod_brutto, dochod_netto, vat, podatek_dochodowy],
        marker_color=['#28a745', '#1e7e34', '#cc0000', '#990000']
    )])
    fig_bar.update_layout(title="Wynik finansowy", height=400)
    st.plotly_chart(fig_bar, use_container_width=True)

# Tabele szczegółowe
t1, t2 = st.columns(2)
with t1:
    st.markdown("<div class='table-header'>Wydatki (Koszty)</div>", unsafe_allow_html=True)
    st.markdown(f"""<div class='table-container'>
        <div class='row'><span>Cena auta</span><span>{cena_pln_auto:,.2f} zł</span></div>
        <div class='row'><span>Akcyza</span><span>{wartosc_akcyzy:,.2f} zł</span></div>
        <div class='row'><span>Naprawy i Transport</span><span>{mechanik+transport+lakier:,.2f} zł</span></div>
        <div class='total-row'><span>SUMA WYDATKÓW</span><span>{suma_wydatki:,.2f} zł</span></div>
    </div>""", unsafe_allow_html=True)

with t2:
    st.markdown("<div class='table-header'>Przychody i Dochód</div>", unsafe_allow_html=True)
    st.markdown(f"""<div class='table-container'>
        <div class='row'><span>Przychód</span><span>{przychod_brutto:,.2f} zł</span></div>
        <div class='row'><span>Dochód netto</span><span style='color:#28a745;'>{dochod_netto:,.2f} zł</span></div>
        <div class='row'><span>Suma podatków</span><span style='color:#cc0000;'>{podatki_suma:,.2f} zł</span></div>
        <div class='total-row'><span>CENA SPRZEDAŻY</span><span>{cena_sprzedazy:,.2f} zł</span></div>
    </div>""", unsafe_allow_html=True)
