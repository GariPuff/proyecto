from flask import Flask, render_template
import mysql.connector

app = Flask(__name__)

# Configuración de conexión a la base de datos MySQL
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        port=3307,
        user="root",        # Cambia esto por tu usuario de MySQL
        password="GmKhn4CjNK",        # Cambia esto por tu contraseña de MySQL
        database="cafeteria_universitaria"
    )

# Actividad 3: Ruta principal /
@app.route('/')
def index():
    return render_template('index.html')

# Actividad 4: Ruta /productos
@app.route('/productos')
def productos():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id_producto, nombre, categoria, precio, stock FROM producto;")
    lista_productos = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('productos.html', productos=lista_productos)

# Actividad 5: Ruta /pedidos con cálculo de totales usando JOIN
@app.route('/pedidos')
def pedidos():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    # Consulta SQL relacionando las tablas pedido, cliente y detalle_pedido
    query = """
    SELECT 
        p.id_pedido, 
        c.nombre AS cliente, 
        p.fecha_pedido AS fecha, 
        p.estado, 
        IFNULL(SUM(dp.cantidad * dp.precio_unitario), 0.00) AS total
    FROM pedido p
    JOIN cliente c ON p.id_cliente = c.id_cliente
    LEFT JOIN detalle_pedido dp ON p.id_pedido = dp.id_pedido
    GROUP BY p.id_pedido, c.nombre, p.fecha_pedido, p.estado;
    """
    cursor.execute(query)
    lista_pedidos = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('pedidos.html', pedidos=lista_pedidos)

if __name__ == '__main__':
    app.run(debug=True)