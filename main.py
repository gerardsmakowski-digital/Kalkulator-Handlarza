import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Konfiguracja strony
st.set_page_config(page_title="Kalkulator Handlarza - Gerard S.", layout="wide")

# --- ZAAWANSOWANY CSS (Stylizacja Chipsów i Układu) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700&display=swap');
    html, body, [class*="css"], .stMarkdown, p, span, label { font-family: 'Montserrat', sans-serif !important; }
    
    /* Ciemny sidebar */
    [data-testid="stSidebar"] { background-color: #111111; color: white !important; border-right: 1px solid #333; }
    [data-testid="stSidebar"] label, [data-testid="stSidebar"] p { color: #ffffff !important; }

    /* STYLIZACJA CHIPSÓW (Segmented Control) - Ciemne tło, Biały aktywny */
    div[data-baseweb="segmented-control"] button {
        background-color: #1a1a1a !important;
        color: white !important;
        border: 1px solid #444 !important;
        padding: 10px 20px !important;
    }
    div[data-baseweb="segmented-control"] button[aria-selected="true"] {
        background-color: white !important;
        color: black !important;
        font-weight: bold !important;
    }

    /* Układ kart i tabel */
    .metric-card { background-color: white; padding: 20px; border-radius: 5px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); border: 1px solid #ddd; text-align: center; margin-bottom: 10px; }
    .metric-label { font-size: 13px; color: #666; font-weight: bold; text-transform: uppercase; }
    .metric-value { font-size: 26px; color: #000; font-weight: bold; }
    .table-header { background-color: #cc0000; color: white; padding: 12px; font-weight: bold; border-radius: 5px 5px 0 0; }
    .table-container { background: white; padding: 10px; border: 1px solid #eee; border-radius: 0 0 5px 5px; margin-bottom: 20px; }
    .row { display: flex; justify-content: space-between; padding: 8px 0; border-bottom: 1px solid #f0f0f0; font-size: 14px; color: #333; }
    .total-row { display: flex; justify-content: space-between; padding: 12px 0; font-weight: bold; color: #28a745; font-size: 16px; }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR (Panel Sterowania) ---
with st.sidebar:
    st.image("logo gerard s białe .png", width=180)
    st.markdown("<br>", unsafe_allow_html=True)
    
    # 1. Kurs i Cena
    kurs_eur = st.number_input("Kurs Euro", value=4.32, step=0.01)
    cena_eur = st.number_input("Cena auta w EURO", value=5000)
    
    st.markdown("---")
    
    # 2. Akcyza (Chipsy)
    st.markdown("Stawka Akcyzy")
    akcyza_typ = st.segmented_control(
        "akcyza_chips", 
        ["Brak", "do 2.0", "pow. 2.0"], 
        default="do 2.0",
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    
    # 3. Opłaty Dodatkowe (Rejestracja i Przegląd obok siebie)
    st.markdown("Opłaty dodatkowe")
    col_op1, col_op2 = st.columns(2)
    with col_op1:
        rejestracja_check = st.checkbox("Rejestracja", value=True)
    with col_op2:
        st.write("Przegląd") # Napis nad radio buttons jak na screenie
        przeglad_opcja = st.radio(
            "Rodzaj przeglądu", 
            ["Bez gazu", "Z gazem"], 
            index=0,
            label_visibility="collapsed"
        )
    
    st.markdown("---")
    
    # 4. Koszty eksploatacji
    transport = st.number_input("Transport (PLN)", value=1700)
    mechanik = st.number_input("Mechanik / Części", value=700)
    lakiernik = st.number_input("Lakierowanie", value=0)
    detailing = st.number_input("Myjnia / Detailing", value=200)
    ogloszenia = st.number_input("Ogłoszenia", value=300)
    
    st.markdown("---")
    cena_sprzedazy = st.number_input("CENA SPRZEDAŻY AUTA", value=30000)

# --- LOGIKA OBLICZEŃ ---
cena_pln = cena_eur * kurs_eur
stawka_akc = 0.031 if akcyza_typ == "do 2.0" else (0.186 if akcyza_typ == "pow. 2.0" else 0)
wartosc_akcyzy = cena_pln * stawka_akc
koszt_rej = 162 if rejestracja_check else 0
koszt_prz = 150 if przeglad_opcja == "Bez gazu" else 245

suma_wydatki = cena_pln + wartosc_akcyzy + transport + mechanik + lakiernik + detailing + ogloszenia + koszt_rej + koszt_prz
dochod = cena_sprzedazy - suma_wydatki
marza_proc = (dochod / suma_wydatki * 100) if suma_wydatki > 0 else 0

# --- PANEL GŁÓWNY ---
st.markdown(f"<h2 style='text-align: center; margin-bottom: 0;'>Kalkulator Handlarza</h2>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align: center; color: gray; margin-bottom: 30px;'>by Gerard S Digital Agency</p>", unsafe_allow_html=True)

# Górny rząz z wizualizacjami
c1, c2, c3 = st.columns([1.5, 2, 1.5])

with c1:
    st.bar_chart(pd.DataFrame({'PLN': [cena_pln, wartosc_akcyzy, transport, dochod]}, index=['Auto', 'Akcyza', 'Transport', 'Zysk']))

with c2:
    m1, m2 = st.columns(2)
    m1.markdown(f"<div class='metric-card'><div class='metric-label'>Przychód</div><div class='metric-value'>{cena_sprzedazy:,.0f} zł</div><div style='color:gray;font-size:11px;'>{marza_proc:.1f}% marży</div></div>", unsafe_allow_html=True)
    m2.markdown(f"<div class='metric-card'><div class='metric-label'>Dochód</div><div class='metric-value' style='color:#28a745;'>{dochod:,.0f} zł</div></div>", unsafe_allow_html=True)
    m3, m4 = st.columns(2)
    m3.markdown(f"<div class='metric-card'><div class='metric-label'>Vat (23%)</div><div class='metric-value' style='font-size:18px;'>{(dochod*0.23):,.0f} zł</div></div>", unsafe_allow_html=True)
    m4.markdown(f"<div class='metric-card'><div class='metric-label'>Zdrowotna</div><div class='metric-value' style='font-size:18px;'>130 zł</div></div>", unsafe_allow_html=True)

with c3:
    fig = go.Figure(data=[go.Pie(labels=['Auto', 'Akcyza', 'Inne'], values=[cena_pln, wartosc_akcyzy, suma_wydatki-cena_pln-wartosc_akcyzy], hole=.4, marker_colors=['#cc0000', '#111111', '#dddddd'])])
    fig.update_layout(margin=dict(t=0, b=0, l=0, r=0), height=220, showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

st.markdown("<br>", unsafe_allow_html=True)

# Tabele podsumowujące (Dół)
t1, t2 = st.columns(2)
with t1:
    st.markdown("<div class='table-header'>Wydatki - podsumowanie</div>", unsafe_allow_html=True)
    st.markdown(f"""<div class='table-container'>
        <div class='row'><span>Samochód</span><span>{cena_pln:,.2f} zł</span></div>
        <div class='row'><span>Akcyza ({akcyza_typ})</span><span>{wartosc_akcyzy:,.2f} zł</span></div>
        <div class='row'><span>Transport</span><span>{transport:,.2f} zł</span></div>
        <div class='row'><span>Przegląd i Rejestracja</span><span>{koszt_prz + koszt_rej:,.2f} zł</span></div>
        <div class='row'><span>Mechanik i Części</span><span>{mechanik:,.2f} zł</span></div>
        <div class='row'><span>Inne (Lakier/Detail/Ogł)</span><span>{lakiernik+detailing+ogloszenia:,.2f} zł</span></div>
        <div class='total-row'><span>Podsumowanie wydatków</span><span>{suma_wydatki:,.2f} zł</span></div>
    </div>""", unsafe_allow_html=True)

with t2:
    st.markdown("<div class='table-header'>Przychody - podsumowanie</div>", unsafe_allow_html=True)
    st.markdown(f"""<div class='table-container'>
        <div class='row'><span>Przychód ze sprzedaży</span><span>{cena_sprzedazy:,.2f} zł</span></div>
        <div class='row'><span>Dochód Brutto</span><span>{dochod:,.2f} zł</span></div>
        <div class='row'><span>Podatek dochodowy (est.)</span><span>{dochod*0.19:,.2f} zł</span></div>
        <div class='total-row' style='color:#000;'><span>Zysk Procentowy</span><span>{marza_proc:.1f}%</span></div>
    </div>""", unsafe_allow_html=True)
