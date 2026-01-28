import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Konfiguracja strony
st.set_page_config(page_title="Kalkulator Handlarza - Gerard S.", layout="wide")

# --- CUSTOM CSS (Odwzorowanie wyglądu arkusza) ---
st.markdown("""
    <style>
    /* Ciemny sidebar */
    [data-testid="stSidebar"] { background-color: #111111; color: white; border-right: 1px solid #333; }
    [data-testid="stSidebar"] .stMarkdown { color: white; }
    
    /* Karty wyników (Górne boxy) */
    .metric-card {
        background-color: white; padding: 20px; border-radius: 5px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1); border: 1px solid #ddd;
        text-align: center; margin-bottom: 10px;
    }
    .metric-label { font-size: 14px; color: #666; font-weight: bold; }
    .metric-value { font-size: 24px; color: #000; font-weight: bold; }
    
    /* Tabele podsumowujące */
    .summary-table { width: 100%; border-collapse: collapse; background: white; }
    .table-header { background-color: #cc0000; color: white; padding: 10px; font-weight: bold; text-align: left; }
    .table-row { border-bottom: 1px solid #eee; }
    .table-cell { padding: 8px; font-size: 14px; }
    .total-row { font-weight: bold; color: #28a745; border-top: 2px solid #eee; }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR (Panel wprowadzania danych) ---
with st.sidebar:
    st.markdown("### GERARD S. DIGITAL AGENCY")
    st.markdown("---")
    
    kurs_eur = st.number_input("Kurs Euro", value=4.32, step=0.01)
    cena_eur = st.number_input("Cena auta w EURO", value=5000)
    
    st.markdown("**Akcyza:**")
    akcyza_typ = st.radio("Wybierz stawkę", ["bez akcyzy", "do 2.0 l", "powyżej 2.0 l"], index=1)
    
    rejestracja_check = st.checkbox("Rejestracja", value=True)
    przeglad_check = st.checkbox("Przegląd", value=True)
    
    transport = st.number_input("Transport", value=1500)
    lakiernik = st.number_input("Lakierowanie (suma)", value=0)
    mechanik = st.number_input("Mechanik / Części", value=0)
    myjnia = st.number_input("Myjnia / Detailing", value=150)
    ogloszenia = st.number_input("Ogłoszenia", value=100)
    
    st.markdown("---")
    cena_sprzedazy = st.number_input("Cena sprzedaży auta", value=30000)

# --- LOGIKA OBLICZEŃ ---
cena_pln = cena_eur * kurs_eur
stawka_akc = 0.031 if akcyza_typ == "do 2.0 l" else (0.186 if akcyza_typ == "powyżej 2.0 l" else 0)
wartosc_akcyzy = cena_pln * stawka_akc
koszt_rej = 256 if rejestracja_check else 0
koszt_prz = 100 if przeglad_check else 0

suma_wydatki = cena_pln + wartosc_akcyzy + transport + lakiernik + mechanik + myjnia + ogloszenia + koszt_rej + koszt_prz
dochod = cena_sprzedazy - suma_wydatki
marza_proc = (dochod / suma_wydatki * 100) if suma_wydatki > 0 else 0

# --- PANEL GŁÓWNY (Układ wizualny) ---
st.title("Kalkulator Handlarza")
st.caption("by Gerard S Digital Agency")

# GÓRNY RZĄD: Wykres słupkowy | Metryki | Wykres kołowy
c_chart1, c_metrics, c_chart2 = st.columns([1.5, 2, 1.5])

with c_chart1:
    st.bar_chart(pd.DataFrame({'Wartość': [cena_pln, wartosc_akcyzy, transport, dochod]}, 
                               index=['Auto', 'Akcyza', 'Transport', 'Zysk']))

with c_metrics:
    m1, m2 = st.columns(2)
    m1.markdown(f"<div class='metric-card'><div class='metric-label'>Przychód</div><div class='metric-value'>{cena_sprzedazy:,.0f} zł</div><div style='color:green;font-size:12px;'>{marza_proc:.2f}% marży</div></div>", unsafe_allow_html=True)
    m2.markdown(f"<div class='metric-card'><div class='metric-label'>Dochód</div><div class='metric-value' style='color:green;'>{dochod:,.0f} zł</div></div>", unsafe_allow_html=True)
    
    m3, m4 = st.columns(2)
    # Uproszczone podatki jak w Twoim arkuszu
    st.markdown(f"<div class='metric-card'><div class='metric-label'>Wszystkie Koszty</div><div class='metric-value'>{suma_wydatki:,.0f} zł</div></div>", unsafe_allow_html=True)

with c_chart2:
    fig = go.Figure(data=[go.Pie(labels=['Auto', 'Akcyza', 'Inne'], values=[cena_pln, wartosc_akcyzy, suma_wydatki-cena_pln-wartosc_akcyzy], hole=.3)])
    fig.update_layout(margin=dict(t=0, b=0, l=0, r=0), height=200, showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# DOLNY RZĄD: Tabele podsumowujące
t1, t2 = st.columns(2)

with t1:
    st.markdown("<div class='table-header'>Wydatki - podsumowanie</div>", unsafe_allow_html=True)
    items = [
        ("Samochód", f"{cena_pln:,.2f} zł"),
        ("Akcyza", f"{wartosc_akcyzy:,.2f} zł"),
        ("Transport", f"{transport:,.2f} zł"),
        ("Lakiernik", f"{lakiernik:,.2f} zł"),
        ("Mechanik", f"{mechanik:,.2f} zł"),
        ("Rejestracja/Przegląd", f"{koszt_rej + koszt_prz:,.2f} zł")
    ]
    for name, val in items:
        st.markdown(f"<div class='table-row'><div style='display:flex;justify-content:space-between;padding:5px;'><span>{name}</span><span>{val}</span></div></div>", unsafe_allow_html=True)
    st.markdown(f"<div class='total-row' style='display:flex;justify-content:space-between;padding:10px;'><span>Podsumowanie</span><span>{suma_wydatki:,.2f} zł</span></div>", unsafe_allow_html=True)

with t2:
    st.markdown("<div class='table-header'>Przychody - podsumowanie</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='table-row' style='display:flex;justify-content:space-between;padding:10px;'><span>Przychód</span><span>{cena_sprzedazy:,.2f} zł</span></div>", unsafe_allow_html=True)
    st.markdown(f"<div class='table-row' style='display:flex;justify-content:space-between;padding:10px;'><span>Dochód</span><span>{dochod:,.2f} zł</span></div>", unsafe_allow_html=True)
    st.markdown("<br><p style='font-size:12px;color:grey;'>Wszystkie kwoty wyliczone na podstawie wprowadzonych danych.</p>", unsafe_allow_html=True)
