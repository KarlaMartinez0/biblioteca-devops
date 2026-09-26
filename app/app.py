import os
from flask import Flask, render_template, request, redirect, url_for
import psycopg2
import psycopg2.extras

app = Flask(__name__)

# --- Conexión a PostgreSQL usando variables de entorno ---
# Estas variables las define el docker-compose.yml (tarea Integrante 4)
# y deben coincidir con las que use el Integrante 2 en init.sql
DB_HOST = os.environ.get("DB_HOST", "db")
DB_NAME = os.environ.get("DB_NAME", "biblioteca")
DB_USER = os.environ.get("DB_USER", "postgres")
DB_PASSWORD = os.environ.get("DB_PASSWORD", "postgres")


def get_connection():
    return psycopg2.connect(
        host=DB_HOST,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        cursor_factory=psycopg2.extras.RealDictCursor,
    )


@app.route("/")
def index():
    """Consultar: lista todos los libros."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM libros ORDER BY id;")
    libros = cur.fetchall()
    cur.close()
    conn.close()
    return render_template("index.html", libros=libros)


@app.route("/nuevo", methods=["GET", "POST"])
def nuevo():
    """Crear un nuevo registro."""
    if request.method == "POST":
        titulo = request.form["titulo"]
        autor = request.form["autor"]
        genero = request.form.get("genero", "")
        anio = request.form.get("anio") or None
        copias = request.form.get("copias") or 1

        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO libros (titulo, autor, genero, anio, copias) "
            "VALUES (%s, %s, %s, %s, %s);",
            (titulo, autor, genero, anio, copias),
        )
        conn.commit()
        cur.close()
        conn.close()
        return redirect(url_for("index"))

    return render_template("form.html", libro=None)


@app.route("/editar/<int:libro_id>", methods=["GET", "POST"])
def editar(libro_id):
    """Modificar un registro existente."""
    conn = get_connection()
    cur = conn.cursor()

    if request.method == "POST":
        titulo = request.form["titulo"]
        autor = request.form["autor"]
        genero = request.form.get("genero", "")
        anio = request.form.get("anio") or None
        copias = request.form.get("copias") or 1

        cur.execute(
            "UPDATE libros SET titulo=%s, autor=%s, genero=%s, anio=%s, copias=%s "
            "WHERE id=%s;",
            (titulo, autor, genero, anio, copias, libro_id),
        )
        conn.commit()
        cur.close()
        conn.close()
        return redirect(url_for("index"))

    cur.execute("SELECT * FROM libros WHERE id=%s;", (libro_id,))
    libro = cur.fetchone()
    cur.close()
    conn.close()
    return render_template("form.html", libro=libro)


@app.route("/eliminar/<int:libro_id>", methods=["POST"])
def eliminar(libro_id):
    """Eliminar un registro."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM libros WHERE id=%s;", (libro_id,))
    conn.commit()
    cur.close()
    conn.close()
    return redirect(url_for("index"))


if __name__ == "__main__":
    # host 0.0.0.0 es obligatorio para que el contenedor exponga el puerto
    app.run(host="0.0.0.0", port=5000, debug=True)