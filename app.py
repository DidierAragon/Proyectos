from flask import Flask , render_template, request, redirect
import psycopg2

app = Flask(__name__)

host = "localhost"
port = "5432"
database = "formulario"
user = "postgres"
password = "123456"

def conexion():
    import psycopg2
    try:
        conexion = psycopg2.connect(
            host=host,
            port=port,
            database=database,
            user=user,
            password=password,
            options='-c client_encoding=UTF8'  # forzar codificación cliente UTF-8
        )
        # Asegurar codificación por si acaso
        try:
            conexion.set_client_encoding('UTF8')
        except Exception:
            pass
        return conexion
    except Exception as e:  # capturar Exception porque UnicodeDecodeError puede no ser psycopg2.Error
        print("Error al conectar a la base de datos:", e)
        return None
@app.route('/')
def index():
    return render_template('index.html')
@app.route('/formulario')
def formulario():
    return render_template('formulario.html')
@app.route('/usuarios', methods=['POST'])
def guarda():
    nombre = request.form.get('nombre', '').strip()
    apellido = request.form.get('apellido', '').strip()
    correo = request.form.get('correo', '').strip()
    telefono = request.form.get('telefono', '').strip()
    direccion = request.form.get('direccion', '').strip()
    mensaje = request.form.get('mensaje', '').strip()
    
    # validar antes de abrir la conexión
    if not nombre or not apellido or not correo or not telefono or not direccion:
        return "Error: Todos los campos son obligatorios."
    
    conexion_db = conexion()
    if conexion_db is None:
        return "Error: No se pudo conectar a la base de datos."
    
    try:
        cursor = conexion_db.cursor()
        insert_query = """
            INSERT INTO usuarios (nombre, apellido, correo, telefono, direccion, mensaje)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor.execute(insert_query, (nombre, apellido, correo, telefono, direccion, mensaje))
        conexion_db.commit()
        cursor.close()
        return redirect('/')
    except psycopg2.Error as e:
        print("Error al insertar datos:", e)
        return "Error al guardar el usuario."
    finally:
        try:
            conexion_db.close()
        except Exception:
            pass

if __name__ == '__main__':
    app.run(debug=True)


