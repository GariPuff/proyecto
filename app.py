from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)


# =========================================================
# CONEXIÓN A MYSQL
# =========================================================

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        port=3307,
        user="root",
        password="GmKhn4CjNK",
        database="cafeteria_universitaria"
    )


# =========================================================
# INICIO
# =========================================================

@app.route("/")
def index():
    return render_template("index.html")


# =========================================================
# PRODUCTOS
# =========================================================

@app.route("/productos")
def productos():

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            id_producto,
            nombre,
            categoria,
            precio,
            stock
        FROM producto
        ORDER BY id_producto DESC
    """)

    lista_productos = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        "productos.html",
        productos=lista_productos
    )


# =========================================================
# AGREGAR PRODUCTO
# =========================================================

@app.route("/agregar_producto", methods=["GET", "POST"])
@app.route("/agregar_productos", methods=["GET", "POST"])
def agregar_producto():

    if request.method == "POST":

        nombre = request.form["nombre"]
        categoria = request.form["categoria"]
        precio = request.form["precio"]
        stock = request.form["stock"]

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO producto
            (nombre, categoria, precio, stock)
            VALUES (%s, %s, %s, %s)
        """, (
            nombre,
            categoria,
            precio,
            stock
        ))

        conn.commit()

        cursor.close()
        conn.close()

        return redirect(url_for("productos"))

    return render_template("agregar_producto.html")


# =========================================================
# ACTUALIZAR PRODUCTO
# =========================================================

@app.route("/actualizar_producto/<int:id_producto>")
def actualizar_producto(id_producto):

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            id_producto,
            nombre,
            categoria,
            precio,
            stock
        FROM producto
        WHERE id_producto = %s
    """, (id_producto,))

    producto = cursor.fetchone()

    cursor.close()
    conn.close()

    if producto is None:
        return "Producto no encontrado", 404

    return render_template(
        "actualizar_producto.html",
        producto=producto
    )


# =========================================================
# GUARDAR ACTUALIZACIÓN DEL PRODUCTO
# =========================================================

@app.route("/actualizar_productos", methods=["POST"])
def actualizar_productos():

    id_producto = request.form["id_producto"]
    nombre = request.form["nombre"]
    categoria = request.form["categoria"]
    precio = request.form["precio"]
    stock = request.form["stock"]

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE producto
        SET
            nombre = %s,
            categoria = %s,
            precio = %s,
            stock = %s
        WHERE id_producto = %s
    """, (
        nombre,
        categoria,
        precio,
        stock,
        id_producto
    ))

    conn.commit()

    cursor.close()
    conn.close()

    return redirect(url_for("productos"))


# =========================================================
# BORRAR PRODUCTO
# =========================================================

@app.route("/borrar_producto/<int:id_producto>", methods=["POST"])
def borrar_producto(id_producto):

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM producto
        WHERE id_producto = %s
    """, (id_producto,))

    conn.commit()

    cursor.close()
    conn.close()

    return redirect(url_for("productos"))


# =========================================================
# PEDIDOS
# =========================================================

@app.route("/pedidos")
def pedidos():

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    query = """
        SELECT
            p.id_pedido,
            c.nombre AS cliente,
            p.fecha_pedido AS fecha,
            p.estado,
            IFNULL(
                SUM(dp.cantidad * dp.precio_unitario),
                0.00
            ) AS total

        FROM pedido p

        JOIN cliente c
            ON p.id_cliente = c.id_cliente

        LEFT JOIN detalle_pedido dp
            ON p.id_pedido = dp.id_pedido

        GROUP BY
            p.id_pedido,
            c.nombre,
            p.fecha_pedido,
            p.estado

        ORDER BY p.id_pedido DESC
    """

    cursor.execute(query)

    lista_pedidos = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        "pedidos.html",
        pedidos=lista_pedidos
    )


# =========================================================
# AGREGAR PEDIDO
# =========================================================

@app.route("/agregar_pedido", methods=["GET", "POST"])
def agregar_pedido():

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == "POST":

        id_cliente = request.form["id_cliente"]
        fecha_pedido = request.form["fecha_pedido"]
        estado = request.form["estado"]

        cursor.execute("""
            INSERT INTO pedido
            (id_cliente, fecha_pedido, estado)
            VALUES (%s, %s, %s)
        """, (
            id_cliente,
            fecha_pedido,
            estado
        ))

        conn.commit()

        cursor.close()
        conn.close()

        return redirect(url_for("pedidos"))

    cursor.execute("""
        SELECT
            id_cliente,
            nombre
        FROM cliente
        ORDER BY nombre
    """)

    clientes = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        "agregar_pedido.html",
        clientes=clientes
    )


# =========================================================
# ACTUALIZAR PEDIDO
# =========================================================

@app.route("/actualizar_pedido/<int:id_pedido>")
def actualizar_pedido(id_pedido):

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            id_pedido,
            id_cliente,
            fecha_pedido,
            estado
        FROM pedido
        WHERE id_pedido = %s
    """, (id_pedido,))

    pedido = cursor.fetchone()

    cursor.close()
    conn.close()

    if pedido is None:
        return "Pedido no encontrado", 404

    return render_template(
        "actualizar_pedido.html",
        pedido=pedido
    )


# =========================================================
# GUARDAR ACTUALIZACIÓN DEL PEDIDO
# =========================================================

@app.route("/actualizar_pedidos", methods=["POST"])
def actualizar_pedidos():

    id_pedido = request.form["id_pedido"]
    fecha_pedido = request.form["fecha_pedido"]
    estado = request.form["estado"]

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE pedido
        SET
            fecha_pedido = %s,
            estado = %s
        WHERE id_pedido = %s
    """, (
        fecha_pedido,
        estado,
        id_pedido
    ))

    conn.commit()

    cursor.close()
    conn.close()

    return redirect(url_for("pedidos"))


# =========================================================
# BORRAR PEDIDO
# =========================================================

@app.route("/borrar_pedido/<int:id_pedido>", methods=["POST"])
def borrar_pedido(id_pedido):

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM detalle_pedido
        WHERE id_pedido = %s
    """, (id_pedido,))

    cursor.execute("""
        DELETE FROM pedido
        WHERE id_pedido = %s
    """, (id_pedido,))

    conn.commit()

    cursor.close()
    conn.close()

    return redirect(url_for("pedidos"))


# =========================================================
# EJECUTAR FLASK
# =========================================================

if __name__ == "__main__":
    app.run(debug=True)