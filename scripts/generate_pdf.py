import os
import shutil
import subprocess
import tempfile
from typing import Optional


def inject_css_into_html(html_path: str, css_path: str) -> str:
    """
    Lee el archivo HTML y CSS, y devuelve el contenido HTML con el CSS
    inyectado dentro de la etiqueta <head>.
    
    Args:
        html_path: Ruta al archivo HTML original
        css_path: Ruta al archivo CSS a inyectar
        
    Returns:
        Contenido HTML con CSS inyectado
    """
    # Leer contenido del HTML
    with open(html_path, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    # Leer contenido del CSS
    with open(css_path, 'r', encoding='utf-8') as f:
        css_content = f.read()
    
    # Inyectar CSS dentro de la etiqueta <head>
    # Buscamos el cierre de </head> e insertamos el CSS antes
    css_injection = f'\n<style>\n{css_content}\n</style>'
    
    if '</head>' in html_content:
        # Insertar CSS antes de </head>
        html_content = html_content.replace('</head>', f'{css_injection}\n</head>')
    else:
        # Si no hay </head>, insertar al inicio del documento
        html_content = f'{css_injection}\n{html_content}'
    
    return html_content


def generate_pdf(html_path: str, css_path: str, pdf_path: str) -> None:
    """
    Genera un archivo PDF a partir de un archivo HTML y CSS.
    
    Implementa las siguientes funcionalidades:
    1. Inyección de CSS en el HTML antes de renderizar el PDF
    2. Fallback a wkhtmltopdf si weasyprint no está disponible
    3. Uso de shutil para verificar disponibilidad de binarios
    
    Args:
        html_path: Ruta al archivo HTML de entrada
        css_path: Ruta al archivo CSS a aplicar
        pdf_path: Ruta donde se guardará el PDF generado
        
    Raises:
        ImportError: Si no se encuentra ningún motor de renderizado disponible
        RuntimeError: Si hay errores durante la generación del PDF
    """
    # Inyectar CSS en el HTML
    html_with_css = inject_css_into_html(html_path, css_path)
    
    # Crear archivo temporal con el HTML modificado
    with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False) as temp_html:
        temp_html.write(html_with_css)
        temp_html_path = temp_html.name
    
    try:
        # Intentar con WeasyPrint primero
        try:
            import weasyprint
            
            # Renderizar PDF usando WeasyPrint
            html_doc = weasyprint.HTML(filename=temp_html_path)
            html_doc.write_pdf(pdf_path)
            print(f"PDF generado exitosamente con WeasyPrint: {pdf_path}")
            return
            
        except ImportError:
            print("WeasyPrint no disponible, intentando con wkhtmltopdf...")
        
        # Fallback: Intentar con wkhtmltopdf
        wkhtmltopdf_path = shutil.which('wkhtmltopdf')
        
        if wkhtmltopdf_path is None:
            raise ImportError(
                "No se encontró wkhtmltopdf en el sistema. "
                "Instale WeasyPrint o wkhtmltopdf para generar PDFs."
            )
        
        # Ejecutar wkhtmltopdf para generar el PDF
        cmd = [
            wkhtmltopdf_path,
            '--quiet',  # Modo silencioso
            '--encoding', 'utf-8',
            '--enable-local-file-access',  # Permitir acceso a archivos locales
            temp_html_path,
            pdf_path
        ]
        
        # Ejecutar comando y capturar errores
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=False
        )
        
        if result.returncode != 0:
            raise RuntimeError(
                f"Error al ejecutar wkhtmltopdf (código {result.returncode}):\n"
                f"{result.stderr}"
            )
        
        print(f"PDF generado exitosamente con wkhtmltopdf: {pdf_path}")
        
    finally:
        # Limpiar archivo temporal
        try:
            os.unlink(temp_html_path)
        except OSError:
            pass


# Función main para pruebas
def main() -> None:
    """Función de ejemplo para probar la generación de PDF."""
    import sys
    
    if len(sys.argv) != 4:
        print("Uso: python generate_pdf.py <html_file> <css_file> <output_pdf>")
        sys.exit(1)
    
    html_path, css_path, pdf_path = sys.argv[1:4]
    
    try:
        generate_pdf(html_path, css_path, pdf_path)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
