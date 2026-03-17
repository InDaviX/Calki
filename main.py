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
    /* Kontener listy zakładek */
    div[data-baseweb="tab-list"] {
        width: 100%;
        gap: 0px;
    }
    /* Pojedynczy przycisk zakładki */
    div[data-baseweb="tab-list"] button {
        flex: 1;
        text-align: center;
    }
    /* Opcjonalnie: zmiana wielkości czcionki w zakładkach */
    div[data-baseweb="tab-list"] button p {
        font-size: 20px;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)
tab1, tab2 = st.tabs(["Funkcja Prosta", "Funkcja Skomplikowana"])




st.sidebar.header("Parametry")
n = st.sidebar.slider(
    "Liczba podziałów (n)", 
    min_value=2, 
    max_value=50, 
    value=5, 
    step=1
)
metoda = st.sidebar.selectbox("Metoda", ["Lewostronna", "Prawostronna", "Środkowa"])




with tab1:
    st.markdown(r"<span style='font-size: 22px;'>📈 Wykres i wzór funkcji prostej: &nbsp; $\boldsymbol{f(x) = x \cdot e^{-x}}$</span>", unsafe_allow_html=True)
    a_simple, b_simple = 0, 10
    
    x_plot = m.linspace(a_simple, b_simple, 500)
    y_plot = funkcja_prosta(x_plot)
    
    dx = (b_simple - a_simple) / n
    x_bins = m.linspace(a_simple, b_simple, n + 1)
    
    if metoda == "Lewostronna":
        heights = funkcja_prosta(x_bins[:-1]) 
        bar_color = "skyblue"
    elif metoda == "Prawostronna":
        heights = funkcja_prosta(x_bins[1:])
        bar_color = "salmon"
    elif metoda == "Środkowa":
        x_mids = x_bins[:-1] + (dx / 2)
        heights = funkcja_prosta(x_mids)
        bar_color = "lightgreen"
        
    fig, ax = plt.subplots()

    ax.plot(x_plot, y_plot, color='royalblue', linewidth=2, label="Funkcja f(x)")
    

    ax.bar(x_bins[:-1], heights, width=dx, align='edge',
           alpha=0.4, color=bar_color, edgecolor='black',
           label=f"Przybliżenie: {metoda}")
    
    ax.set_xlim(a_simple, b_simple)
    ax.set_ylim(-0.01, 0.4)
    ax.set_title(f"Metoda Prostokątów: {metoda} (n={n})")
    ax.legend()
    ax.grid(True, linestyle='--')
    
    st.pyplot(fig)



with tab2:
    st.markdown(r"<span style='font-size: 22px;'>📉 Wykres i wzór funkcji skomplikowanej: &nbsp; $\boldsymbol{f(x) = e^x \cdot \cos(e^x)}$</span>", unsafe_allow_html=True)
    
    x_comp = m.linspace(0, 2.5, 1000)
    y_comp = funkcja_skomplikowana(x_comp)
    
    fig2, ax2 = plt.subplots()
    ax2.plot(x_comp, y_comp, color='darkorange')
    ax2.set_title("Szybkie oscylacje")
    
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