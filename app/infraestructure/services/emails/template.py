from __future__ import annotations

from jinja2 import Environment
from jinja2 import FileSystemLoader

# Cargar el entorno de Jinja2 y el directorio de templates
env = Environment(loader=FileSystemLoader('./templates'))

# Cargar el template
template = env.get_template('email.validar.email.html.j2')

# Renderizar el template con datos de ejemplo
rendered_html = template.render(
    title='Título de Ejemplo',
    content='Contenido de ejemplo para el cuerpo del correo.',
)

# Guardar el resultado en un archivo HTML
with open('output.html', 'w') as f:
    f.write(rendered_html)

print('Template renderizado y guardado en output.html')
