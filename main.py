import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Konfiguracja strony
st.set_page_config(page_title="Kalkulator Handlarza - Gerard S.", layout="wide")

# --- AGRESYWNY CSS (Kompaktowy wygląd sidebaru) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700&display=swap');
    
    * { font-family: 'Montserrat', sans-serif !important; }

    /* Usuwanie błędów wizualnych */
    button[title="Collapse sidebar"], [data-testid="stSidebarCollapseButton"] { display: none !important; }
    #MainMenu, footer, header { visibility: hidden !important; height: 0 !important; }

    /* KOMPAKTOWY SIDEBAR */
    [data-testid="stSidebar"] { background-color: #111111; color: white !important; border-right: 1px solid #333; }
    
    /* Zmniejszenie odstępów między elementami w sidebarze */
    [data-testid="stSidebar"] [data-testid="stVerticalBlock"] > div {
        padding-top: 0.1rem !important;
        padding-bottom: 0.1rem !important;
        margin-top: -5px !important;
    }

    /* Zmniejszenie odstępów przy liniach poziomej hr */
    hr {
        margin-top: 0.5rem !important;
        margin-bottom: 0.5rem !important;
        border-bottom: 1px solid #333 !important;
    }

    /* Zacieśnienie etykiet */
    label, .stMarkdown p {
        margin-bottom: 2px !important;
        padding-bottom: 0px !important;
    }

    .stRadio div[role="radiogroup"] {
        padding-top: 2px !important;
        gap: 2px !important;
    }

    /* Dashboard Stylizacja */
    .metric-card { background-color: white; padding: 20px; border-radius: 5px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); border: 1px solid #ddd; text-align: center; margin-bottom: 10px; }
    .metric-label { font-size: 13px; color: #666; font-weight: bold; text-transform: uppercase; }
    .metric-value { font-size: 26px; color: #000; font-weight: bold; }
    .table-header { background-color: #cc0000; color: white; padding: 12px; font-weight: bold; border-radius: 5px 5px 0 0; }
    .table-container { background: white; padding: 10px; border: 1px solid #eee; border-radius: 0 0 5px 5px; margin-bottom: 20px; }
    .row { display: flex; justify-content: space-between; padding: 8px 0; border-bottom: 1px solid #f0f0f0; font-size: 14px; color: #333; }
    .total-row { display: flex; justify-content: space-between; padding: 12px 0; font-weight: bold; color: #28a745; font-size: 16px; }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    st.markdown('<div style="margin-top: -70px;"></div>', unsafe_allow_html=True)
    st.image("logo gerard s białe .png", width=160)
    
    kurs_eur = st.number_input("Kurs Euro", value=4.27, step=0.01)
    cena_eur = st.number_input("Cena auta w EURO", value=0)
    
    kwota_przeliczona = cena_eur * kurs_eur
    st.markdown(f"<p style='font-size: 11px; color: #aaa; margin-top: -10px;'>{kwota_przeliczona:,.2f} zł po kursie</p>", unsafe_allow_html=True)
    
    cena_pln_auto = st.number_input("Cena auta w PLN", value=float(kwota_przeliczona))
    cena_do_akcyzy = st.number_input("Cena do akcyzy", value=float(cena_pln_auto))
    
    st.markdown("---")
    st.markdown("**Stawka Akcyzy**")
    akcyza_opcja = st.radio("akcyza", ["bez akcyzy", "do 2.0 l", "powyżej 2.0 l"], index=1, label_visibility="collapsed")
    
    st.markdown("---")
    col_op1, col_op2 = st.columns(2)
    with col_op1:
        st.markdown("**Rejestracja**")
        rejestracja_check = st.checkbox("Rej", value=True, label_visibility="collapsed")
    with col_op2:
        st.markdown("**Przegląd**")
        przeglad_opcja = st.radio("Przeg", ["bez gazu", "z gazem"], index=0, label_visibility="collapsed")
    
    st.markdown("---")
    transport = st.number_input("Transport", value=1700)
    
    # Lakierowanie w jednej linii dla oszczędności miejsca
    c_l1, c_l2 = st.columns(2)
    with c_l1:
        cena_lakieru = st.number_input("Lakier/elem", value=500)
    with c_l2:
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
suma_wydatki = (cena_pln_auto + wartosc_akcyzy + transport + koszt_lakiernika + cena_czesci + mechanik + myjnia + ogloszenia + pozostale + koszt_rej + koszt_prz)
dochod = cena_sprzedazy - suma_wydatki
marza_proc = (dochod / suma_wydatki * 100) if suma_wydatki > 0 else 0

# --- PANEL GŁÓWNY ---
st.markdown('<div style="text-align: center; margin-top: -60px;"><h2 style="margin-bottom: 0;">Kalkulator Handlarza</h2>'
            '<p style="color: #000; margin-top:-10px; font-size: 18px;">by Gerard S Digital Agency</p></div>', unsafe_allow_html=True)

c1, c2, c3 = st.columns([1.5, 2, 1.5])
with c1:
    st.bar_chart(pd.DataFrame({'PLN': [cena_pln_auto, wartosc_akcyzy, transport, dochod]}, index=['Auto', 'Akcyza', 'Transport', 'Zysk']))
with c2:
    m1, m2 = st.columns(2)
    m1.markdown(f"<div class='metric-card'><div class='metric-label'>Przychód</div><div class='metric-value'>{cena_sprzedazy:,.0f} zł</div></div>", unsafe_allow_html=True)
    m2.markdown(f"<div class='metric-card'><div class='metric-label'>Dochód</div><div class='metric-value' style='color:#28a745;'>{dochod:,.0f} zł</div></div>", unsafe_allow_html=True)
    m3, m4 = st.columns(2)
    m3.markdown(f"<div class='metric-card'><div class='metric-label'>Vat (23%)</div><div class='metric-value' style='font-size:18px;'>{(dochod*0.23):,.0f} zł</div></div>", unsafe_allow_html=True)
    m4.markdown(f"<div class='metric-card'><div class='metric-label'>Zdrowotna</div><div class='metric-value' style='font-size:18px;'>130 zł</div></div>", unsafe_allow_html=True)
with c3:
    fig = go.Figure(data=[go.Pie(labels=['Auto', 'Akcyza', 'Inne'], values=[cena_pln_auto, wartosc_akcyzy, suma_wydatki-cena_pln_auto-wartosc_akcyzy], hole=.4, marker_colors=['#cc0000', '#111111', '#dddddd'])])
    fig.update_layout(margin=dict(t=0, b=0, l=0, r=0), height=220, showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

st.markdown("<br>", unsafe_allow_html=True)
t1, t2 = st.columns(2)
with t1:
    st.markdown("<div class='table-header'>Wydatki - podsumowanie</div>", unsafe_allow_html=True)
    st.markdown(f"""<div class='table-container'>
        <div class='row'><span>Samochód</span><span>{cena_pln_auto:,.2f} zł</span></div>
        <div class='row'><span>Akcyza</span><span>{wartosc_akcyzy:,.2f} zł</span></div>
        <div class='row'><span>Transport</span><span>{transport:,.2f} zł</span></div>
        <div class='total-row'><span>SUMA</span><span>{suma_wydatki:,.2f} zł</span></div>
    </div>""", unsafe_allow_html=True)
with t2:
    st.markdown("<div class='table-header'>Przychody - podsumowanie</div>", unsafe_allow_html=True)
    st.markdown(f"""<div class='table-container'>
        <div class='row'><span>Przychód</span><span>{cena_sprzedazy:,.2f} zł</span></div>
        <div class='row'><span>Dochód</span><span>{dochod:,.2f} zł</span></div>
        <div class='total-row' style='color:#000;'><span>Marża</span><span>{marza_proc:.1f}%</span></div>
    </div>""", unsafe_allow_html=True)
