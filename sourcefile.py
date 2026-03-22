import streamlit as st
import smtplib
from email.mime.text import MIMEText

# ---------------- EMAIL ----------------
EMAIL_SENDER = "mateocamanoocana@alumnos.tajamar.es"
EMAIL_PASSWORD = "36147873"
EMAIL_RECEIVER = "mateocamanoocana@alumnos.tajamar.es"

def enviar_email(nombre, pedido, total):
    try:
        msg = MIMEText(f"Cliente: {nombre}\n\n{pedido}\nTotal: {total}€")
        msg["Subject"] = "Nuevo pedido 3D"
        msg["From"] = EMAIL_SENDER
        msg["To"] = EMAIL_RECEIVER

        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        server.send_message(msg)
        server.quit()
        return True
    except Exception as e:
        st.error(f"Error real: {e}")
        return False

# ---------------- APP ----------------
st.set_page_config(layout="wide")
st.title("🧱 Tienda 3D PRO")

# ---------------- CLIENTE ----------------
st.header("👤 Datos del cliente")
nombre = st.text_input("Nombre y apellidos")

# ---------------- CARRITO ----------------
if "carrito" not in st.session_state:
    st.session_state.carrito = []

# ================= LLAVERO =================
st.header("🔑 Llavero personalizado")

base_precio = 3

col1, col2 = st.columns(2)

with col1:
    tipo = st.selectbox("Tipo", ["Nombre personalizado", "Escudo equipo fútbol"])
    texto = st.text_input("Texto o equipo")

    tamaño = st.selectbox(
        "Tamaño",
        [
            "Estándar (35x25x3) +0€",
            "Grande (45x35x4) +0.5€",
            "Súper grande (55x45x5) +1€",
            "Personalizado +2€"
        ]
    )

    if "Personalizado" in tamaño:
        st.warning("⚠️ Especifica medidas en observaciones")

with col2:
    colores = st.selectbox(
        "Colores",
        [
            "2 colores (estándar) +0€",
            "3 colores +0.5€",
            "4 colores +1€"
        ]
    )

    obs_llavero = st.text_area("Observaciones llavero")

# PRECIO LLAVERO
extra_tamaño = 0
extra_color = 0

if "Grande" in tamaño:
    extra_tamaño = 0.5
elif "Súper" in tamaño:
    extra_tamaño = 1
elif "Personalizado" in tamaño:
    extra_tamaño = 2

if "3 colores" in colores:
    extra_color = 0.5
elif "4 colores" in colores:
    extra_color = 1

precio_llavero = base_precio + extra_tamaño + extra_color

st.write(f"💰 Precio: {precio_llavero}€")

if st.button("Añadir llavero"):
    if "Personalizado" in tamaño and obs_llavero.strip() == "":
        st.error("Debes indicar medidas")
    else:
        desc = f"Llavero | {tipo} | {texto} | {tamaño} | {colores} | {obs_llavero} | {precio_llavero}€"
        st.session_state.carrito.append(("Llavero", precio_llavero, desc))
        st.success("Añadido")

# ================= SOPORTES =================
st.header("📱 Soportes")

col3, col4 = st.columns(2)

with col3:
    tipo_soporte = st.selectbox(
        "Tipo de soporte",
        ["Móvil escritorio", "Móvil coche", "Mando PS5"]
    )

    tamaño_soporte = st.selectbox(
        "Tamaño soporte",
        ["Estándar +0€", "Grande +2€"]
    )

with col4:
    color_soporte = st.selectbox(
        "Color",
        ["1 color +0€", "2 colores +1€"]
    )

    obs_soporte = st.text_area("Observaciones soporte")

# PRECIO SOPORTE
precio_soporte = 10

if "Grande" in tamaño_soporte:
    precio_soporte += 2

if "2 colores" in color_soporte:
    precio_soporte += 1

st.write(f"💰 Precio: {precio_soporte}€")

if st.button("Añadir soporte"):
    desc = f"Soporte | {tipo_soporte} | {tamaño_soporte} | {color_soporte} | {obs_soporte} | {precio_soporte}€"
    st.session_state.carrito.append(("Soporte", precio_soporte, desc))
    st.success("Añadido")

# ================= PERSONALIZADO =================
st.header("✨ Objeto totalmente personalizado")

detalle_personalizado = st.text_area("Describe lo que quieres")

if detalle_personalizado == "":
    st.info("Describe tu idea para calcular el pedido")

precio_personalizado = 20

st.write(f"💰 Precio base desde: {precio_personalizado}€")

if st.button("Añadir personalizado"):
    if detalle_personalizado.strip() == "":
        st.error("Describe el objeto")
    else:
        desc = f"Personalizado | {detalle_personalizado} | {precio_personalizado}€+"
        st.session_state.carrito.append(("Personalizado", precio_personalizado, desc))
        st.success("Añadido")

# ================= CARRITO =================
st.header("🛒 Carrito")

total = 0
pedido_texto = ""

if st.session_state.carrito:
    for item in st.session_state.carrito:
        st.write(item[2])
        total += item[1]
        pedido_texto += item[2] + "\n"

    st.subheader(f"TOTAL: {total}€")

    if st.button("Vaciar carrito"):
        st.session_state.carrito = []
        st.rerun()

    if st.button("Finalizar pedido"):
        if nombre == "":
            st.error("Introduce tu nombre")
        else:
            if enviar_email(nombre, pedido_texto, total):
                st.success("Pedido enviado ✅")
                st.balloons()
                st.session_state.carrito = []
            else:
                st.error("Error enviando pedido")

else:
    st.info("Carrito vacío")
