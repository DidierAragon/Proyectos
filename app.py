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
            password=password
        )
        return conexion
    except psycopg2.Error as e:
        print("Error al conectar a la base de datos:", e)
        return None
@app.route('/')
def index():
    return render_template('index.html')
@app.route('/formulario')
def formulario():
    return render_template('formulario.html')
@app.route('/usuarios', methods=['post'])
def guarda():
    nombre = request.form['nombre']
    apellido = request.form['apellido']
    correo = request.form['correo']
    telefono = request.form['telefono']
    direccion = request.form['direccion']
    mensaje = request.form['mensaje']
    
    conexion_db = conexion()
    if not nombre or not apellido or not correo or not telefono or not direccion:
        return "Error: Todos los campos son obligatorios."
    if conexion_db is None:
        return "Error: No se pudo conectar a la base de datos."
    conn = conexion()

    try:
        cursor = conexion_db.cursor()
        insert_query = """
            INSERT INTO usuarios (nombre, apellido, correo, telefono, direccion)
            VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(insert_query, (nombre, apellido, correo, telefono, direccion))
        conexion_db.commit()
        cursor.close()
        return "Usuario guardado exitosamente."
    except psycopg2.Error as e:
        print("Error al insertar datos:", e)
        return "Error al guardar el usuario."
    finally:
        conn.close()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)


