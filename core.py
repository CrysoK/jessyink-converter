import asyncio
import img2pdf
import tempfile
from pathlib import Path
from playwright.async_api import async_playwright

TRANSITION_DELAY = 0.6


async def _analyze_presentation(page):
    """Inyecta JS para detectar tipo de presentación (Sozi/JessyInk) y metadatos."""
    return await page.evaluate(
        """() => {
        // Detección Sozi
        if (typeof sozi !== 'undefined' && sozi.presentation) {
            return {
                type: 'sozi',
                width: window.innerWidth || 1024,
                height: window.innerHeight || 768,
                data: sozi.presentation.frames.map(f => f.frameId)
            };
        }
        // Detección JessyInk
        if (typeof slides !== 'undefined' && slides.length > 0) {
            return {
                type: 'jessyink',
                width: window.WIDTH || 1024,
                height: window.HEIGHT || 768,
                data: Array.from(slides).map(s => s.effects ? s.effects.length : 0)
            };
        }
        return { type: 'unknown' };
    }"""
    )


def _generate_steps(info):
    """Genera la lista de hashes URL basada en el tipo de presentación."""
    steps = []
    if info["type"] == "sozi":
        steps = [f"#{frame_id}" for frame_id in info["data"]]
    elif info["type"] == "jessyink":
        for slide_idx, effect_count in enumerate(info["data"]):
            # JessyInk usa base-1 para slides
            for effect_step in range(effect_count + 1):
                steps.append(f"#{slide_idx + 1}_{effect_step}")
    return steps


async def convert_presentation(
    file_path: Path, output_path: Path, quality: int, progress_callback=None
):
    """Convierte presentaciones web (SVG/HTML) a PDF."""
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(device_scale_factor=quality)
        page = await context.new_page()
        file_url = file_path.absolute().as_uri()

        try:
            if progress_callback:
                progress_callback(0, 0, "Cargando presentación...")

            await page.goto(file_url)
            await page.wait_for_load_state("networkidle")

            info = await _analyze_presentation(page)
            if info["type"] == "unknown":
                raise ValueError(
                    "No es una presentación compatible (se requiere JessyInk o Sozi)."
                )

            # Ocultar UI específica de Sozi para que no salga en el PDF
            if info["type"] == "sozi":
                await page.add_style_tag(
                    content=".sozi-frame-list, .sozi-frame-number { display: none !important; }"
                )

            await page.set_viewport_size(
                {"width": int(info["width"]), "height": int(info["height"])}
            )

            steps = _generate_steps(info)
            total = len(steps)
            image_files = []

            with tempfile.TemporaryDirectory() as tmp_dir:
                for idx, step_hash in enumerate(steps):
                    current = idx + 1
                    if progress_callback:
                        progress_callback(
                            current, total, f"Capturando {current}/{total}"
                        )

                    await page.goto(f"{file_url}{step_hash}")
                    await page.reload()  # Forzar estado final de animación
                    await asyncio.sleep(TRANSITION_DELAY)

                    img_path = Path(tmp_dir) / f"{current:04d}.png"
                    await page.screenshot(path=img_path, type="png")
                    image_files.append(img_path)

                if progress_callback:
                    progress_callback(total, total, "Generando PDF...")

                if not image_files:
                    raise RuntimeError("No se generaron imágenes.")

                with open(output_path, "wb") as f:
                    f.write(img2pdf.convert([str(p) for p in image_files]))

        finally:
            await browser.close()
