#!/usr/bin/env python3
import asyncio
import argparse
import sys
from pathlib import Path
from core import convert_presentation


def cli_progress(current, total, message):
    """Callback para mostrar barra de progreso en la terminal."""
    padding = " " * 20
    if total > 0:
        percent = int(current / total * 100)
        sys.stdout.write(f"\r   📸 {message} [{percent}%]{padding}")
    else:
        sys.stdout.write(f"\r   ℹ️  {message}{padding}")
    sys.stdout.flush()


async def process_files(paths, quality):
    """Busca archivos SVG/HTML en las rutas dadas y ejecuta la conversión."""
    files_to_process = []
    valid_exts = {".svg", ".html"}

    for path_str in paths:
        path = Path(path_str)
        if path.is_file() and path.suffix.lower() in valid_exts:
            files_to_process.append(path)
        elif path.is_dir():
            for ext in valid_exts:
                files_to_process.extend(list(path.glob(f"*{ext}")))

    files_to_process = sorted(list(set(files_to_process)))

    if not files_to_process:
        print("❌ No se encontraron archivos válidos (.svg, .html) en las rutas.")
        return

    print(f"🚀 Procesando {len(files_to_process)} archivos (Calidad: {quality}x)\n")

    for input_file in files_to_process:
        output_pdf = input_file.with_suffix(".pdf")
        print(f"📄 Procesando: {input_file.name}")

        try:
            await convert_presentation(input_file, output_pdf, quality, cli_progress)
            print(f"\n   ✅ Guardado exitosamente: {output_pdf.name}")
        except Exception as e:
            print(f"\n   ❌ Error al convertir {input_file.name}: {e}")
        print("-" * 40)


def main():
    parser = argparse.ArgumentParser(
        description="Convertidor de presentaciones Web (JessyInk, Sozi, etc.) a PDF."
    )
    parser.add_argument("paths", nargs="*", help="Archivos o carpetas")
    parser.add_argument(
        "-q",
        "--quality",
        type=int,
        default=4,
        choices=range(1, 9),
        help="Factor de escala de calidad (1-8, defecto: 4)",
    )

    args = parser.parse_args()

    if not args.paths:
        parser.print_help()
        sys.exit(0)

    try:
        asyncio.run(process_files(args.paths, args.quality))
    except KeyboardInterrupt:
        print("\n\n⚠️  Proceso interrumpido por el usuario.")
        sys.exit(0)


if __name__ == "__main__":
    main()
