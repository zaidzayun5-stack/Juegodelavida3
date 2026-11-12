import numpy as np
import pytest

import life


def test_bloque_es_estable():
    g = life.empty(6, 6)
    g[2:4, 2:4] = 1
    assert np.array_equal(life.step(g), g)


def test_parpadeador_oscila():
    g = life.empty(5, 5)
    g[2, 1:4] = 1
    s1 = life.step(g)
    assert np.array_equal(s1, np.rot90(g))
    assert np.array_equal(life.step(s1), g)


def test_planeador_se_desplaza_en_cuatro_generaciones():
    g = life.place(life.empty(10, 10), "Planeador", 1, 1)
    for _ in range(4):
        g = life.step(g)
    assert np.array_equal(g, life.place(life.empty(10, 10), "Planeador", 2, 2))


def test_bordes_conectados():
    g = life.empty(5, 5)
    g[0, 1:4] = 1  # parpadeador pegado al borde superior
    assert life.step(g).sum() == 3


def test_patrones_son_rectangulares():
    for name, rows in life.PATTERNS.items():
        assert len({len(r) for r in rows}) == 1, name


def test_patron_demasiado_grande():
    with pytest.raises(ValueError):
        life.place(life.empty(5, 5), "Cañón de planeadores")
