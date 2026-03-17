import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.title("Wizualizacja Całkowania Numerycznego")

# Suwak do liczby podziałów
n = st.slider("Wybierz liczbę podziałów (n)", min_value=2, max_value=100, value=10)

# Definicja funkcji (np. ta "prosta")
def f(x):
    return x**2

x = np.linspace(0, 1, 100)
x_bins = np.linspace(0, 1, n)
y_bins = f(x_bins)

fig, ax = plt.subplots()
ax.plot(x, f(x), 'r', label="f(x) = x^2")
ax.bar(x_bins[:-1], y_bins[:-1], width=(1/n), align='edge', alpha=0.3, edgecolor='blue')

st.pyplot(fig)

# Tutaj możesz liczyć błąd i wyświetlać go dynamicznie
st.write(f"Błąd bezwzględny dla n={n} wynosi: ...")