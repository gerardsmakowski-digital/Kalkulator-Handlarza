import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Konfiguracja strony
st.set_page_config(page_title="Kalkulator Handlarza - Gerard S.", layout="wide")

# --- STABILNY CSS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700&display=swap');
    
    * { font-family: 'Montserrat', sans-serif !important; }

    /* Ukrycie błędów technicznych */
    header, footer, #MainMenu { visibility: hidden !important; }
    button[title="Collapse sidebar"] { display: none !important; }

    /* SIDEBAR STYLING */
    [data-testid="stSidebar"] { 
        background-color: #111111; 
        color: white !important; 
        border-right: 1px solid #333; 
    }
    
    /* Białe rozdzielacze */
    hr {
        margin: 15px 0 !important;
        border: 0;
        border-top: 1px solid rgba(255, 255, 255, 0.3) !important;
    }

    [data-testid="stSidebar"] label { 
        color: #ffffff !important; 
        font-weight: 600 !important;
        margin-bottom: 5px !important;
    }

    /* Pola numeryczne - stabilizacja */
    .stNumberInput { margin-bottom: 10px !important; }

    /* Karty wyników */
    .metric-card { 
        background-color: white; 
        padding: 20px; 
        border-radius: 8px; 
        box-shadow: 0 2px 10px rgba(0,0,0,0.05); 
        border: 1px solid #eee; 
        text-align: center; 
    }
    .metric-label { font-size: 12px; color: #888; font-weight: bold; text-transform: uppercase; }
    .metric-value { font-size: 24px; color: #000; font-weight: bold; }
    
    .table-header { background-color: #cc0000; color: white; padding: 10px; font-weight: bold; border-radius: 8px 8px 0 0; }
    .table-container { background: white; padding: 15px; border: 1px solid #eee; border-radius: 0 0 8px 8px; }
    .row { display: flex; justify-content: space-between; padding: 5px 0; border-bottom: 1px solid #f9f9f9; font-size: 14px; }
    .total-row { display: flex; justify-content: space-between; padding-top: 10px; font-weight: bold; color: #28a745; border-top: 1px solid #eee; }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    st.markdown('<div style="margin-top: -30px;"></div>', unsafe_allow_html=True)
    st.image("logo gerard s białe .png", width=170)
    st.markdown("<br>", unsafe_allow_html=True)
    
    kurs_eur = st.number_input("Kurs Euro", value=4.27, step=0.01)
    cena_eur = st.number_input("Cena auta w EURO", value=0)
    
    if cena_eur > 0:
        kwota_pln = cena_eur * kurs_eur
        st.markdown(f"<p style='color: #28a745; font-size: 13px; margin-top: -10px;'>= {kwota_pln:,.2f} PLN</p>", unsafe_allow_html=True)
    
    cena_pln_auto = st.number_input("Cena auta w PLN", value=float(cena_eur * kurs_eur))
    cena_do_akcyzy = st.number_input("Cena do akcyzy", value=float(cena_pln_auto))
    
    st.markdown("---")
    st.write("**STAWKA AKCYZY**")
    akcyza_opcja = st.radio("akc", ["bez akcyzy", "do 2.0 l", "powyżej 2.0 l"], index=1, label_visibility="collapsed")
    
    st.markdown("---")
    c_op1, c_op2 = st.columns(2)
    with c_op1:
        st.write("**REJESTRACJA**")
        rejestracja_check = st.checkbox("Zaznacz", value=True)
    with c_op2:
        st.write("**PRZEGLĄD**")
        przeglad_opcja = st.radio("prz", ["bez gazu", "z gazem"], index=0, label_visibility="collapsed")
    
    st.markdown("---")
    transport = st.number_input("Transport", value=1700)
    
    c_l1, c_l2 = st.columns(2)
    with c_l1:
        cena_lakieru = st.number_input("Lakier/elem", value=500)
    with c_l2:
        ilosc_lakieru = st.number_input("Ilość elem", value=0)
    
    mechanik = st.number_input("Mechanik", value=700)
    pozostale = st.number_input("Inne (myjnia, części, ogłoszenia)", value=1000)
    
    st.markdown("---")
    cena_sprzedazy = st.number_input("CENA SPRZEDAŻY", value=25000)

# --- LOGIKA OBLICZEŃ ---
stawka_akc = 0.031 if akcyza_opcja == "do 2.0 l" else (0.186 if akcyza_opcja == "powyżej 2.0 l" else 0)
koszt_akcyzy = cena_do_akcyzy * stawka_akc
koszt_lakiernika = cena_lakieru * ilosc_lakieru
koszt_rej = 162 if rejestracja_check else 0
koszt_prz = 150 if przeglad_opcja == "bez gazu" else 245

suma_wydatki = (cena_pln_auto + koszt_akcyzy + transport + koszt_lakiernika + mechanik + pozostale + koszt_rej + koszt_prz)
zysk = cena_sprzedazy - suma_wydatki
marza = (zysk / suma_wydatki * 100) if suma_wydatki > 0 else 0

# --- PANEL GŁÓWNY ---
st.markdown(f"""
    <div style='text-align: center; margin-top: -30px; margin-bottom: 30px;'>
        <h1 style='margin-bottom: 0;'>Kalkulator Handlarza</h1>
        <p style='font-size: 18px; color: #333;'>by Gerard S Digital Agency</p>
    </div>
""", unsafe_allow_html=True)

# Metryki
col_m1, col_m2, col_m3 = st.columns(3)
with col_m1:
    st.markdown(f"<div class='metric-card'><div class='metric-label'>Inwestycja Total</div><div class='metric-value'>{suma_wydatki:,.0f} zł</div></div>", unsafe_allow_html=True)
with col_m2:
    st.markdown(f"<div class='metric-card'><div class='metric-label'>Zysk Sprzedaży</div><div class='metric-value' style='color:#28a745;'>{zysk:,.0f} zł</div></div>", unsafe_allow_html=True)
with col_m3:
    st.markdown(f"<div class='metric-card'><div class='metric-label'>Marża</div><div class='metric-value'>{marza:.1f}%</div></div>", unsafe_allow_html=True)

# Tabele i wykres
st.markdown("<br>", unsafe_allow_html=True)
t1, t2 = st.columns([2, 1])

with t1:
    st.markdown("<div class='table-header'>Szczegółowe Koszty</div>", unsafe_allow_html=True)
    st.markdown(f"""
    <div class='table-container'>
        <div class='row'><span>Zakup auta</span><span>{cena_pln_auto:,.2f} zł</span></div>
        <div class='row'><span>Akcyza ({akcyza_opcja})</span><span>{koszt_akcyzy:,.2f} zł</span></div>
        <div class='row'><span>Transport</span><span>{transport:,.2f} zł</span></div>
        <div class='row'><span>Lakierowanie ({ilosc_lakieru} el.)</span><span>{koszt_lakiernika:,.2f} zł</span></div>
        <div class='row'><span>Serwis i Inne</span><span>{mechanik + pozostale:,.2f} zł</span></div>
        <div class='row'><span>Opłaty (Rej + Prz)</span><span>{koszt_rej + koszt_prz:,.2f} zł</span></div>
        <div class='total-row'><span>SUMA KOSZTÓW</span><span>{suma_wydatki:,.2f} zł</span></div>
    </div>
    """, unsafe_allow_html=True)

with t2:
    fig = go.Figure(data=[go.Pie(labels=['Auto', 'Koszty', 'Zysk'], values=[cena_pln_auto, suma_wydatki-cena_pln_auto, zysk], hole=.4)])
    fig.update_layout(margin=dict(t=0, b=0, l=0, r=0), height=250, showlegend=False)
    st.plotly_chart(fig, use_container_width=True)
