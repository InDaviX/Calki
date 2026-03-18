import streamlit as st
import numpy as m
import matplotlib.pyplot as plt

def funkcja_prosta(x):
    return x * m.exp(-1 * x)

def funkcja_skomplikowana(x):
    return m.exp(x) * m.cos(m.exp(x))

st.title("🧮 Wizualizacja Metod Całkowania Numerycznego")

st.markdown("""
    <style>
    div[data-baseweb="tab-list"] {
        width: 100%;
        gap: 0px;
    }
    div[data-baseweb="tab-list"] button {
        flex: 1;
        text-align: center;
    }
    div[data-baseweb="tab-list"] button p {
        font-size: 20px;
        font-weight: bold;
    }
    div[data-testid="stSelectbox"] {
        margin-bottom: 30px;
    }
    .toggle-label {
        font-size: 16px;
        margin-top: 5px;
    }
    .result-label {
        font-size: 16px;
        color: var(--text-color);
        opacity: 0.7;
    }
    .result-value {
        font-size: 20px;
        font-weight: bold;
        color: var(--text-color);
    }
    .right-panel {
        position: fixed;
        top: 80px;
        right: 20px;
        width: 320px;
        padding: 15px;
        background-color: var(--secondary-background-color);
        color: var(--text-color);
        border: 1px solid var(--border-color);
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.3);
        z-index: 999;
        font-size: 13px;
    }
    [data-testid="stLatex"] {
        overflow-x: hidden !important;
        width: 100%;
    }
    </style>
    """, unsafe_allow_html=True)

st.sidebar.header("Parametry")
n = st.sidebar.slider("Liczba podziałów (n)", min_value=5, max_value=80, value=20, step=1)
metoda_rect = st.sidebar.selectbox("Metoda Prostokątów", ["Lewostronna", "Środkowa", "Prawostronna"])

col_text, col_toggle = st.sidebar.columns([3, 1])
with col_text:
    st.markdown('<p class="toggle-label">Pokaż nadmiary i niedomiary</p>', unsafe_allow_html=True)
with col_toggle:
    pokaz_bledy = st.toggle("", value=True, label_visibility="collapsed")
st.sidebar.divider()

tab1, tab2 = st.tabs(["Funkcja Prosta", "Funkcja Skomplikowana"])

