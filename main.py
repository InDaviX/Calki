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
    /* Zakładki 50/50 */
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
    
    /* Margines w sidebarze */
    div[data-testid="stSelectbox"] {
        margin-bottom: 30px;
    }
    .toggle-label {
        font-size: 16px;
        margin-top: 5px;
    }

    /* FORMATOWANIE WYNIKÓW - MOTYW-AWARE */
    .result-label {
        font-size: 18px;
        color: var(--text-color);
        opacity: 0.8;
    }
    .result-value {
        font-size: 24px;
        font-weight: bold;
        color: var(--text-color);
    }

    /* PRAWY PANEL - REAGUJE NA MOTYW */
    .right-panel {
        position: fixed;
        top: 100px;
        right: 30px;
        width: 280px;
        padding: 20px;
        /* Używamy zmiennych systemowych Streamlita */
        background-color: var(--secondary-background-color);
        color: var(--text-color);
        border: 1px solid var(--border-color);
        border-radius: 15px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.3);
        z-index: 999;
    }

    /* POZBYCIE SIĘ SUWAKA POD LATEX */
    [data-testid="stLatex"] {
        overflow-x: hidden !important;
    }
    [data-testid="stLatex"] > div {
        overflow-y: hidden !important;
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
    
    fig, ax = plt.subplots(facecolor='none') # Przezroczyste tło wykresu pod motyw
    ax.set_facecolor('none')
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
    
    # Dostosowanie kolorów osi do motywu
    ax.tick_params(colors='gray')
    ax.xaxis.label.set_color('gray')
    ax.yaxis.label.set_color('gray')
    
    ax.set_xlim(a, b)
    ax.set_ylim(-0.01, 0.4)
    ax.grid(True, linestyle='--', alpha=0.3)
    st.pyplot(fig)

    if pokaz_bledy:
        st.markdown(f"""
            <div class="right-panel">
                <h3 style='margin-top:0'>📊 Statystyki błędu</h3>
                <p>🔵 <b>Suma nadmiarów:</b><br>{s_prosta:.6f}</p>
                <p>🔴 <b>Suma niedomiarów:</b><br>{d_prosta:.6f}</p>
                <hr style="border: 0.5px solid var(--border-color)">
                <p>⚖️ <b>Błąd przybliżenia:</b><br>{s_prosta - d_prosta:.6f}</p>
            </div>
            """, unsafe_allow_html=True)

    st.markdown(f"### Podsumowanie: {metoda} (n={n})")
    r1, r2 = st.columns(2)
    r1.markdown(f"<p class='result-label'>Wynik numeryczny:</p><p class='result-value'>{wynik_num_1:.6f}</p>", unsafe_allow_html=True)
    r2.markdown(f"<p class='result-label'>Wynik oczekiwany:</p><p class='result-value'>{wynik_ana_1:.6f}</p>", unsafe_allow_html=True)
    st.latex(r"I = \int_{0}^{10} x e^{-x} \, dx = \left[ -e^{-x}(x+1) \right]_{0}^{10}")

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
        
    fig2, ax2 = plt.subplots(facecolor='none')
    ax2.set_facecolor('none')
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
    
    ax2.tick_params(colors='gray')
    ax2.set_xlim(a_c, b_c)
    ax2.set_ylim(-13, 13)
    ax2.grid(True, alpha=0.2)
    st.pyplot(fig2)

    if pokaz_bledy:
        st.markdown(f"""
            <div class="right-panel">
                <h3 style='margin-top:0'>📊 Statystyki błędu</h3>
                <p>🔵 <b>Suma nadmiarów:</b><br>{s_skompl:.6f}</p>
                <p>🔴 <b>Suma niedomiarów:</b><br>{d_skompl:.6f}</p>
                <hr style="border: 0.5px solid var(--border-color)">
                <p>⚖️ <b>Błąd przybliżenia:</b><br>{s_skompl - d_skompl:.6f}</p>
            </div>
            """, unsafe_allow_html=True)

    st.markdown(f"### Podsumowanie: {metoda} (n={n})")
    k1, k2 = st.columns(2)
    k1.markdown(f"<p class='result-label'>Wynik numeryczny:</p><p class='result-value'>{wynik_num_2:.6f}</p>", unsafe_allow_html=True)
    k2.markdown(f"<p class='result-label'>Wynik oczekiwany:</p><p class='result-value'>{wynik_ana_2:.6f}</p>", unsafe_allow_html=True)
    st.latex(r"I = \int_{0}^{2.5} e^x \cos(e^x) \, dx = \left[ \sin(e^x) \right]_{0}^{2.5}")