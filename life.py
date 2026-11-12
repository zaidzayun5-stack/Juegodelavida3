"""Lógica del Juego de la vida de Conway (sin dependencias de interfaz)."""
import numpy as np

# 'O' = célula viva, '.' = célula muerta
PATTERNS = {
    "Planeador": [".O.", "..O", "OOO"],
    "Nave ligera": [".OOOO", "O...O", "....O", "O..O."],
    "Púlsar": [
        "..OOO...OOO..",
        ".............",
        "O....O.O....O",
        "O....O.O....O",
        "O....O.O....O",
        "..OOO...OOO..",
        ".............",
        "..OOO...OOO..",
        "O....O.O....O",
        "O....O.O....O",
        "O....O.O....O",
        ".............",
        "..OOO...OOO..",
    ],
    "Cañón de planeadores": [
        "........................O...........",
        "......................O.O...........",
        "............OO......OO............OO",
        "...........O...O....OO............OO",
        "OO........O.....O...OO..............",
        "OO........O...O.OO....O.O...........",
        "..........O.....O.......O...........",
        "...........O...O....................",
        "............OO......................",
    ],
}


def empty(rows: int, cols: int) -> np.ndarray:
    return np.zeros((rows, cols), dtype=np.uint8)


def random_grid(rows: int, cols: int, density: float = 0.25, seed=None) -> np.ndarray:
    rng = np.random.default_rng(seed)
    return (rng.random((rows, cols)) < density).astype(np.uint8)


def step(grid: np.ndarray) -> np.ndarray:
    """Calcula la siguiente generación. Los bordes se conectan (toro)."""
    neighbors = sum(
        np.roll(np.roll(grid, dy, axis=0), dx, axis=1)
        for dy in (-1, 0, 1)
        for dx in (-1, 0, 1)
        if (dy, dx) != (0, 0)
    )
    born = neighbors == 3
    survives = (grid == 1) & (neighbors == 2)
    return (born | survives).astype(np.uint8)


def place(grid: np.ndarray, name: str, top=None, left=None) -> np.ndarray:
    """Devuelve una copia de `grid` con el patrón colocado (centrado por defecto)."""
    pattern = np.array([[c == "O" for c in row] for row in PATTERNS[name]], dtype=np.uint8)
    ph, pw = pattern.shape
    rows, cols = grid.shape
    if ph > rows or pw > cols:
        raise ValueError(f"El patrón «{name}» necesita al menos {ph}×{pw} celdas.")
    top = (rows - ph) // 2 if top is None else top
    left = (cols - pw) // 2 if left is None else left
    out = grid.copy()
    out[top:top + ph, left:left + pw] |= pattern
    return out
