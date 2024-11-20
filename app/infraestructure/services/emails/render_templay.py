from jinja2 import Environment, FileSystemLoader

# Configura el entorno de Jinja2
file_loader = FileSystemLoader('templates')
env = Environment(loader=file_loader)

# Carga la plantilla
template = env.get_template('user.new.account.html.j2')

# Renderiza la plantilla con los datos necesarios
output = template.render(title="Mi Título")

# Guarda el resultado en un archivo .html
with open('output.html', 'w') as f:
    f.write(output)