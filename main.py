import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.title("🧮 Wizualizacja Metod Całkowania Numerycznego")
st.markdown("Porównanie działania metody prostokątów (w 3 wariantach), metody trapezów oraz metody monte carlo")

st.sidebar.header("Parametry")
n = st.sidebar.number_input("Liczba podziałów", min_value=2, value=10)
metoda = st.sidebar.selectbox("Metoda", ["Lewostronna", "Prawostronna", "Środkowa"])


tab1, tab2 = st.tabs(["Funkcja Prosta", "Funkcja Skomplikowana"])
with tab1:
    st.write("Tu będzie wykres x^2")









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