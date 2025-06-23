import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from sympy import sympify, lambdify, Symbol

# Konfigurasi halaman
st.set_page_config(page_title="Bisection Method App", layout="wide")

# CSS: grafik tetap proporsional & teks tidak membesar
st.markdown("""
<style>
.element-container:has(canvas) {
    max-width: 700px;
    margin-left: auto;
    margin-right: auto;
}
.custom-title {
    text-align: center;
    font-size: 24px;
    font-weight: 600;
    margin-top: 0;
    margin-bottom: 10px;
    color: white;
}
.instruction {
    text-align: center;
    font-size: 16px;
    line-height: 1.6;
    color: white;
}
</style>

<div style='text-align: center; font-size: 16px; margin-top: 20px;'>
    Masukkan fungsi <span style='font-family: monospace; color: #00FF99;'>f(x)</span> dalam format Python:<br><br>
    Gunakan <span style='font-family: monospace;'>*</span> untuk pangkat, <span style='font-family: monospace;'></span> untuk perkalian.<br><br>
    Contoh: <span style='font-family: monospace; color: #00FF99;'>x**3 + 3*x - 5</span>
</div>
""", unsafe_allow_html=True)
st.markdown("---")

# Fungsi Bisection
def bisection_visual(f, a, b, tol=1e-6, max_iter=100):
    steps = []
    if f(a) * f(b) >= 0:
        raise ValueError("f(a) dan f(b) harus memiliki tanda yang berbeda.")
    
    for i in range(max_iter):
        c = (a + b) / 2
        steps.append((a, b, c, f(c)))
        if abs(f(c)) < tol or abs(b - a) < tol:
            return c, i + 1, steps
        if f(a) * f(c) < 0:
            b = c
        else:
            a = c
    return c, max_iter, steps

# Layout 2 kolom
col1, col2 = st.columns([1, 2])

with col1:
    st.header("🧮 Input")
    f_expr = st.text_input("Fungsi f(x):", "x**3 + 3*x - 5", key="fx_input")
    a = st.number_input("Batas bawah (a):", value=1.0, key="a_input")
    b = st.number_input("Batas atas (b):", value=2.0, key="b_input")
    tol = st.number_input("Toleransi:", value=1e-6, format="%.6f", key="tol_input")
    max_iter = st.number_input("Maksimum Iterasi:", value=100, step=1, key="iter_input")

    if st.button("🔍 Hitung"):
        st.session_state['run'] = True

    if st.button("🔄 Reset"):
        st.session_state.clear()

with col2:
    st.header("📊 Hasil dan Grafik")

    if st.session_state.get('run', False):
        try:
            x = Symbol('x')
            f_sym = sympify(st.session_state['fx_input'])
            f = lambdify(x, f_sym, modules=['numpy'])

            a = st.session_state['a_input']
            b = st.session_state['b_input']
            tol = st.session_state['tol_input']
            max_iter = st.session_state['iter_input']

            f_a = f(a)
            f_b = f(b)

            st.write(f"**f(a) = {f_a:.4f}**, **f(b) = {f_b:.4f}**")

            if f_a * f_b > 0:
                st.warning("⚠️ f(a) dan f(b) harus memiliki tanda berbeda.")
            else:
                root, iterations, steps = bisection_visual(f, a, b, tol, max_iter)
                st.success(f"Akar ditemukan: **{root:.6f}** dalam {iterations} iterasi.")

                step_num = st.slider("🔄 Lihat iterasi ke-", 0, len(steps)-1, 0)
                a_i, b_i, c_i, fc_i = steps[step_num]

                st.write(f"**Iterasi {step_num + 1}**:")
                st.write(f"a = {a_i:.6f}, b = {b_i:.6f}, c = {c_i:.6f}, f(c) = {fc_i:.6f}")

                # Grafik
                x_vals = np.linspace(a - 1, b + 1, 400)
                y_vals = f(x_vals)

                fig, ax = plt.subplots(figsize=(6, 4))
                ax.plot(x_vals, y_vals, label='f(x)', color='blue')
                ax.axhline(0, color='black', linewidth=1)
                ax.axvline(a_i, color='gray', linestyle='dotted', label='a')
                ax.axvline(b_i, color='gray', linestyle='dotted', label='b')
                ax.plot(c_i, fc_i, 'ro', label=f'c = {c_i:.4f}')
                ax.axvline(root, color='red', linestyle='--', label=f"Akar ≈ {root:.6f}")

                ax.set_xlabel("x")
                ax.set_ylabel("f(x)")
                ax.grid(True)
                ax.legend()
                st.pyplot(fig)

        except Exception as e:
            st.error(f"❌ Terjadi kesalahan: {e}")