with tab1:
    st.markdown(r"<span style='font-size: 22px;'>📈 Analiza funkcji prostej: &nbsp; $\boldsymbol{f(x) = x \cdot e^{-x}}$</span>", unsafe_allow_html=True)
    a, b = 0, 10
    x_plot = m.linspace(a, b, 500)
    y_plot = funkcja_prosta(x_plot)
    dx = (b - a) / n
    x_bins = m.linspace(a, b, n + 1)
    y_ana = (-m.exp(-b)*(b+1)) - (-m.exp(-a)*(a+1))

    if metoda_rect == "Lewostronna":
        h_rect = funkcja_prosta(x_bins[:-1])
    elif metoda_rect == "Prawostronna":
        h_rect = funkcja_prosta(x_bins[1:])
    else:
        h_rect = funkcja_prosta(x_bins[:-1] + dx/2)
    res_rect = m.sum(h_rect) * dx
    
    st.subheader(f"1. Metoda Prostokątów ({metoda_rect})")
    fig1, ax1 = plt.subplots()
    ax1.plot(x_plot, y_plot, color='royalblue', linewidth=2)
    s_p, d_p = 0, 0
    for i in range(n):
        xi, xf, h = x_bins[i], x_bins[i+1], h_rect[i]
        sx = m.linspace(xi, xf, 50)
        sf = funkcja_prosta(sx)
        diff = h - sf
        s_p += m.sum(m.maximum(0, diff)) * (dx/50)
        d_p += m.sum(m.maximum(0, -diff)) * (dx/50)
        ax1.bar(xi, h, width=dx, align='edge', color='lightgreen', edgecolor='black', alpha=0.4)
        if pokaz_bledy:
            ax1.fill_between(sx, sf, h, where=(h > sf), color='cyan', alpha=0.4)
            ax1.fill_between(sx, h, sf, where=(sf > h), color='red', alpha=0.4)
    ax1.set_xlim(a, b); ax1.set_ylim(-0.01, 0.4); ax1.grid(True, alpha=0.3)
    st.pyplot(fig1)

    st.latex(r"I_{exact} = \int_{0}^{10} x e^{-x} \, dx = \left[ -e^{-x}(x+1) \right]_{0}^{10} = " + f"{y_ana:.10f}")
    
    r1, r2 = st.columns(2)
    r1.markdown(f"<p class='result-label'>Przybliżenie Prostokątów:</p><p class='result-value'>{res_rect:.10f}</p>", unsafe_allow_html=True)
    r2.markdown(f"<p class='result-label'>Wartość dokładna:</p><p class='result-value'>{y_ana:.10f}</p>", unsafe_allow_html=True)

    st.divider()
    
    st.subheader("2. Metoda Trapezów")
    h_trap = funkcja_prosta(x_bins)
    res_trap = (dx / 2) * (h_trap[0] + 2 * m.sum(h_trap[1:-1]) + h_trap[-1])
    
    fig1t, ax1t = plt.subplots()
    ax1t.plot(x_plot, y_plot, color='royalblue', linewidth=2)
    s_pt, d_pt = 0, 0
    for i in range(n):
        xi, xf = x_bins[i], x_bins[i+1]
        yi, yf = h_trap[i], h_trap[i+1]
        sx = m.linspace(xi, xf, 50)
        sf = funkcja_prosta(sx)
        ltrap = yi + (yf - yi) * (sx - xi) / dx
        diff = ltrap - sf
        s_pt += m.sum(m.maximum(0, diff)) * (dx/50)
        d_pt += m.sum(m.maximum(0, -diff)) * (dx/50)
        ax1t.fill_between([xi, xf], [0, 0], [yi, yf], color='lightgreen', edgecolor='black', alpha=0.4)
        if pokaz_bledy:
            ax1t.fill_between(sx, sf, ltrap, where=(ltrap > sf), color='cyan', alpha=0.4)
            ax1t.fill_between(sx, ltrap, sf, where=(sf > ltrap), color='red', alpha=0.4)
    ax1t.set_xlim(a, b); ax1t.set_ylim(-0.01, 0.4); ax1t.grid(True, alpha=0.3)
    st.pyplot(fig1t)

    t1, t2 = st.columns(2)
    t1.markdown(f"<p class='result-label'>Przybliżenie Trapezów:</p><p class='result-value'>{res_trap:.10f}</p>", unsafe_allow_html=True)
    t2.markdown(f"<p class='result-label'>Wartość dokładna:</p><p class='result-value'>{y_ana:.10f}</p>", unsafe_allow_html=True)

    if pokaz_bledy:
        st.markdown(f"""<div class="right-panel"><h3 style='margin-top:0'>📊 Statystyki błędu</h3>
            <p><b>Metoda Prostokątów ({metoda_rect}):</b><br>
            🔵 Nadmiar: {s_p:.10f}<br>🔴 Niedomiar: {d_p:.10f}<br>⚖️ Błąd: {res_rect - y_ana:.10f}</p>
            <hr style="border:0.5px solid var(--border-color)">
            <p><b>Metoda Trapezów:</b><br>
            🔵 Nadmiar: {s_pt:.10f}<br>🔴 Niedomiar: {d_pt:.10f}<br>⚖️ Błąd: {res_trap - y_ana:.10f}</p></div>""", unsafe_allow_html=True)

