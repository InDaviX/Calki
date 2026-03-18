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
    </style>
    """, unsafe_allow_html=True)

st.sidebar.header("Parametry")
n = st.sidebar.slider("Liczba podziałów (n)", min_value=5, max_value=80, value=20, step=1)
metoda = st.sidebar.selectbox("Metoda", ["Lewostronna", "Środkowa", "Prawostronna"])

col_text, col_toggle = st.sidebar.columns([3, 1])
with col_text:
    st.markdown('<p class="toggle-label">Pokaż nadmiary i niedomiary</p>', unsafe_allow_html=True)
with col_toggle:
    pokaz_bledy = st.toggle("", value=True, label_visibility="collapsed")
st.sidebar.divider()

tab1, tab2 = st.tabs(["Funkcja Prosta", "Funkcja Skomplikowana"])

with tab1:
    st.markdown(r"<span style='font-size: 22px;'>📈 Wykres i wzór funkcji prostej: &nbsp; $\boldsymbol{f(x) = x \cdot e^{-x}}$</span>", unsafe_allow_html=True)
    
    a, b = 0, 10
    x_plot = m.linspace(a, b, 500)
    y_plot = funkcja_prosta(x_plot)
    
    dx = (b - a) / n
    x_bins = m.linspace(a, b, n + 1)
    
    if metoda == "Lewostronna":
        heights = funkcja_prosta(x_bins[:-1])
    elif metoda == "Prawostronna":
        heights = funkcja_prosta(x_bins[1:])
    elif metoda == "Środkowa":
        heights = funkcja_prosta(x_bins[:-1] + (dx / 2))
        
    wynik_num_1 = m.sum(heights) * dx
    wynik_ana_1 = (-m.exp(-b)*(b+1)) - (-m.exp(-a)*(a+1))
        
    fig, ax = plt.subplots()
    ax.plot(x_plot, y_plot, color='royalblue', linewidth=2)
    
    s_prosta, d_prosta = 0, 0
    
    for i in range(n):
        xi, xf, h = x_bins[i], x_bins[i+1], heights[i]
        step_x = m.linspace(xi, xf, 100)
        step_f = funkcja_prosta(step_x)
        diff = h - step_f
        s_prosta += m.sum(m.maximum(0, diff)) * (dx / 100)
        d_prosta += m.sum(m.maximum(0, -diff)) * (dx / 100)
        
        ax.bar(xi, h, width=dx, align='edge', color='lightgreen', edgecolor='black', alpha=0.6)
        
        if pokaz_bledy:
            ax.fill_between(step_x, step_f, h, where=(h > step_f), color='cyan', alpha=0.4)
            ax.fill_between(step_x, h, step_f, where=(step_f > h), color='red', alpha=0.4)

    ax.set_xlim(a, b)
    ax.set_ylim(-0.01, 0.4)
    ax.grid(True, linestyle='--', alpha=0.6)
    st.pyplot(fig)

    st.latex(r"I = \int_{0}^{10} x e^{-x} \, dx = \left[ -e^{-x}(x+1) \right]_{0}^{10} \approx " + f"{wynik_ana_1:.6f}")
    st.write(f"**Wynik numeryczny ({metoda}):** {wynik_num_1:.6f}")

    if pokaz_bledy:
        c1, c2, c3 = st.columns(3)
        c1.markdown(f"🔵 **Suma nadmiarów:** \n{s_prosta:.6f}")
        c2.markdown(f"🔴 **Suma niedomiarów:** \n{d_prosta:.6f}")
        c3.markdown(f"⚖️ **Błąd przybliżenia:** \n{s_prosta - d_prosta:.6f}")

with tab2:
    st.markdown(r"<span style='font-size: 22px;'>📉 Wykres i wzór funkcji skomplikowanej: &nbsp; $\boldsymbol{f(x) = e^x \cdot \cos(e^x)}$</span>", unsafe_allow_html=True)
    
    a_c, b_c = 0, 2.5
    x_comp_plot = m.linspace(a_c, b_c, 2000)
    y_comp_plot = funkcja_skomplikowana(x_comp_plot)
    
    dx_c = (b_c - a_c) / n
    x_bins_c = m.linspace(a_c, b_c, n + 1)
    
    if metoda == "Lewostronna":
        heights_c = funkcja_skomplikowana(x_bins_c[:-1])
    elif metoda == "Prawostronna":
        heights_c = funkcja_skomplikowana(x_bins_c[1:])
    elif metoda == "Środkowa":
        heights_c = funkcja_skomplikowana(x_bins_c[:-1] + (dx_c / 2))
        
    wynik_num_2 = m.sum(heights_c) * dx_c
    wynik_ana_2 = m.sin(m.exp(b_c)) - m.sin(m.exp(a_c))
        
    fig2, ax2 = plt.subplots()
    ax2.plot(x_comp_plot, y_comp_plot, color='darkorange', linewidth=1)
    
    s_skompl, d_skompl = 0, 0
    
    for i in range(n):
        xi_c, xf_c, h_c = x_bins_c[i], x_bins_c[i+1], heights_c[i]
        step_x_c = m.linspace(xi_c, xf_c, 100)
        step_f_c = funkcja_skomplikowana(step_x_c)
        diff_c = h_c - step_f_c
        s_skompl += m.sum(m.maximum(0, diff_c)) * (dx_c / 100)
        d_skompl += m.sum(m.maximum(0, -diff_c)) * (dx_c / 100)
        
        ax2.bar(xi_c, h_c, width=dx_c, align='edge', color='lightgreen', edgecolor='black', alpha=0.6)
        
        if pokaz_bledy:
            ax2.fill_between(step_x_c, step_f_c, h_c, where=(h_c > step_f_c), color='cyan', alpha=0.4)
            ax2.fill_between(step_x_c, h_c, step_f_c, where=(step_f_c > h_c), color='red', alpha=0.4)

    ax2.set_xlim(a_c, b_c)
    ax2.set_ylim(-13, 13)
    ax2.grid(True)
    st.pyplot(fig2)

    st.latex(r"I = \int_{0}^{2.5} e^x \cos(e^x) \, dx = \left[ \sin(e^x) \right]_{0}^{2.5} \approx " + f"{wynik_ana_2:.6f}")
    st.write(f"**Wynik numeryczny ({metoda}):** {wynik_num_2:.6f}")

    if pokaz_bledy:
        k1, k2, k3 = st.columns(3)
        k1.markdown(f"🔵 **Suma nadmiarów:** \n{s_skompl:.6f}")
        k2.markdown(f"🔴 **Suma niedomiarów:** \n{d_skompl:.6f}")
        k3.markdown(f"⚖️ **Błąd przybliżenia:** \n{s_skompl - d_skompl:.6f}")