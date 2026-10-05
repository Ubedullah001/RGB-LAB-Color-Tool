import streamlit as st
import math


# -----------------------------
# LAB to XYZ conversion
# -----------------------------
def lab_to_xyz(L, a, b):
    fy = (L + 16) / 116
    fx = a / 500 + fy
    fz = fy - b / 200

    delta = 6 / 29

    def f_inverse(t):
        if t > delta:
            return t ** 3
        return 3 * (delta ** 2) * (t - 4 / 29)

    # D65 reference white
    Xn = 95.047
    Yn = 100.000
    Zn = 108.883

    X = Xn * f_inverse(fx)
    Y = Yn * f_inverse(fy)
    Z = Zn * f_inverse(fz)

    return X, Y, Z


# -----------------------------
# XYZ to RGB conversion
# -----------------------------
def xyz_to_rgb(X, Y, Z):
    X /= 100
    Y /= 100
    Z /= 100

    r = X * 3.2406 + Y * -1.5372 + Z * -0.4986
    g = X * -0.9689 + Y * 1.8758 + Z * 0.0415
    b = X * 0.0557 + Y * -0.2040 + Z * 1.0570

    def gamma_correct(value):
        if value > 0.0031308:
            return 1.055 * (value ** (1 / 2.4)) - 0.055
        return 12.92 * value

    r = gamma_correct(r)
    g = gamma_correct(g)
    b = gamma_correct(b)

    # Limit values to valid RGB range
    r = max(0, min(1, r))
    g = max(0, min(1, g))
    b = max(0, min(1, b))

    return round(r * 255), round(g * 255), round(b * 255)


# -----------------------------
# LAB to RGB
# -----------------------------
def lab_to_rgb(L, a, b):
    X, Y, Z = lab_to_xyz(L, a, b)
    return xyz_to_rgb(X, Y, Z)


# -----------------------------
# Page settings
# -----------------------------
st.set_page_config(
    page_title="RGB & LAB Color Tool",
    page_icon="🎨",
    layout="centered"
)

# -----------------------------
# Title
# -----------------------------
st.title("🎨 RGB & LAB Color Tool")
st.write(
    "A simple color tool for textile students to explore "
    "LAB, RGB, and HEX color values."
)

st.divider()


# -----------------------------
# Primary RGB Colors
# -----------------------------
st.header("Primary RGB Colors")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(
        """
        <div style="
            background-color:#FF0000;
            padding:35px;
            border-radius:10px;
            text-align:center;
            color:white;
            font-weight:bold;">
            RED<br>
            RGB: (255, 0, 0)
        </div>
        """,
        unsafe_allow_html=True
    )

with col2:
    st.markdown(
        """
        <div style="
            background-color:#00FF00;
            padding:35px;
            border-radius:10px;
            text-align:center;
            color:black;
            font-weight:bold;">
            GREEN<br>
            RGB: (0, 255, 0)
        </div>
        """,
        unsafe_allow_html=True
    )

with col3:
    st.markdown(
        """
        <div style="
            background-color:#0000FF;
            padding:35px;
            border-radius:10px;
            text-align:center;
            color:white;
            font-weight:bold;">
            BLUE<br>
            RGB: (0, 0, 255)
        </div>
        """,
        unsafe_allow_html=True
    )

st.divider()


# -----------------------------
# LAB Input
# -----------------------------
st.header("Enter LAB Values")

st.write(
    "Change the L, a, and b* values to generate a color."
)

col1, col2, col3 = st.columns(3)

with col1:
    L = st.number_input(
        "L* (Lightness)",
        min_value=0.0,
        max_value=100.0,
        value=50.0,
        step=1.0
    )

with col2:
    a = st.number_input(
        "a* (Green ↔ Red)",
        min_value=-128.0,
        max_value=127.0,
        value=0.0,
        step=1.0
    )

with col3:
