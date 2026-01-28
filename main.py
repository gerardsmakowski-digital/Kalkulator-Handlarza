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
    [data-testid="stSidebar"] label, [data-testid="stSidebar"] p { color: #ffffff !important; }
    [data-testid="stSidebar"] hr { margin: 10px 0 !important; border-top: 1px solid rgba(255, 255, 255, 0.2) !important; }
    [data-testid="stSidebar"] [data-testid="stVerticalBlock"] { gap: 0.5rem !important; }
    .metric-card { background-color: white; padding: 20px; border-radius: 5px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); border: 1px solid #ddd; text-align: center; margin-bottom: 10px; }
    .metric-label { font-size: 13px; color: #666; font-weight: bold; text-transform: uppercase; }
    .metric-value { font-size: 26px; color: #000; font-weight: bold; }
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
        st.markdown(f"<p style='font-size: 12px; color: #aaa; margin-top: -15px;'>Wpisz kwotę w PLN poniżej</p>", unsafe_allow_html=True)
        cena_pln_auto = st.number_input("Cena auta w PLN", value=0.0)

    finalna_cena_samochodu = cena_pln_auto
    cena_do_akcyzy = st.number_input("Cena auta do akcyzy", value=float(finalna_cena_samochodu))
    
    st.markdown("---")
    st.markdown("**Stawka Akcyzy**")
    akcyza_opcja = st.radio("akcyza", ["bez akcyzy", "do 2.0 l", "powyżej 2.0 l"], index=1, label_visibility="collapsed")
    
    st.markdown("---")
    c_rej, c_prz = st.columns(2)
    with c_rej:
        st.markdown("**Rejestracja**")
        rejestracja_check = st.checkbox("Rej", value=True, label_visibility="collapsed")
    with c_prz:
        st.markdown("**Przegląd**")
        przeglad_opcja = st.radio("Prz", ["bez gazu", "z gazem"], index=0, label_visibility="collapsed")
    
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
suma_wydatki = (finalna_cena_samochodu + wartosc_akcyzy + transport + koszt_lakiernika + cena_czesci + mechanik + myjnia + ogloszenia + pozostale + koszt_rej + koszt_prz)

dochod_brutto = cena_sprzedazy - suma_wydatki
vat_kwota = dochod_brutto * 0.23 if dochod_brutto > 0 else 0
podatek_dochodowy = dochod_brutto * 0.19 if dochod_brutto > 0 else 0
skladka_zdrowotna = dochod_brutto * 0.049 if dochod_brutto > 0 else 0
podatki_razem = vat_kwota + podatek_dochodowy + skladka_zdrowotna
marza_proc = (dochod_brutto / suma_wydatki * 100) if suma_wydatki > 0 else 0

# --- PANEL GŁÓWNY ---
st.markdown(f"<h2 style='text-align: center; margin-top: -30px; margin-bottom: 0;'>Kalkulator Handlarza</h2>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align: center; color: #000; margin-bottom: 40px; font-size: 18px;'>by Gerard S Digital Agency</p>", unsafe_allow_html=True)

# Dashboard
c1, c2, c3 = st.columns([1.5, 2, 1.5])
with c1:
    st.bar_chart(pd.DataFrame({'PLN': [finalna_cena_samochodu, wartosc_akcyzy, transport, dochod_brutto]}, index=['Auto', 'Akcyza', 'Transport', 'Zysk']))

with c2:
    m1, m2 = st.columns(2)
    m1.markdown(f"<div class='metric-card'><div class='metric-label'>Przychód</div><div class='metric-value'>{cena_sprzedazy:,.0f} zł</div></div>", unsafe_allow_html=True)
    m2.markdown(f"<div class='metric-card'><div class='metric-label'>Dochód</div><div class='metric-value' style='color:#28a745;'>{dochod_brutto:,.0f} zł</div></div>", unsafe_allow_html=True)
    m3, m4 = st.columns(2)
    m3.markdown(f"<div class='metric-card'><div class='metric-label'>Podatki Razem</div><div class='metric-value' style='color:#cc0000; font-size:22px;'>{podatki_razem:,.0f} zł</div></div>", unsafe_allow_html=True)
    m4.markdown(f"<div class='metric-card'><div class='metric-label'>Marża</div><div class='metric-value'>{marza_proc:.1f}%</div></div>", unsafe_allow_html=True)

with c3:
    fig = go.Figure(data=[go.Pie(labels=['Auto', 'Akcyza', 'Inne'], values=[finalna_cena_samochodu, wartosc_akcyzy, suma_wydatki-finalna_cena_samochodu-wartosc_akcyzy], hole=.4, marker_colors=['#cc0000', '#111111', '#dddddd'])])
    fig.update_layout(margin=dict(t=0, b=0, l=0, r=0), height=220, showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

st.markdown("<br>", unsafe_allow_html=True)
t1, t2 = st.columns(2)

with t1:
    st.markdown("<div class='table-header'>Wydatki - podsumowanie</div>", unsafe_allow_html=True)
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
        <div class='total-row'><span>Podsumowanie</span><span>{suma_wydatki:,.2f} zł</span></div>
    </div>""", unsafe_allow_html=True)

with t2:
    st.markdown("<div class='table-header'>Przychody - podsumowanie</div>", unsafe_allow_html=True)
    st.markdown(f"""<div class='table-container'>
        <div class='row'><span>Przychód</span><span>{cena_sprzedazy:,.2f} zł</span></div>
        <div class='row'><span>Dochód</span><span>{dochod_brutto:,.2f} zł</span></div>
        <div class='row'><span>Vat</span><span>{vat_kwota:,.2f} zł</span></div>
        <div class='row'><span>Podatek dochodowy 19%</span><span>{podatek_dochodowy:,.2f} zł</span></div>
        <div class='row'><span>Składka zdrowotna 4,90%</span><span>{skladka_zdrowotna:,.2f} zł</span></div>
        <div class='total-row' style='color:#cc0000;'><span>Podatki razem</span><span>{podatki_razem:,.2f} zł</span></div>
    </div>""", unsafe_allow_html=True)
