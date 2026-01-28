import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Ustawienia strony - wymuszamy rozwinięty sidebar
st.set_page_config(
    page_title="Kalkulator Handlarza - Gerard S.", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CSS (Stylizacja Montserrat + Fixy UI) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700&display=swap');
    * { font-family: 'Montserrat', sans-serif !important; }
    
    /* Ukrywamy standardowe menu, ale zostawiamy header dla przycisku sidebaru */
    footer, #MainMenu { visibility: hidden !important; }
    header { background-color: rgba(0,0,0,0) !important; }

    /* Fix dla przycisku sidebaru (strzałki), żeby był widoczny na białym tle */
    .st-emotion-cache-hp089u { color: #111111 !important; }

    /* Sidebar Stylizacja */
    [data-testid="stSidebar"] { background-color: #111111; color: white !important; min-width: 300px !important; }
    [data-testid="stSidebar"] label, [data-testid="stSidebar"] p { color: #ffffff !important; font-size: 14px !important; }
    
    /* Karty Wyników */
    .metric-card { 
        background-color: white; padding: 15px; border-radius: 10px; 
        box-shadow: 0 4px 6px rgba(0,0,0,0.07); border: 1px solid #eee; 
        text-align: center; margin-bottom: 10px; min-height: 110px; 
        display: flex; flex-direction: column; justify-content: center; 
    }
    .metric-label { font-size: 11px; color: #666; font-weight: bold; text-transform: uppercase; }
    .metric-value { font-size: 22px; color: #000; font-weight: 800; margin: 2px 0; }

    /* Tabele */
    .table-header { background-color: #cc0000; color: white; padding: 12px; font-weight: bold; border-radius: 5px 5px 0 0; }
    .table-container { background: white; padding: 20px; border: 1px solid #eee; border-radius: 0 0 5px 5px; margin-bottom: 20px; }
    .row { display: flex; justify-content: space-between; padding: 8px 0; border-bottom: 1px solid #f0f0f0; color: #333; }
    .total-row { display: flex; justify-content: space-between; padding-top: 12px; font-weight: bold; border-top: 2px solid #eee; }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR (Dane wejściowe) ---
with st.sidebar:
    st.image("logo gerard s białe .png", width=180)
    st.markdown("<br>", unsafe_allow_html=True)
    
    kurs_eur = st.number_input("Kurs Euro", value=4.27, step=0.01)
    cena_eur = st.number_input("Cena auta w EURO", value=3550.0)
    cena_pln_auto = st.number_input("Cena auta w PLN", value=float(cena_eur * kurs_eur))
    cena_do_akcyzy = st.number_input("Cena auta do akcyzy", value=cena_pln_auto)
    
    st.markdown("---")
    akcyza_opcja = st.radio("Akcyza", ["bez akcyzy", "do 2.0 l", "powyżej 2.0 l"], index=1)
    
    col_rej, col_prz = st.columns(2)
    with col_rej:
        rejestracja_check = st.checkbox("Rejestracja", value=True)
    with col_prz:
        przeglad_opcja = st.radio("Przegląd", ["bez gazu", "z gazem"], index=0)
    
    st.markdown("---")
    transport = st.number_input("Transport", value=1700)
    lakier = st.number_input("Lakier (suma)", value=0)
    czesci = st.number_input("Części", value=300)
    mechanik = st.number_input("Mechanik", value=700)
    inne = st.number_input("Inne (myjnia, ogłoszenia itp.)", value=700)
    
    st.markdown("---")
    cena_sprzedazy = st.number_input("CENA SPRZEDAŻY", value=25000)

# --- OBLICZENIA ---
stawka_akc = 0.031 if akcyza_opcja == "do 2.0 l" else (0.186 if akcyza_opcja == "powyżej 2.0 l" else 0)
wartosc_akcyzy = cena_do_akcyzy * stawka_akc
koszt_rej = 162 if rejestracja_check else 0
koszt_prz = 150 if przeglad_opcja == "bez gazu" else 245

suma_wydatki = cena_pln_auto + wartosc_akcyzy + transport + lakier + czesci + mechanik + inne + koszt_rej + koszt_prz
przychod_brutto = cena_sprzedazy - suma_wydatki

if przychod_brutto > 0:
    vat_kwota = przychod_brutto * (0.23 / 1.23)
    baza_po_vat = przychod_brutto - vat_kwota
    zdrowotna = baza_po_vat * 0.049
    dochodowy = (baza_po_vat - zdrowotna) * 0.19
else:
    vat_kwota = dochodowy = zdrowotna = 0

podatki_razem = vat_kwota + dochodowy + zdrowotna
dochod_netto = przychod_brutto - podatki_razem
roi = (dochod_netto / cena_pln_auto * 100) if cena_pln_auto > 0 else 0

# --- UKŁAD GRAFICZNY ---
st.markdown("<h1 style='text-align: center; font-weight: 800;'>Kalkulator Handlarza</h1>", unsafe_allow_html=True)

col_chart_l, col_metrics, col_chart_r = st.columns([2.5, 3, 2.5])

with col_chart_l:
    # Wykres kołowy (Struktura)
    fig_pie = go.Figure(data=[go.Pie(
        labels=['Samochód', 'Akcyza', 'Koszty', 'Przychód'],
        values=[cena_pln_auto, wartosc_akcyzy, (suma_wydatki - cena_pln_auto - wartosc_akcyzy), przychod_brutto],
        hole=.4,
        marker_colors=['#cc0000', '#800000', '#dddddd', '#28a745'],
        textinfo='percent+label'
    )])
    fig_pie.update_layout(
        title="Struktura ceny", 
        height=450, 
        margin=dict(t=50, b=100, l=10, r=10), # Zwiększony margines dolny (b=100)
        showlegend=False
    )
    st.plotly_chart(fig_pie, use_container_width=True)

with col_metrics:
    m1, m2 = st.columns(2)
    m1.markdown(f"<div class='metric-card'><div class='metric-label'>Przychód</div><div class='metric-value' style='color:#28a745;'>{przychod_brutto:,.2f} zł</div></div>", unsafe_allow_html=True)
    m2.markdown(f"<div class='metric-card'><div class='metric-label'>Dochód</div><div class='metric-value' style='color:#28a745;'>{dochod_netto:,.2f} zł</div><div style='color:#28a745; font-weight:bold;'>{roi:.1f}% ROI</div></div>", unsafe_allow_html=True)
    
    m3, m4, m5 = st.columns(3)
    m3.markdown(f"<div class='metric-card'><div class='metric-label'>VAT</div><div class='metric-value' style='font-size:16px;'>{vat_kwota:,.2f} zł</div></div>", unsafe_allow_html=True)
    m4.markdown(f"<div class='metric-card'><div class='metric-label'>Podatek</div><div class='metric-value' style='font-size:16px;'>{dochodowy:,.2f} zł</div></div>", unsafe_allow_html=True)
    m5.markdown(f"<div class='metric-card'><div class='metric-label'>Zdrowotna</div><div class='metric-value' style='font-size:16px;'>{zdrowotna:,.2f} zł</div></div>", unsafe_allow_html=True)

    m6, m7 = st.columns(2)
    m6.markdown(f"<div class='metric-card'><div class='metric-label'>Inwestycja</div><div class='metric-value' style='font-size:18px;'>{suma_wydatki:,.2f} zł</div></div>", unsafe_allow_html=True)
    m7.markdown(f"<div class='metric-card'><div class='metric-label'>Podatki Razem</div><div class='metric-value' style='color:#cc0000; font-size:18px;'>{podatki_razem:,.2f} zł</div></div>", unsafe_allow_html=True)

with col_chart_r:
    # Wykres słupkowy (Wynik)
    fig_bar = go.Figure(data=[go.Bar(
        x=['Przychód', 'Dochód', 'VAT', 'Podatek', 'Zdrowotna'],
        y=[przychod_brutto, dochod_netto, vat_kwota, dochodowy, zdrowotna],
        marker_color=['#28a745', '#1e7e34', '#cc0000', '#990000', '#660000']
    )])
    fig_bar.update_layout(title="Wynik finansowy", height=450, margin=dict(t=50, b=100, l=10, r=10))
    st.plotly_chart(fig_bar, use_container_width=True)

# --- TABELE SZCZEGÓŁOWE ---
t1, t2 = st.columns(2)
with t1:
    st.markdown("<div class='table-header'>Wydatki - szczegóły</div>", unsafe_allow_html=True)
    st.markdown(f"""<div class='table-container'>
        <div class='row'><span>Samochód</span><span>{cena_pln_auto:,.2f} zł</span></div>
        <div class='row'><span>Akcyza</span><span>{wartosc_akcyzy:,.2f} zł</span></div>
        <div class='row'><span>Transport / Lakier</span><span>{transport + lakier:,.2f} zł</span></div>
        <div class='row'><span>Mechanik / Części</span><span>{mechanik + czesci:,.2f} zł</span></div>
        <div class='row'><span>Pozostałe koszty</span><span>{inne + koszt_rej + koszt_prz:,.2f} zł</span></div>
        <div class='total-row'><span>SUMA WYDATKÓW</span><span>{suma_wydatki:,.2f} zł</span></div>
    </div>""", unsafe_allow_html=True)

with t2:
    st.markdown("<div class='table-header'>Przychody - szczegóły</div>", unsafe_allow_html=True)
    st.markdown(f"""<div class='table-container'>
        <div class='row'><span>Przychód</span><span>{przychod_brutto:,.2f} zł</span></div>
        <div class='row'><span>Dochód</span><span style='color:#28a745; font-weight:bold;'>{dochod_netto:,.2f} zł</span></div>
        <div class='row'><span>VAT (23%)</span><span>{vat_kwota:,.2f} zł</span></div>
        <div class='row'><span>Podatek dochodowy</span><span>{dochodowy:,.2f} zł</span></div>
        <div class='row'><span>Składka zdrowotna</span><span>{zdrowotna:,.2f} zł</span></div>
        <div class='total-row' style='color:#cc0000;'><span>Podatki razem</span><span>{podatki_razem:,.2f} zł</span></div>
    </div>""", unsafe_allow_html=True)
