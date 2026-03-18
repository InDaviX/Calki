import streamlit as st
import numpy as m
import matplotlib.pyplot as plt
import time




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
    [data-testid="stLatex"] > div {
        overflow-y: hidden !important;
    }
    </style>
    """, unsafe_allow_html=True)
tab1, tab2 = st.tabs(["Funkcja Prosta", "Funkcja Skomplikowana"])
st.sidebar.header("Parametry")
n = st.sidebar.slider("Liczba podziałów (n)", min_value=5, max_value=80, value=20, step=1)
metoda_rect = st.sidebar.selectbox("Metoda Prostokątów", ["Lewostronna", "Środkowa", "Prawostronna"])
col_text, col_toggle = st.sidebar.columns([3, 1])
with col_text:
    st.markdown('<p class="toggle-label">Pokaż nadmiary i niedomiary</p>', unsafe_allow_html=True)
with col_toggle:
    pokaz_bledy = st.toggle("", value=True, label_visibility="collapsed")
st.sidebar.divider()
n_mc = st.sidebar.slider("Liczba punktów Monte Carlo", min_value=100, max_value=25000, value=1500, step=100)







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
            ax1.fill_between(sx, sf, h, where=(h > sf), color='cyan', alpha=0.3)
            ax1.fill_between(sx, h, sf, where=(sf > h), color='red', alpha=0.3)
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
            ax1t.fill_between(sx, sf, ltrap, where=(ltrap > sf), color='cyan', alpha=0.3)
            ax1t.fill_between(sx, ltrap, sf, where=(sf > ltrap), color='red', alpha=0.3)
    ax1t.set_xlim(a, b); ax1t.set_ylim(-0.01, 0.4); ax1t.grid(True, alpha=0.3)
    st.pyplot(fig1t)

    t1, t2 = st.columns(2)
    t1.markdown(f"<p class='result-label'>Przybliżenie Trapezów:</p><p class='result-value'>{res_trap:.10f}</p>", unsafe_allow_html=True)
    t2.markdown(f"<p class='result-label'>Wartość dokładna:</p><p class='result-value'>{y_ana:.10f}</p>", unsafe_allow_html=True)

    st.divider()

    st.subheader("3. Metoda Monte Carlo")
    y_min_mc, y_max_mc = 0, 0.4
    x_mc = m.random.uniform(a, b, n_mc)
    y_mc = m.random.uniform(y_min_mc, y_max_mc, n_mc)
    f_val_mc = funkcja_prosta(x_mc)
    
    is_under = y_mc <= f_val_mc
    hits = m.sum(is_under)
    pole_box = (b - a) * (y_max_mc - y_min_mc)
    res_mc = pole_box * (hits / n_mc)

    fig1mc, ax1mc = plt.subplots()
    ax1mc.plot(x_plot, y_plot, color='royalblue', linewidth=2)
    ax1mc.scatter(x_mc[is_under], y_mc[is_under], color='green', s=2, alpha=0.5, label='Pod wykresem')
    ax1mc.scatter(x_mc[~is_under], y_mc[~is_under], color='orange', s=2, alpha=0.5, label='Nad wykresem')
    ax1mc.set_xlim(a, b); ax1mc.set_ylim(-0.01, 0.4); ax1mc.grid(True, alpha=0.3)
    st.pyplot(fig1mc)

    mc1, mc2 = st.columns(2)
    mc1.markdown(f"<p class='result-label'>Przybliżenie Monte Carlo:</p><p class='result-value'>{res_mc:.10f}</p>", unsafe_allow_html=True)
    mc2.markdown(f"<p class='result-label'>Wartość dokładna:</p><p class='result-value'>{y_ana:.10f}</p>", unsafe_allow_html=True)

    if pokaz_bledy:
        st.markdown(f"""<div class="right-panel"><h3 style='margin-top:0'>📊 Statystyki błędu</h3>
            <p><b>Metoda Prostokątów ({metoda_rect}):</b><br>
            🔵 Nadmiar: {s_p:.10f}<br>🔴 Niedomiar: {d_p:.10f}<br>⚖️ Błąd: {res_rect - y_ana:.10f}</p>
            <hr style="border:0.5px solid var(--border-color)">
            <p><b>Metoda Trapezów:</b><br>
            🔵 Nadmiar: {s_pt:.10f}<br>🔴 Niedomiar: {d_pt:.10f}<br>⚖️ Błąd: {res_trap - y_ana:.10f}</p>
            <hr style="border:0.5px solid var(--border-color)">
            <p><b>Metoda Monte Carlo:</b><br>
            <span>🟢 Pod wykresem: {hits}</span><br>
            <span>🟠 Nad wykresem: {n_mc - hits}</span><br>
            ⚖️ Błąd: {res_mc - y_ana:.10f}</p></div>""", unsafe_allow_html=True)







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
    ax2.plot(x_c_plot, y_c_plot, color='darkorange', linewidth=2)
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
            ax2.fill_between(sx, sf, h, where=(h > sf), color='cyan', alpha=0.3)
            ax2.fill_between(sx, h, sf, where=(sf > h), color='red', alpha=0.3)
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
    ax2t.plot(x_c_plot, y_c_plot, color='darkorange', linewidth=2)
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

    st.divider()

    st.subheader("3. Metoda Monte Carlo")
    y_min_mc_c, y_max_mc_c = -13, 13
    x_mc_c = m.random.uniform(a_c, b_c, n_mc)
    y_mc_c = m.random.uniform(y_min_mc_c, y_max_mc_c, n_mc)
    f_val_mc_c = funkcja_skomplikowana(x_mc_c)
    
    is_hit_pos = (y_mc_c > 0) & (y_mc_c <= f_val_mc_c)
    is_hit_neg = (y_mc_c < 0) & (y_mc_c >= f_val_mc_c)
    hits_c = m.sum(is_hit_pos) - m.sum(is_hit_neg)
    
    pole_box_c = (b_c - a_c) * (y_max_mc_c - y_min_mc_c)
    res_mc_c = pole_box_c * (hits_c / n_mc)

    fig2mc, ax2mc = plt.subplots()
    ax2mc.plot(x_c_plot, y_c_plot, color='darkorange', linewidth=2)
    
    mask_hit = is_hit_pos | is_hit_neg
    ax2mc.scatter(x_mc_c[mask_hit], y_mc_c[mask_hit], color='green', s=2, alpha=0.5)
    ax2mc.scatter(x_mc_c[~mask_hit], y_mc_c[~mask_hit], color='orange', s=2, alpha=0.5)
    
    ax2mc.set_xlim(a_c, b_c); ax2mc.set_ylim(-13, 13); ax2mc.grid(True, alpha=0.2)
    st.pyplot(fig2mc)

    mc1_c, mc2_c = st.columns(2)
    mc1_c.markdown(f"<p class='result-label'>Przybliżenie Monte Carlo:</p><p class='result-value'>{res_mc_c:.10f}</p>", unsafe_allow_html=True)
    mc2_c.markdown(f"<p class='result-label'>Wartość dokładna:</p><p class='result-value'>{y_ana_c:.10f}</p>", unsafe_allow_html=True)

    if pokaz_bledy:
        st.markdown(f"""<div class="right-panel"><h3 style='margin-top:0'>📊 Statystyki błędu</h3>
            <p><b>Metoda Prostokątów ({metoda_rect}):</b><br>
            🔵 Nadmiar: {s_c:.10f}<br>🔴 Niedomiar: {d_c:.10f}<br>⚖️ Błąd: {res_rc - y_ana_c:.10f}</p>
            <hr style="border:0.5px solid var(--border-color)">
            <p><b>Metoda Trapezów:</b><br>
            🔵 Nadmiar: {s_ct:.10f}<br>🔴 Niedomiar: {d_ct:.10f}<br>⚖️ Błąd: {res_tc - y_ana_c:.10f}</p>
            <hr style="border:0.5px solid var(--border-color)">
            <p><b>Metoda Monte Carlo:</b><br>
            <span>🟢 Pod wykresem: {m.sum(mask_hit)}</span><br>
            <span>🟠 Nad wykresem: {n_mc - m.sum(mask_hit)}</span><br>
            ⚖️ Błąd: {res_mc_c - y_ana_c:.10f}</p></div>""", unsafe_allow_html=True)




st.divider()
st.header(" Zestawienie Wydajności")

complexity_steps = [10,20, 50, 80, 100, 150, 200, 300, 400, 500, 800, 1000]
err_rect, err_trap, err_mc = [], [], []
time_rect, time_trap, time_mc = [], [], []

for step in complexity_steps:
    t_r_tmp, t_t_tmp, t_m_tmp = [], [], []
    e_r_tmp, e_t_tmp, e_m_tmp = [], [], []
    
    for _ in range(30):
        t0 = time.perf_counter()
        x_b = m.linspace(a, b, step + 1)
        r_rect = m.sum(funkcja_prosta(x_b[:-1] + (b-a)/(2*step))) * (b-a)/step
        t_r_tmp.append(time.perf_counter() - t0)
        e_r_tmp.append(abs(r_rect - y_ana))

        t0 = time.perf_counter()
        h_t = funkcja_prosta(x_b)
        r_trap = ((b-a)/(2*step)) * (h_t[0] + 2 * m.sum(h_t[1:-1]) + h_t[-1])
        t_t_tmp.append(time.perf_counter() - t0)
        e_t_tmp.append(abs(r_trap - y_ana))

        points_mc = step * 100
        t0 = time.perf_counter()
        x_m = m.random.uniform(a, b, points_mc)
        y_m = m.random.uniform(0, 0.4, points_mc)
        r_mc = ((b-a) * 0.4) * (m.sum(y_m <= funkcja_prosta(x_m)) / points_mc)
        t_m_tmp.append(time.perf_counter() - t0)
        e_m_tmp.append(abs(r_mc - y_ana))

    time_rect.append(m.mean(t_r_tmp) * 1000)
    time_trap.append(m.mean(t_t_tmp) * 1000)
    time_mc.append(m.mean(t_m_tmp) * 1000)
    err_rect.append(m.mean(e_r_tmp))
    err_trap.append(m.mean(e_t_tmp))
    err_mc.append(m.mean(e_m_tmp))

col_bench1, col_bench2 = st.columns(2)

with col_bench1:
    st.subheader("🎯 Dokładność")
    fig_err, ax_err = plt.subplots()
    ax_err.plot(complexity_steps, err_rect, label="Prostokąty", color="royalblue")
    ax_err.plot(complexity_steps, err_trap, label="Trapezy", color="green")
    ax_err.plot(complexity_steps, err_mc, label="Monte Carlo", color="orange", linestyle="--")
    ax_err.set_yscale('log')
    ax_err.set_ylabel("Błąd bezwzględny")
    ax_err.legend()
    ax_err.grid(True, alpha=0.2)
    st.pyplot(fig_err)

with col_bench2:
    st.subheader("⏱️ Czas")
    fig_time, ax_time = plt.subplots()
    ax_time.plot(complexity_steps, time_rect, label="Prostokąty", color="royalblue")
    ax_time.plot(complexity_steps, time_trap, label="Trapezy", color="green")
    ax_time.plot(complexity_steps, time_mc, label="Monte Carlo", color="orange")
    ax_time.set_yscale('log')
    ax_time.set_ylabel("Czas")
    ax_time.legend()
    ax_time.grid(True, which="both", alpha=0.2)
    st.pyplot(fig_time)


st.divider()
st.header("💬Mój komentarz")
st.write("Przede wszystkim chcę powiedzieć, że nienawidzę Jupyter Notebooków, jak zapewne widać.Lepiej spędzić pare godzin robić to w pythonie na streamlit'cie. Robiłem to tak między północą a 3:00, więc jak coś nie jest bardzo szczególowo opisane, to pewnie dlatego.")
st.write("Teraz do faktycznych wniosków:")
st.write("""
         Metoda prostokątów jest w zasadzie wystarczająca do większości zastosowań. Na moją intuicję zakładałbym, że opcja środkowa
         jest najbezpieczniejsza i najbardziej uniwersalna. Metoda Lewostronna zawsze mocno zawyża funkcje malejace, a zaniża rosnące.
         Oczywiście analogicznie dla Metody Prawostronnej (przeciwnie do Lewostronnej). W części funkcji te błędy obliczeniowe będą się kancelować,
         jeśli funkcja ma podobną ilość obszarów rosnących co malejących.
         """)
st.write("""
         Metoda trapezów jest w sumie sprytna, ale w tym wariancie ta metoda opiera kąt góry trapezu na punktach pobliskich, co jest tym razem poddatne bardziej
         na zachowanie drugiej pochodnej, czyli czy nasza funkcja zagina się do góry czy do dołu. Myślę że nie głupią opcją, byłoby wyliczać pochodna z funkcji w punkcie
         środka przedziału i ustawiać trapez pod tym kątem (w sensie żeby obliczyć kąt nachylenia funkcji w punkcie środka przedziału).
         Z wykresów wynika że zapewnia ona nieco mniejszą dokładność (zgadza się to z moimi obserwacjami, choć może być winą przyjętej metody badawczej),
         ale za to jest szybsza, przynajmniej w kontekscie bazowym. Czas potrzebny dla metody prostokątów i trapezów rośnie z podobną prędkością,
         ale metoda trapezów jest szybsza o jakąś stałą. To stanowi, że będzie się nadawać bardziej do wielokrotnego obliczania prostych całek, 
         kiedy metoda prostokątów będzie lepsza dla jednej, ale bardzo złożonej całki.
         """)
st.write("""
         Metoda monte carlo szczerze mnie zawiodła. Pamiętam jak przybliżałem wartość Pi używając losowych punktów i wyniki potrafiły być zaskakująco dokładne,
         tymczasem na całkowaniu nie widać jej potęgi. Wykresy sugerują że precyzja przybliżenia rośnie dość powoli, kiedy czas potrzebny rośnie dość szybko.
         Zastanawia mnie realne tempo tego wzrostu, bo próbowałem zwiększać dokładnośc wykresów i mimo że monte carlo wygląda jakby rosło logarytmicznie,
         to nawet dla dość dużych złożoności nadal wyprzedza funkcje liniowe w swoim wzroście (może liniowe ją wyprzedzą w przypadku bardzo dużych liczb, znacznie dalej na prawo na wykresie).
         Ostatecznie cała siła monte carlo zależy od tego, jak umieścimy obszar na którym rozrzucamy punkty. Myślę że w przypadku moich wykresów, te punkty
         mogą być rozrzucone troche za daleko (za duży head space zostawiony), ale metoda, która wymaga żeby się nią troszczyć jak niemowlęciem, żeby tylko zadziałała, to słaba metoda.
         Mimo że nie działa świetnie, to nadal fascynującym faktem jest to, że w ogóle działa. Pradoksalne jest natomiast to, że niejednokrotnie produkuje dokładniejsze wyniki dla mniejszej liczby punktów.
         """)
st.write("""
         Kończąc wywód - ja bym używał metody prostokątów wyrównywanej do środka przedziału. Metoda trapezów jest delikatnie lżejsza, więc nadaje
         się lepiej do wielu prostych funkcji. Monte carlo wymaga specjalnej troski, ale przez swoją losowość przypomina hazard, więc i tak jest moim ulubieńcem.
         """)
st.header("Dawid Szewcztk®")