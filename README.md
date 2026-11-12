# Juego de la vida

Implementación en Python del autómata celular de John Conway, con interfaz en [Streamlit](https://streamlit.io).

## Estructura

```
├── app.py              # Interfaz Streamlit
├── life.py             # Lógica del juego (NumPy)
├── tests/test_life.py  # Pruebas con pytest
└── requirements.txt
```

## Ejecutar en local

```bash
python -m venv .venv
source .venv/bin/activate      # En Windows: .venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

## Pruebas

```bash
pip install pytest
python -m pytest
```

## Subir a GitHub

```bash
git init
git add .
git commit -m "Juego de la vida con Streamlit"
git branch -M main
git remote add origin https://github.com/TU_USUARIO/juego-de-la-vida.git
git push -u origin main
```

## Desplegar en Streamlit Community Cloud

1. Entra en <https://share.streamlit.io> e inicia sesión con GitHub.
2. Pulsa **Create app** y elige el repositorio, la rama `main` y el archivo `app.py`.
3. Pulsa **Deploy**.

## Reglas

- Una célula viva con 2 o 3 vecinas vivas sigue viva; en otro caso muere.
- Una célula muerta con exactamente 3 vecinas vivas nace.
- Los bordes de la cuadrícula se conectan (toro).
