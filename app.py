from flask import Flask, render_template
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

if __name__ == '__main__':
    app.run(debug=True)