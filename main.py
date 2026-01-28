import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Konfiguracja strony
st.set_page_config(page_title="Kalkulator Handlarza - Gerard S.", layout="wide")

# --- CUSTOM CSS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700&display=swap');
    html, body, [class*="css"], .stMarkdown, p, span, label { font-family: 'Montserrat', sans-serif !important; }
    [data-testid="stSidebar"] { background-color: #111111; color: white !important; border-right: 1px solid #333; }
    [data-testid="stSidebar"] label, [data-testid="stSidebar"] p { color: #ffffff !important; }
    .metric-card { background-color: white; padding: 20px; border-radius: 5px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); border: 1px solid #ddd; text-align: center; margin-bottom: 10px; }
    .metric-label { font-size: 14px; color: #666; font-weight: bold; text-transform: uppercase; }
    .metric-value { font-size: 28px; color: #000; font-weight: bold; }
    .table-header { background-color: #cc0000; color: white; padding: 12px; font-weight: bold; border-radius: 5px 5px 0 0; }
    .table-container { background: white; padding: 10px; border: 1px solid #eee; border-radius: 0 0 5px 5px; }
    .row { display: flex; justify-content: space-between; padding: 8px 0; border-bottom: 1px solid #f0f0f0; font-size: 14px; }
    .total-row { display: flex; justify-content: space-between; padding: 12px 0; font-weight: bold; color: #28a745; font-size: 16px; }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    st.image("logo gerard s białe .png", width=180) # Zmniejszone logo
    st.markdown("<br>", unsafe_allow_html=True)
    
    st.markdown("### DANE WEJŚCIOWE")
    kurs_eur = st.number_input("Kurs Euro", value=4.32, step=0.01)
    cena_eur = st.number_input("Cena auta w EURO", value=5000)
    
    st.markdown("---")
    # WYBÓR AKCYZY JAKO CHIPSY
    st.markdown("Stawka Akcyzy")
    akcyza_typ = st.segmented_control(
        "Wybierz akcyzę", 
        ["Brak", "do 2.0 l", "pow. 2.0 l"], 
        default="do 2.0 l"
    )
    
    st.markdown("---")
    # ROZBUDOWANY PRZEGLĄD
    st.markdown("Przegląd techniczny")
    przeglad_opcja = st.radio(
        "Rodzaj przeglądu", 
        ["Brak", "Bez gazu (150 zł)", "Z gazem (245 zł)"], 
        index=1
    )
    
    rejestracja_check = st.checkbox("Rejestracja (162 zł)", value=True)
    
    st.markdown("---")
    transport = st.number_input("Transport (PLN)", value=1700)
    mechanik = st.number_input("Mechanik / Części", value=700)
    lakiernik = st.number_input("Lakierowanie", value=0)
    detailing = st.number_input("Myjnia / Detailing", value=200)
    ogloszenia = st.number_input("Ogłoszenia / Inne", value=300)
    
    st.markdown("---")
    cena_sprzedazy = st.number_input("CENA SPRZEDAŻY AUTA", value=30000)

# --- LOGIKA OBLICZEŃ ---
cena_pln = cena_eur * kurs_eur

# Obliczanie akcyzy z chipsów
stawka_akc = 0.031 if akcyza_typ == "do 2.0 l" else (0.186 if akcyza_typ == "pow. 2.0 l" else 0)
wartosc_akcyzy = cena_pln * stawka_akc

# Obliczanie przeglądu
koszt_prz = 150 if "Bez gazu" in przeglad_opcja else (245 if "Z gazem" in przeglad_opcja else 0)
koszt_rej = 162 if rejestracja_check else 0

suma_wydatki = cena_pln + wartosc_akcyzy + transport + mechanik + lakiernik + detailing + ogloszenia + koszt_rej + koszt_prz
dochod = cena_sprzedazy - suma_wydatki
marza_proc = (dochod / suma_wydatki * 100) if suma_wydatki > 0 else 0

# --- PANEL GŁÓWNY ---
st.markdown(f"<h2 style='text-align: center;'>Kalkulator Handlarza</h2>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align: center; color: gray;'>by Gerard S Digital Agency</p>", unsafe_allow_html=True)

c1, c2, c3 = st.columns([1.5, 2, 1.5])

with c1:
    st.bar_chart(pd.DataFrame({'PLN': [cena_pln, wartosc_akcyzy, transport, dochod]}, index=['Auto', 'Akcyza', 'Transport', 'Zysk']))

with c2:
    m1, m2 = st.columns(2)
    m1.markdown(f"<div class='metric-card'><div class='metric-label'>Przychód</div><div class='metric-value'>{cena_sprzedazy:,.0f} zł</div><div style='color:gray;font-size:12px;'>{marza_proc:.1f}% marży</div></div>", unsafe_allow_html=True)
    m2.markdown(f"<div class='metric-card'><div class='metric-label'>Dochód</div><div class='metric-value' style='color:#28a745;'>{dochod:,.0f} zł</div></div>", unsafe_allow_html=True)
    m3, m4 = st.columns(2)
    m3.markdown(f"<div class='metric-card'><div class='metric-label'>Vat (szac.)</div><div class='metric-value' style='font-size:18px;'>{(dochod*0.23):,.0f} zł</div></div>", unsafe_allow_html=True)
    m4.markdown(f"<div class='metric-card'><div class='metric-label'>Zdrowotna</div><div class='metric-value' style='font-size:18px;'>130 zł</div></div>", unsafe_allow_html=True)

with c3:
    fig = go.Figure(data=[go.Pie(labels=['Auto', 'Akcyza', 'Inne'], values=[cena_pln, wartosc_akcyzy, suma_wydatki-cena_pln-wartosc_akcyzy], hole=.4, marker_colors=['#cc0000', '#111111', '#dddddd'])])
    fig.update_layout(margin=dict(t=0, b=0, l=0, r=0), height=220, showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

t1, t2 = st.columns(2)
with t1:
    st.markdown("<div class='table-header'>Wydatki - podsumowanie</div>", unsafe_allow_html=True)
    st.markdown(f"""<div class='table-container'>
        <div class='row'><span>Samochód</span><span>{cena_pln:,.2f} zł</span></div>
        <div class='row'><span>Akcyza ({akcyza_typ})</span><span>{wartosc_akcyzy:,.2f} zł</span></div>
        <div class='row'><span>Transport</span><span>{transport:,.2f} zł</span></div>
        <div class='row'><span>Przegląd i Rejestracja</span><span>{koszt_prz + koszt_rej:,.2f} zł</span></div>
        <div class='row'><span>Inne koszty</span><span>{mechanik+lakiernik+detailing+ogloszenia:,.2f} zł</span></div>
        <div class='total-row'><span>Podsumowanie</span><span>{suma_wydatki:,.2f} zł</span></div>
    </div>""", unsafe_allow_html=True)

with t2:
    st.markdown("<div class='table-header'>Przychody - podsumowanie</div>", unsafe_allow_html=True)
    st.markdown(f"""<div class='table-container'>
        <div class='row'><span>Przychód</span><span>{cena_sprzedazy:,.2f} zł</span></div>
        <div class='row'><span>Dochód Brutto</span><span>{dochod:,.2f} zł</span></div>
        <div class='total-row' style='color:#000;'><span>Marża</span><span>{marza_proc:.1f}%</span></div>
    </div>""", unsafe_allow_html=True)
