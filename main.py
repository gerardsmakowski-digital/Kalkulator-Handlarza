import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Konfiguracja strony
st.set_page_config(
    page_title="Kalkulator Handlarza - Gerard S.", 
    layout="wide",
    initial_sidebar_state="expanded" 
)

# --- CSS (Ukrycie headera i naprawa czcionek) ---
st.markdown("""
    <style>
    

    footer { visibility: hidden !important; }
    #MainMenu { visibility: hidden !important; }

    /* Poprawka odstępu po usunięciu headera, żeby tytuł nie był przyklejony do góry */
    .block-container {
        padding-top: 2rem !important;
    }

    /* Sidebar - Stylizacja */
    [data-testid="stSidebar"] { background-color: #111111; color: white !important; }
    [data-testid="stSidebar"] label, [data-testid="stSidebar"] p { color: #ffffff !important; font-size: 14px !important; }
    [data-testid="stSidebar"] hr { margin: 15px 0 !important; border-top: 1px solid rgba(255, 255, 255, 0.2) !important; }
    
    /* Kolor ikony zamykania sidebaru */
    [data-testid="stSidebar"] button { color: white !important; }

    /* Dashboard Cards */
    .metric-card { 
        background-color: white; padding: 15px; border-radius: 10px; 
        box-shadow: 0 4px 6px rgba(0,0,0,0.07); border: 1px solid #eee; 
        text-align: center; margin-bottom: 10px; min-height: 110px; 
        display: flex; flex-direction: column; justify-content: center; 
    }
    .metric-label { font-size: 11px; color: #666; font-weight: bold; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 4px; }
    .metric-value { font-size: 22px; color: #000; font-weight: 800; margin: 2px 0; }
    .metric-sub { font-size: 12px; color: #28a745; font-weight: bold; }

    /* Tables */
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
        st.markdown("### Gerard S.")
    
    kurs_eur = st.number_input("Kurs Euro", value=4.27, step=0.01)
    cena_eur = st.number_input("Cena auta w EURO", value=3550.0)
    
    kwota_z_euro = cena_eur * kurs_eur
    if cena_eur > 0:
        st.markdown(f"<p style='font-size: 12px; color: #28a745; margin-top: -15px;'>Przeliczono z Euro: {kwota_z_euro:,.2f} zł</p>", unsafe_allow_html=True)
        cena_pln_auto = st.number_input("Cena auta w PLN", value=float(kwota_z_euro))
    else:
        cena_pln_auto = st.number_input("Cena auta w PLN", value=15158.50)

    finalna_cena_samochodu = cena_pln_auto
    cena_do_akcyzy = st.number_input("Cena auta do akcyzy", value=float(finalna_cena_samochodu))
    
    st.markdown("---")
    st.markdown("**Akcyza**")
    akcyza_opcja = st.radio("Stawka", ["bez akcyzy", "do 2.0 l", "powyżej 2.0 l"], index=1, label_visibility="collapsed")
    
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

pozostale_suma = suma_wydatki - finalna_cena_samochodu - wartosc_akcyzy
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
procent_dochod = (dochod_na_czysto / finalna_cena_samochodu * 100) if finalna_cena_samochodu > 0 else 0

# --- PANEL GŁÓWNY ---
st.markdown(f"<h1 style='text-align: center; margin-top: 30px; font-weight: 800;'>Kalkulator Handlarza</h1>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align: center; color: #666; margin-bottom: 30px; font-size: 18px;'>by Gerard S Digital Agency</p>", unsafe_allow_html=True)

col_left, col_mid, col_right = st.columns([2.5, 3, 2.5])

with col_left:
    labels_pie = ['Samochód', 'Akcyza', 'Pozostałe koszty', 'Przychód']
    values_pie = [finalna_cena_samochodu, wartosc_akcyzy, pozostale_suma, przychod_roznica]
    
    fig_left = go.Figure(data=[go.Pie(
        labels=labels_pie, 
        values=values_pie, 
        hole=.4, 
        marker_colors=['#cc0000', '#990000', '#dddddd', '#28a745'],
        textinfo='percent+label'
    )])
    fig_left.update_layout(
        title=dict(text="Struktura ceny sprzedaży", x=0.5, y=0.95, xanchor='center'),
        margin=dict(t=80, b=50, l=10, r=10), 
        height=450, 
        showlegend=False
    )
    st.plotly_chart(fig_left, use_container_width=True)

with col_mid:
    r1_1, r1_2 = st.columns(2)
    r1_1.markdown(f"<div class='metric-card'><div class='metric-label'>Przychód</div><div class='metric-value' style='color:#28a745;'>{przychod_roznica:,.2f} zł</div></div>", unsafe_allow_html=True)
    r1_2.markdown(f"<div class='metric-card'><div class='metric-label'>Dochód</div><div class='metric-value' style='color:#28a745;'>{dochod_na_czysto:,.2f} zł</div><div class='metric-sub'>{procent_dochod:.1f}% ROI</div></div>", unsafe_allow_html=True)

    r2_1, r2_2, r2_3 = st.columns(3)
    r2_1.markdown(f"<div class='metric-card'><div class='metric-label'>VAT</div><div class='metric-value' style='font-size:16px;'>{vat_kwota:,.2f} zł</div></div>", unsafe_allow_html=True)
    r2_2.markdown(f"<div class='metric-card'><div class='metric-label'>Podatek</div><div class='metric-value' style='font-size:16px;'>{podatek_dochodowy:,.2f} zł</div></div>", unsafe_allow_html=True)
    r2_3.markdown(f"<div class='metric-card'><div class='metric-label'>Zdrowotna</div><div class='metric-value' style='font-size:16px;'>{skladka_zdrowotna:,.2f} zł</div></div>", unsafe_allow_html=True)

    r3_1, r3_2 = st.columns(2)
    r3_1.markdown(f"<div class='metric-card'><div class='metric-label'>Inwestycja Total</div><div class='metric-value' style='font-size:18px;'>{suma_wydatki:,.2f} zł</div></div>", unsafe_allow_html=True)
    r3_2.markdown(f"<div class='metric-card'><div class='metric-label'>Podatki Razem</div><div class='metric-value' style='color:#cc0000; font-size:18px;'>{podatki_razem:,.2f} zł</div></div>", unsafe_allow_html=True)

with col_right:
    data_bars = {
        'Przychód': przychod_roznica,
        'Dochód': dochod_na_czysto,
        'VAT': vat_kwota,
        'Podatek': podatek_dochodowy,
        'Zdrowotna': skladka_zdrowotna
    }
    
    fig_right = go.Figure(data=[
        go.Bar(
            x=list(data_bars.keys()), 
            y=list(data_bars.values()),
            marker_color=['#28a745', '#1e7e34', '#cc0000', '#990000', '#660000']
        )
    ])
    fig_right.update_layout(
        title=dict(text="Wynik finansowy (PLN)", x=0.5, y=0.95, xanchor='center'),
        height=450, 
        margin=dict(t=80, b=50, l=10, r=10),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        yaxis=dict(showgrid=True, gridcolor='#f0f0f0')
    )
    st.plotly_chart(fig_right, use_container_width=True)

st.markdown("<br>", unsafe_allow_html=True)

# --- TABELE ---
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
        <div class='row'><span>Przychód</span><span>{przychod_roznica:,.2f} zł</span></div>
        <div class='row'><span>Dochód</span><span style='color:#28a745; font-weight:bold;'>{dochod_na_czysto:,.2f} zł</span></div>
        <div class='row'><span>Vat (marża)</span><span>{vat_kwota:,.2f} zł</span></div>
        <div class='row'><span>Podatek dochodowy 19%</span><span>{podatek_dochodowy:,.2f} zł</span></div>
        <div class='row'><span>Składka zdrowotna 4,90%</span><span>{skladka_zdrowotna:,.2f} zł</span></div>
        <div class='total-row' style='color:#cc0000;'><span>Podatki razem</span><span>{podatki_razem:,.2f} zł</span></div>
    </div>""", unsafe_allow_html=True)