with tab2:
    st.markdown(r"<span style='font-size: 22px;'>📉 Analiza funkcji skomplikowanej: &nbsp; $\boldsymbol{f(x) = e^x \cdot \cos(e^x)}$</span>", unsafe_allow_html=True)
    a_c, b_c = 0, 2.5
    x_c_plot = m.linspace(a_c, b_c, 2000)
    y_c_plot = funkcja_skomplikowana(x_c_plot)
    dx_c = (b_c - a_c) / n
    x_bc = m.linspace(a_c, b_c, n + 1)
    y_ana_c = m.sin(m.exp(b_c)) - m.sin(m.exp(a_c))

    if metoda_rect == "Lewostronna":
        h_rc = funkcja_skomplikowana(x_bc[:-1])
    elif metoda_rect == "Prawostronna":
        h_rc = funkcja_skomplikowana(x_bc[1:])
    else:
        h_rc = funkcja_skomplikowana(x_bc[:-1] + dx_c/2)
    res_rc = m.sum(h_rc) * dx_c

    st.subheader(f"1. Metoda Prostokątów ({metoda_rect})")
    fig2, ax2 = plt.subplots()
    ax2.plot(x_c_plot, y_c_plot, color='darkorange', linewidth=1)
    s_c, d_c = 0, 0
    for i in range(n):
        xi, xf, h = x_bc[i], x_bc[i+1], h_rc[i]
        sx = m.linspace(xi, xf, 50)
        sf = funkcja_skomplikowana(sx)
        diff = h - sf
        s_c += m.sum(m.maximum(0, diff)) * (dx_c/50)
        d_c += m.sum(m.maximum(0, -diff)) * (dx_c/50)
        ax2.bar(xi, h, width=dx_c, align='edge', color='lightgreen', edgecolor='black', alpha=0.4)
        if pokaz_bledy:
            ax2.fill_between(sx, sf, h, where=(h > sf), color='cyan', alpha=0.4)
            ax2.fill_between(sx, h, sf, where=(sf > h), color='red', alpha=0.4)
    ax2.set_xlim(a_c, b_c); ax2.set_ylim(-13, 13); ax2.grid(True, alpha=0.2)
    st.pyplot(fig2)

    st.latex(r"I_{exact} = \int_{0}^{2.5} e^x \cos(e^x) \, dx = \left[ \sin(e^x) \right]_{0}^{2.5} = " + f"{y_ana_c:.10f}")

    r1_c, r2_c = st.columns(2)
    r1_c.markdown(f"<p class='result-label'>Przybliżenie Prostokątów:</p><p class='result-value'>{res_rc:.10f}</p>", unsafe_allow_html=True)
    r2_c.markdown(f"<p class='result-label'>Wartość dokładna:</p><p class='result-value'>{y_ana_c:.10f}</p>", unsafe_allow_html=True)

    st.divider()

    st.subheader("2. Metoda Trapezów")
    h_tc = funkcja_skomplikowana(x_bc)
    res_tc = (dx_c / 2) * (h_tc[0] + 2 * m.sum(h_tc[1:-1]) + h_tc[-1])
    
    fig2t, ax2t = plt.subplots()
    ax2t.plot(x_c_plot, y_c_plot, color='darkorange', linewidth=1)
    s_ct, d_ct = 0, 0
    for i in range(n):
        xi, xf = x_bc[i], x_bc[i+1]
        yi, yf = h_tc[i], h_tc[i+1]
        sx = m.linspace(xi, xf, 50)
        sf = funkcja_skomplikowana(sx)
        ltrap = yi + (yf - yi) * (sx - xi) / dx_c
        diff = ltrap - sf
        s_ct += m.sum(m.maximum(0, diff)) * (dx_c/50)
        d_ct += m.sum(m.maximum(0, -diff)) * (dx_c/50)
        ax2t.fill_between([xi, xf], [0, 0], [yi, yf], color='lightgreen', edgecolor='black', alpha=0.4)
        if pokaz_bledy:
            ax2t.fill_between(sx, sf, ltrap, where=(ltrap > sf), color='cyan', alpha=0.4)
            ax2t.fill_between(sx, ltrap, sf, where=(sf > ltrap), color='red', alpha=0.4)
    ax2t.set_xlim(a_c, b_c); ax2t.set_ylim(-13, 13); ax2t.grid(True, alpha=0.2)
    st.pyplot(fig2t)

    t1_c, t2_c = st.columns(2)
    t1_c.markdown(f"<p class='result-label'>Przybliżenie Trapezów:</p><p class='result-value'>{res_tc:.10f}</p>", unsafe_allow_html=True)
    t2_c.markdown(f"<p class='result-label'>Wartość dokładna:</p><p class='result-value'>{y_ana_c:.10f}</p>", unsafe_allow_html=True)

    if pokaz_bledy:
        st.markdown(f"""<div class="right-panel"><h3 style='margin-top:0'>📊 Statystyki błędu</h3>
            <p><b>Metoda Prostokątów ({metoda_rect}):</b><br>
            🔵 Nadmiar: {s_c:.10f}<br>🔴 Niedomiar: {d_c:.10f}<br>⚖️ Błąd: {res_rc - y_ana_c:.10f}</p>
            <hr style="border:0.5px solid var(--border-color)">
            <p><b>Metoda Trapezów:</b><br>
            🔵 Nadmiar: {s_ct:.10f}<br>🔴 Niedomiar: {d_ct:.10f}<br>⚖️ Błąd: {res_tc - y_ana_c:.10f}</p></div>""", unsafe_allow_html=True)