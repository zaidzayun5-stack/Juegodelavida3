"""Interfaz Streamlit del Juego de la vida."""
import time

import numpy as np
import pandas as pd
import streamlit as st

import life

st.set_page_config(page_title="Juego de la vida", page_icon="🧬", layout="wide")

ALIVE = np.array([127, 214, 166], dtype=np.uint8)
DEAD = np.array([24, 36, 30], dtype=np.uint8)
GAP = np.array([14, 22, 18], dtype=np.uint8)


# ---------- Estado ----------
def init_state(rows=40, cols=60):
    if "grid" not in st.session_state:
        st.session_state.grid = life.place(life.empty(rows, cols), "Planeador", 5, 5)
        st.session_state.gen = 0
        st.session_state.running = False
        st.session_state.version = 0  # cambia la clave del editor al modificar desde código


def set_grid(grid, reset_gen=True):
    st.session_state.grid = grid
    st.session_state.version += 1
    if reset_gen:
        st.session_state.gen = 0


# ---------- Callbacks de botones ----------
def on_step():
    st.session_state.running = False
    set_grid(life.step(st.session_state.grid), reset_gen=False)
    st.session_state.gen += 1


def on_run():
    st.session_state.running = True
    st.session_state.version += 1


def on_stop():
    st.session_state.running = False
    st.session_state.version += 1


def on_random(density):
    r, c = st.session_state.grid.shape
    st.session_state.running = False
    set_grid(life.random_grid(r, c, density))


def on_clear():
    st.session_state.running = False
    set_grid(life.empty(*st.session_state.grid.shape))


def on_pattern():
    name = st.session_state.pattern
    if not name:
        return
    st.session_state.running = False
    try:
        set_grid(life.place(life.empty(*st.session_state.grid.shape), name))
        st.session_state.pattern_error = None
    except ValueError as e:
        st.session_state.pattern_error = str(e)
    st.session_state.pattern = ""


# ---------- Dibujo ----------
def render(grid, cell=12):
    h, w = grid.shape
    img = np.empty((h * cell, w * cell, 3), dtype=np.uint8)
    img[:] = np.where(np.kron(grid, np.ones((cell, cell), dtype=np.uint8))[..., None] == 1, ALIVE, DEAD)
    # líneas de cuadrícula
    img[cell - 1::cell, :, :] = GAP
    img[:, cell - 1::cell, :] = GAP
    return img


# ---------- Interfaz ----------
init_state()

st.title("Juego de la vida")
st.caption(
    "Autómata celular de John Conway. Una célula viva sobrevive con 2 o 3 vecinas vivas; "
    "una célula muerta nace si tiene exactamente 3. Los bordes se conectan."
)

with st.sidebar:
    st.header("Controles")
    rows = st.slider("Filas", 10, 80, st.session_state.grid.shape[0])
    cols = st.slider("Columnas", 10, 100, st.session_state.grid.shape[1])
    if (rows, cols) != st.session_state.grid.shape:
        st.session_state.running = False
        set_grid(life.empty(rows, cols))

    c1, c2 = st.columns(2)
    if st.session_state.running:
        c1.button("Detener", on_click=on_stop, type="primary", use_container_width=True)
    else:
        c1.button("Iniciar", on_click=on_run, type="primary", use_container_width=True)
    c2.button("Paso", on_click=on_step, use_container_width=True)

    gens = st.slider("Generaciones por ejecución", 10, 1000, 200, step=10)
    speed = st.slider("Velocidad (generaciones por segundo)", 1, 30, 10)

    st.divider()
    density = st.slider("Densidad aleatoria", 0.05, 0.60, 0.25, step=0.05)
    st.button("Aleatorio", on_click=on_random, args=(density,), use_container_width=True)
    st.button("Limpiar", on_click=on_clear, use_container_width=True)
    st.selectbox("Patrón", [""] + list(life.PATTERNS), key="pattern", on_change=on_pattern,
                 format_func=lambda x: x or "Elegir un patrón…")
    if st.session_state.get("pattern_error"):
        st.warning(st.session_state.pattern_error + " Aumenta el tamaño de la cuadrícula.")

board = st.empty()
stats = st.empty()


def show():
    g = st.session_state.grid
    board.image(render(g), use_container_width=True)
    stats.markdown(f"**Generación:** {st.session_state.gen} · **Células vivas:** {int(g.sum())}")


show()

with st.expander("Editar células a mano (marca o desmarca las casillas)"):
    if st.session_state.grid.shape[1] > 40:
        st.info("Para editar a mano conviene una cuadrícula de hasta 40 columnas.")
    df = pd.DataFrame(st.session_state.grid.astype(bool))
    edited = st.data_editor(df, hide_index=True, key=f"editor_{st.session_state.version}",
                            use_container_width=True)
    new_grid = edited.to_numpy(dtype=np.uint8)
    if not np.array_equal(new_grid, st.session_state.grid):
        st.session_state.grid = new_grid
        st.rerun()

# ---------- Ejecución continua ----------
if st.session_state.running:
    for _ in range(gens):
        st.session_state.grid = life.step(st.session_state.grid)
        st.session_state.gen += 1
        show()
        time.sleep(1 / speed)
    st.session_state.running = False
    st.session_state.version += 1
    st.rerun()
