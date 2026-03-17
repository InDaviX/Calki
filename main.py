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
    </style>
    """, unsafe_allow_html=True)

st.sidebar.header("Parametry")
n = st.sidebar.slider("Liczba podziałów (n)", min_value=5, max_value=80, value=20, step=1)
metoda = st.sidebar.selectbox("Metoda", ["Lewostronna", "Środkowa", "Prawostronna"])
pokaz_bledy = st.sidebar.toggle("Pokaż nadmiary i niedomiary", value=True)

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
        
    fig, ax = plt.subplots()
    ax.plot(x_plot, y_plot, color='royalblue', linewidth=2)
    
    for i in range(n):
        xi = x_bins[i]
        xf = x_bins[i+1]
        h = heights[i]
        
        ax.bar(xi, h, width=dx, align='edge', color='lightgreen', edgecolor='black', alpha=0.6)
        
        if pokaz_bledy:
            step_x = m.linspace(xi, xf, 10)
            step_f = funkcja_prosta(step_x)
            step_h = m.full_like(step_x, h)
            ax.fill_between(step_x, step_f, step_h, where=(step_h > step_f), color='cyan', alpha=0.4, interpolate=True)
            ax.fill_between(step_x, step_h, step_f, where=(step_f > step_h), color='red', alpha=0.4, interpolate=True)

    ax.set_xlim(a, b)
    ax.set_ylim(-0.01, 0.4)
    ax.set_title(f"Metoda Prostokątów: {metoda} (n={n})")
    ax.grid(True, linestyle='--', alpha=0.6)
    st.pyplot(fig)

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
        
    fig2, ax2 = plt.subplots()
    ax2.plot(x_comp_plot, y_comp_plot, color='darkorange', linewidth=1)
    
    for i in range(n):
        xi_c = x_bins_c[i]
        xf_c = x_bins_c[i+1]
        h_c = heights_c[i]
        
        ax2.bar(xi_c, h_c, width=dx_c, align='edge', color='lightgreen', edgecolor='black', alpha=0.6)
        
        if pokaz_bledy:
            step_x_c = m.linspace(xi_c, xf_c, 10)
            step_f_c = funkcja_skomplikowana(step_x_c)
            step_h_c = m.full_like(step_x_c, h_c)
            ax2.fill_between(step_x_c, step_f_c, step_h_c, where=(step_h_c > step_f_c), color='cyan', alpha=0.4, interpolate=True)
            ax2.fill_between(step_x_c, step_h_c, step_f_c, where=(step_f_c > step_h_c), color='red', alpha=0.4, interpolate=True)

    ax2.set_xlim(a_c, b_c)
    ax2.set_ylim(-13, 13)
    ax2.set_title(f"Szybkie oscylacje: {metoda} (n={n})")
    ax2.grid(True)
    st.pyplot(fig2)







# st.set_page_config(page_title="Zadanie: Całkowanie Numeryczne", layout="wide")

# st.title("🧮 Wizualizacja Całkowania Numerycznego")
# st.markdown("Student: Dawid | Przedmiot: Analiza Matematyczna")

# # --- PARAMETRY W PANELU BOCZNYM ---
# st.sidebar.header("Ustawienia obliczeń")
# n_bins = st.sidebar.slider("Liczba podziałów (n)", 2, 100, 10)
# n_mc = st.sidebar.number_input("Liczba punktów Monte Carlo", 100, 10000, 1000)

# # --- DEFINICJA FUNKCJI ---
# def f_simple(x):
#     return x**2

# # Rozwiązanie analityczne dla x^2 na [0, 1] to 1/3
# exact_val = 1/3

# # --- WIZUALIZACJA METODY PROSTOKĄTÓW ---
# st.subheader("1. Metoda Prostokątów (Wariant Lewostronny)")

# x = np.linspace(0, 1, 500)
# y = f_simple(x)

# fig1, ax1 = plt.subplots(figsize=(10, 4))
# ax1.plot(x, y, 'r', label="$f(x) = x^2$")

# # Rysowanie prostokątów
# x_bins = np.linspace(0, 1, n_bins + 1)
# dx = 1 / n_bins
# for i in range(n_bins):
#     xi = x_bins[i]
#     yi = f_simple(xi)
#     ax1.add_patch(plt.Rectangle((xi, 0), dx, yi, edgecolor='blue', facecolor='blue', alpha=0.2))

# ax1.set_title(f"Podział na {n_bins} prostokątów")
# ax1.legend()
# st.pyplot(fig1)

# # --- WIZUALIZACJA MONTE CARLO ---
# st.subheader("2. Metoda Monte Carlo")

# x_rand = np.random.uniform(0, 1, n_mc)
# y_rand = np.random.uniform(0, 1, n_mc) # f(x) na [0,1] nie przekracza 1
# under_curve = y_rand <= f_simple(x_rand)

# fig2, ax2 = plt.subplots(figsize=(10, 4))
# ax2.plot(x, y, color='black', lw=2)
# ax2.scatter(x_rand[under_curve], y_rand[under_curve], color='green', s=1, alpha=0.5, label="Trafione")
# ax2.scatter(x_rand[~under_curve], y_rand[~under_curve], color='red', s=1, alpha=0.3, label="Chybione")
# ax2.legend()
# st.pyplot(fig2)

# # --- WYNIKI ---
# st.divider()
# approx_rect = sum([f_simple(x_bins[i]) * dx for i in range(n_bins)])
# approx_mc = np.sum(under_curve) / n_mc

# col1, col2, col3 = st.columns(3)
# col1.metric("Wartość Dokładna", f"{exact_val:.4f}")
# col2.metric("Metoda Prostokątów", f"{approx_rect:.4f}", f"{approx_rect - exact_val:.4f}", delta_color="inverse")
# col3.metric("Metoda Monte Carlo", f"{approx_mc:.4f}", f"{approx_mc - exact_val:.4f}", delta_color="inverse")