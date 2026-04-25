import os
from datetime import date


def file_write(content: str) -> dict:
    """
    Escribe el resumen diario en el archivo outputs/brief_YYYY-MM-DD.md.
    Crea el directorio outputs/ si no existe.
    Recibe el contenido completo del resumen como texto markdown.
    Retorna el path del archivo guardado.
    """
    try:
        today = date.today().isoformat()
        outputs_dir = os.path.join(os.getcwd(), "outputs")
        os.makedirs(outputs_dir, exist_ok=True)

        file_path = os.path.join(outputs_dir, f"brief_{today}.md")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)

        return {"status": "success", "path": file_path}
    except Exception as e:
        return {"status": "error", "message": f"No se pudo guardar el archivo: {e}"}
