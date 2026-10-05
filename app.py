import streamlit as st
import numpy as np

# --- LAB to RGB Conversion ---
def lab_to_xyz(l, a, b):
    ref_x, ref_y, ref_z = 95.047, 100.0, 108.883
    y = (l + 16) / 116
    x = a / 500 + y
    z = y - b / 200

    def f_inv(t):
        if t**3 > 0.008856:
            return t**3
        else:
            return (t - 16/116) / 7.787

    x = ref_x * f_inv(x)
    y = ref_y * f_inv(y)
    z = ref_z * f_inv(z)
    return x/100, y/100, z/100

def xyz_to_rgb(x, y, z):
    r = x * 3.2406 + y * -1.5372 + z * -0.4986
    g = x * -0.9689 + y * 1.8758 + z * 0.0415
    b = x * 0.0557 + y * -0.2040 + z * 1.0570

    def gamma(c):
        if c <= 0.0031308:
            return 12.92*c
        else:
            return 1.055*(c**(1/2.4)) - 0.055

    r, g, b = gamma(r), gamma(g), gamma(b)
    r, g, b = np.clip([r,g,b], 0, 1)
    return int(r*255), int(g*255), int(b*255)

def lab_to_rgb(L, a, b):
    x, y, z = lab_to_xyz(L, a, b)
    return xyz_to_rgb(x, y, z)

# --- App UI ---
st.set_page_config(page_title="Color Mix Lab", page_icon="🎨")
st.title("🎨 Color Combination & LAB Mixer")

tab1, tab2 = st.tabs(["Color Combinations", "LAB Color Mixing"])

with tab1:
    st.header("1. Color Combination Generator")
    base_color = st.color_picker("Pick a Base Color", "#FF0000")
    r = int(base_color[1:3], 16)
    g = int(base_color[3:5], 16)
    b = int(base_color[5:7], 16)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.write("**Complementary**")
        comp = f"#{255-r:02x}{255-g:02x}{255-b:02x}"
        st.color_picker("Comp Color", comp, key="c1")
        st.code(comp)

    with col2:
        st.write("**Analogous**")
        st.color_picker("Analogous 1", f"#{r:02x}{g:02x}{min(255, b+50):02x}", key="a1")
        st.color_picker("Analogous 2", f"#{min(255, r+50):02x}{g:02x}{b:02x}", key="a2")

    with col3:
        st.write("**Triadic**")
        st.color_picker("Triadic 1", f"#{g:02x}{b:02x}{r:02x}", key="t1")
        st.color_picker("Triadic 2", f"#{b:02x}{r:02x}{g:02x}", key="t2")

with tab2:
    st.header("2. LAB Color Mixing")
    st.info("LAB me mixing RGB se zyada natural hota hai.")

    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Color 1 LAB")
        L1 = st.slider("L1 Lightness", 0, 100, 60, key="L1")
        a1 = st.slider("a1 Green-Red", -128, 127, 50, key="a1_lab")
        b1 = st.slider("b1 Blue-Yellow", -128, 127, 50, key="b1_lab")
        rgb1 = lab_to_rgb(L1, a1, b1)
        st.markdown(f'<div style="background-color:rgb{rgb1};height:100px;border-radius:10px"></div>', unsafe_allow_html=True)

    with c2:
        st.subheader("Color 2 LAB")
        L2 = st.slider("L2 Lightness", 0, 100, 40, key="L2")
        a2 = st.slider("a2 Green-Red", -128, 127, -20, key="a2_lab")
        b2 = st.slider("b2 Blue-Yellow", -128, 127, 20, key="b2_lab")
        rgb2 = lab_to_rgb(L2, a2, b2)
        st.markdown(f'<div style="background-color:rgb{rgb2};height:100px;border-radius:10px"></div>', unsafe_allow_html=True)

    st.divider()
    Lm = (L1 + L2) / 2
    am = (a1 + a2) / 2
    bm = (b1 + b2) / 2
    rgb_mix = lab_to_rgb(Lm, am, bm)
    hex_mix = f"#{rgb_mix[0]:02x}{rgb_mix[1]:02x}{rgb_mix[2]:02x}"

    st.subheader("Mixed Result (LAB Average)")
    st.markdown(f'<div style="background-color:rgb{rgb_mix};height:150px;border-radius:15px;border:3px solid black"></div>', unsafe_allow_html=True)
    st.success(f"Mixed LAB: L={Lm:.1f}, a={am:.1f}, b={bm:.1f} -> HEX: {hex_mix} RGB: {rgb_mix}")
