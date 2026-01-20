# 📄 Web Slides to PDF Converter

Convierte tus presentaciones web interactivas (SVG/HTML) a formato PDF estático, manteniendo cada efecto, frame y transición como una página individual.

**Formatos soportados:**

- [JessyInk](https://code.google.com/archive/p/jessyink/) (Extensión de Inkscape)
- [Sozi](https://sozi.baierouge.fr/) (Editor de presentaciones Zooming)

## 🚀 Características

- 🎯 **Captura paso a paso:** Convierte cada "clic" (JessyInk) o frame (Sozi) en una página del PDF.
- 🖼️ **Alta Calidad:** Utiliza un motor de navegador real (Chromium) para renderizar los SVG exactamente como se ven en pantalla.
- 📦 **Multi-plataforma:** Detecta automáticamente el tipo de presentación.
- ⚡ **Eficiencia:** Modo CLI para automatización y modo Web para uso fácil.

## ☁️ Uso online

La forma más rápida de usar la herramienta es a través de nuestra aplicación en la nube.

👉 **[Abrir Web Slides Converter en Streamlit Cloud](https://jessyink-converter.streamlit.app/)**

---

## 💻 Uso local

Recomendamos usar **[uv](https://docs.astral.sh/uv/)** para gestionar las dependencias de forma rápida y aislada.

### 1. Preparación

```bash
# Instalar uv (si no lo tienes)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Clonar repo
git clone https://github.com/tu-usuario/web-slides-to-pdf.git
cd web-slides-to-pdf
```

### 2. Opción A: Línea de Comandos (CLI)

Ideal para scripts, procesamiento por lotes o servidores.

```bash
# 1. Instalar dependencias
uv sync

# 2. Instalar el navegador (solo la primera vez)
uv run playwright install chromium

# 3. Convertir archivo
uv run cli.py mi-presentacion.svg
```

**Ejemplos avanzados:**

```bash
# Convertir Sozi (html) con calidad máxima (8x)
uv run cli.py presentacion-sozi.html -q 8

# Procesar una carpeta mixta (SVG y HTML)
uv run cli.py ./mis-proyectos/
```

### 3. Opción B: Interfaz Gráfica (Web UI local)

```bash
# 1. Instalar dependencias web
uv sync --extra web

# 2. Iniciar la app
uv run streamlit run app.py
```

## 🛠 Desarrollo

Este proyecto utiliza `pyproject.toml` para la configuración.
El archivo `requirements.txt` se mantiene únicamente para compatibilidad con el despliegue en Streamlit Cloud.
