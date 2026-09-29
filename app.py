from flask import Flask, render_template, request, redirect
import mysql.connector

app = Flask(__name__)

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        port=3307,
        user="root",
        password='GmKhn4CjNK',
        database="cafeteria_universitaria"
    )

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/productos')
def productos():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id_producto, nombre, categoria, precio, stock FROM producto;")
    lista_productos = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('productos.html', productos=lista_productos)

@app.route('/pedidos')
def pedidos():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
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

@app.route('/agregar_productos', methods=['GET', 'POST'])
def agregar_productos():
    if request.method == 'POST':
        nombre = request.form['nombre']
        categoria = request.form['categoria']
        precio = request.form['precio']
        stock = request.form['stock']

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO producto (nombre, categoria, precio, stock) VALUES (%s, %s, %s, %s)",
            (nombre, categoria, precio, stock)
        )
        conn.commit()
        cursor.close()
        conn.close()

    return redirect('/productos')

@app.route('/agregar_pedidos', methods=['GET', 'POST'])
def agregar_pedidos():
    if request.method == 'POST':
        id_cliente = request.form['id_cliente']
        fecha_pedido = request.form['fecha_pedido']
        estado = request.form['estado']

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO pedido (id_cliente, fecha_pedido, estado) VALUES (%s, %s, %s)",
            (id_cliente, fecha_pedido, estado)
        )
        conn.commit()
        cursor.close()
        conn.close()

    return redirect('/pedidos')

@app.route('/actualizar_pedidos', methods=['GET', 'POST'])
def actualizar_pedidos():
    if request.method == 'POST':
        id_pedido = request.form['id_pedido']
        fecha_pedido = request.form['fecha_pedido']
        estado = request.form['estado']

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE pedido SET fecha_pedido = %s, estado = %s WHERE id_pedido = %s",
            (fecha_pedido, estado, id_pedido)
        )
        conn.commit()
        cursor.close()
        conn.close()

    return redirect('/pedidos')

if __name__ == '__main__':
    app.run(debug=True)