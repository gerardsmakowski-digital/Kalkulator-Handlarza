import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Konfiguracja strony
st.set_page_config(page_title="Kalkulator Handlarza - Gerard S.", layout="wide")

# --- CSS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700&display=swap');
    * { font-family: 'Montserrat', sans-serif !important; }
    header, footer, #MainMenu { visibility: hidden !important; }
    [data-testid="stSidebar"] { background-color: #111111; color: white !important; }
    [data-testid="stSidebar"] label, [data-testid="stSidebar"] p { color: #ffffff !important; font-size: 14px !important; }
    [data-testid="stSidebar"] hr { margin: 15px 0 !important; border-top: 1px solid rgba(255, 255, 255, 0.2) !important; }
    
    .metric-card { 
        background-color: white; padding: 15px; border-radius: 10px; 
        box-shadow: 0 4px 6px rgba(0,0,0,0.07); border: 1px solid #eee; 
        text-align: center; margin-bottom: 10px; min-height: 110px; 
        display: flex; flex-direction: column; justify-content: center; 
    }
    .metric-label { font-size: 11px; color: #666; font-weight: bold; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 4px; }
    .metric-value { font-size: 22px; color: #000; font-weight: 800; margin: 2px 0; }
    .metric-sub { font-size: 12px; color: #28a745; font-weight: bold; }
    
    .table-header { background-color: #cc0000; color: white; padding: 12px; font-weight: bold; border-radius: 5px 5px 0 0; font-size: 16px; }
    .table-container { background: white; padding: 20px; border: 1px solid #eee; border-radius: 0 0 5px 5px; margin-bottom: 20px; }
    .row { display: flex; justify-content: space-between; padding: 8px 0; border-bottom: 1px solid #f0f0f0; color: #333; font-size: 15px; }
    .total-row { display: flex; justify-content: space-between; padding-top: 12px; font-weight: bold; color: #000; font-size: 18px; border-top: 2px solid #eee; }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    st.markdown('<div style="margin-top: -50px;"></div>', unsafe_allow_html=True)
    st.image("logo gerard s białe .png", width=180)
    kurs_eur = st.number_input("Kurs Euro", value=4.27, step=0.01)
    cena_eur = st.number_input("Cena auta w EURO", value=3550.0)
    cena_pln_auto = st.number_input("Cena auta w PLN", value=float(cena_eur * kurs_eur))
    cena_do_akcyzy = st.number_input("Cena auta do akcyzy", value=float(cena_pln_auto))
    st.markdown("---")
    akcyza_opcja = st.radio("Akcyza", ["bez akcyzy", "do 2.0 l", "powyżej 2.0 l"], index=1)
    st.markdown("---")
    col_rej, col_prz = st.columns(2)
    with col_rej:
        st.markdown("**Rejestracja**")
        rejestracja_check = st.checkbox("Tak", value=True)
    with col_prz:
        st.markdown("**Przegląd**")
        przeglad_opcja = st.radio("Rodzaj", ["bez gazu", "z gazem"], index=0, label_visibility="collapsed")
    st.markdown("---")
    transport = st.number_input("Transport", value=1700)
    cena_lakieru = st.number_input("Lakier/elem", value=500)
    ilosc_lakieru = st.number_input("Ilość elem", value=0)
    koszt_lakiernika = cena_lakieru * ilosc_lakieru
    cena_czesci = st.number_input("Części", value=300)
    mechanik = st.number_input("Mechanik", value=700)
    myjnia = st.number_input("Myjnia", value=200)
    ogloszenia = st.number_input("Ogłoszenia", value=300)
    pozostale_inp = st.number_input("Pozostałe", value=200)
    st.markdown("---")
    cena_sprzedazy = st.number_input("CENA SPRZEDAŻY", value=25000)

# --- OBLICZENIA ---
stawka_akc = 0.031 if akcyza_opcja == "do 2.0 l" else (0.186 if akcyza_opcja == "powyżej 2.0 l" else 0)
wartosc_akcyzy = cena_do_akcyzy * stawka_akc
koszt_rej = 162 if rejestracja_check else 0
koszt_prz = 150 if przeglad_opcja == "bez gazu" else 245

# Grupa "Wszystko inne" do tabeli i wykresu
wszystko_inne = transport + koszt_lakiernika + cena_czesci + mechanik + myjnia + ogloszenia + pozostale_inp + koszt_rej + koszt_prz
suma_wydatki = cena_pln_auto + wartosc_akcyzy + wszystko_inne
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
roi = (dochod_na_czysto / cena_pln_auto * 100) if cena_pln_auto > 0 else 0

# --- PANEL GŁÓWNY ---
st.markdown(f"<h1 style='text-align: center; margin-top: -50px; font-weight: 800;'>Kalkulator Handlarza</h1>", unsafe_allow_html=True)

col_left, col_mid, col_right = st.columns([2, 3, 2])

with col_left:
    fig_bar = go.Figure()
    fig_bar.add_trace(go.Bar(x=['Auto', 'Akcyza', 'Pozostałe'], y=[cena_pln_auto, wartosc_akcyzy, wszystko_inne], marker_color='#111111'))
    fig_bar.add_trace(go.Bar(x=['SUMA'], y=[suma_wydatki], marker_color='#cc0000'))
    fig_bar.update_layout(height=350, margin=dict(t=20, b=20, l=0, r=0), showlegend=False, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig_bar, use_container_width=True)

with col_mid:
    r1_1, r1_2 = st.columns(2)
    r1_1.markdown(f"<div class='metric-card'><div class='metric-label'>Przychód (Zysk)</div><div class='metric-value' style='color:#28a745;'>{przychod_roznica:,.2f} zł</div><div class='metric-sub'>Brutto</div></div>", unsafe_allow_html=True)
    r1_2.markdown(f"<div class='metric-card'><div class='metric-label'>Dochód (Netto)</div><div class='metric-value' style='color:#28a745;'>{dochod_na_czysto:,.2f} zł</div><div class='metric-sub'>{roi:.1f}% ROI</div></div>", unsafe_allow_html=True)
    
    r2_1, r2_2, r2_3 = st.columns(3)
    r2_1.markdown(f"<div class='metric-card'><div class='metric-label'>VAT</div><div class='metric-value' style='font-size:16px;'>{vat_kwota:,.2f} zł</div></div>", unsafe_allow_html=True)
    r2_2.markdown(f"<div class='metric-card'><div class='metric-label'>Podatek</div><div class='metric-value' style='font-size:16px;'>{podatek_dochodowy:,.2f} zł</div></div>", unsafe_allow_html=True)
    r2_3.markdown(f"<div class='metric-card'><div class='metric-label'>Zdrowotna</div><div class='metric-value' style='font-size:16px;'>{skladka_zdrowotna:,.2f} zł</div></div>", unsafe_allow_html=True)
    
    r3_1, r3_2 = st.columns(2)
    r3_1.markdown(f"<div class='metric-card'><div class='metric-label'>Inwestycja Total</div><div class='metric-value' style='font-size:18px;'>{suma_wydatki:,.2f} zł</div></div>", unsafe_allow_html=True)
    r3_2.markdown(f"<div class='metric-card'><div class='metric-label'>Podatki Razem</div><div class='metric-value' style='color:#cc0000; font-size:18px;'>{podatki_razem:,.2f} zł</div></div>", unsafe_allow_html=True)

with col_right:
    fig_pie = go.Figure(data=[go.Pie(labels=['Auto', 'Koszty operacyjne', 'Podatki'], values=[cena_pln_auto, wszystko_inne, podatki_razem], hole=.5, marker_colors=['#cc0000', '#dddddd', '#111111'])])
    fig_pie.update_layout(margin=dict(t=20, b=20, l=0, r=0), height=350, showlegend=True, legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5))
    st.plotly_chart(fig_pie, use_container_width=True)

st.markdown("<br>", unsafe_allow_html=True)

# --- PRZYWRÓCONE TABELE ---
t1, t2 = st.columns(2)
with t1:
    st.markdown("<div class='table-header'>Wydatki - szczegóły</div>", unsafe_allow_html=True)
    st.markdown(f"""<div class='table-container'>
        <div class='row'><span>Samochód</span><span>{cena_pln_auto:,.2f} zł</span></div>
        <div class='row'><span>Akcyza</span><span>{wartosc_akcyzy:,.2f} zł</span></div>
        <div class='row'><span>Wszystko inne (transport, lakier, rej itd.)</span><span>{wszystko_inne:,.2f} zł</span></div>
        <div class='total-row'><span>SUMA WYDATKÓW</span><span>{suma_wydatki:,.2f} zł</span></div>
    </div>""", unsafe_allow_html=True)

with t2:
    st.markdown("<div class='table-header'>Przychody - szczegóły</div>", unsafe_allow_html=True)
    st.markdown(f"""<div class='table-container'>
        <div class='row'><span>Przychód (Różnica)</span><span>{przychod_roznica:,.2f} zł</span></div>
        <div class='row'><span>Dochód (Na czysto)</span><span style='color:#28a745; font-weight:bold;'>{dochod_na_czysto:,.2f} zł</span></div>
        <div class='total-row' style='color:#cc0000;'><span>Podatki razem</span><span>{podatki_razem:,.2f} zł</span></div>
    </div>""", unsafe_allow_html=True)
