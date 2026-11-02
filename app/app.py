import os
os.environ["PGCLIENTENCODING"] = "UTF8"

from flask import Flask, render_template, request, redirect, url_for
import psycopg2
import psycopg2.extras
import sqlite3

app = Flask(__name__)

# --- Conexión a PostgreSQL usando variables de entorno ---
DB_HOST = os.environ.get("DB_HOST", "localhost")
DB_NAME = os.environ.get("DB_NAME", "biblioteca")
DB_USER = os.environ.get("DB_USER", "postgres")
DB_PASSWORD = os.environ.get("DB_PASSWORD", "postgres")


def get_connection():
    try:
        return psycopg2.connect(
            host=DB_HOST,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            cursor_factory=psycopg2.extras.RealDictCursor,
            client_encoding='UTF8',
        )
    except Exception:
        # Fallback automático a SQLite para pruebas locales en Windows
        conn = sqlite3.connect(":memory:")
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS libros (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                titulo TEXT NOT NULL,
                autor TEXT NOT NULL,
                genero TEXT,
                anio INTEGER,
                copias INTEGER DEFAULT 1
            );
        """)
        conn.commit()
        return conn


def validar_libro(titulo, autor):
    """Valida los datos obligatorios de un libro. Retorna (es_valido, mensaje_error)."""
    if not titulo or not titulo.strip():
        return False, "El título no puede estar vacío"
    if not autor or not autor.strip():
        return False, "El autor no puede estar vacío"
    return True, ""


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

        valido, mensaje = validar_libro(titulo, autor)
        if not valido:
            return render_template("form.html", libro=None, error=mensaje)

        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO libros (titulo, autor, genero, anio, copias) "
            "VALUES (?, ?, ?, ?, ?);" if isinstance(conn, sqlite3.Connection) else
            "INSERT INTO libros (titulo, autor, genero, anio, copias) VALUES (%s, %s, %s, %s, %s);",
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
    if request.method == "POST":
        titulo = request.form["titulo"]
        autor = request.form["autor"]
        genero = request.form.get("genero", "")
        anio = request.form.get("anio") or None
        copias = request.form.get("copias") or 1

        valido, mensaje = validar_libro(titulo, autor)
        if not valido:
            libro = {"titulo": titulo, "autor": autor, "genero": genero,
                     "anio": anio, "copias": copias}
            return render_template("form.html", libro=libro, error=mensaje)

        conn = get_connection()
        cur = conn.cursor()
        update_query = (
            "UPDATE libros SET titulo=?, autor=?, genero=?, anio=?, copias=? WHERE id=?;"
            if isinstance(conn, sqlite3.Connection) else
            "UPDATE libros SET titulo=%s, autor=%s, genero=%s, anio=%s, copias=%s WHERE id=%s;"
        )
        cur.execute(update_query, (titulo, autor, genero, anio, copias, libro_id))
        conn.commit()
        cur.close()
        conn.close()
        return redirect(url_for("index"))

    conn = get_connection()
    cur = conn.cursor()
    select_query = (
        "SELECT * FROM libros WHERE id=?;" if isinstance(conn, sqlite3.Connection) else
        "SELECT * FROM libros WHERE id=%s;"
    )
    cur.execute(select_query, (libro_id,))
    libro = cur.fetchone()
    cur.close()
    conn.close()
    return render_template("form.html", libro=libro)


@app.route("/eliminar/<int:libro_id>", methods=["POST"])
def eliminar(libro_id):
    """Eliminar un registro."""
    conn = get_connection()
    cur = conn.cursor()
    delete_query = (
        "DELETE FROM libros WHERE id=?;" if isinstance(conn, sqlite3.Connection) else
        "DELETE FROM libros WHERE id=%s;"
    )
    cur.execute(delete_query, (libro_id,))
    conn.commit()
    cur.close()
    conn.close()
    return redirect(url_for("index"))


@app.route("/buscar")
def buscar_por_autor():
    """Funcionalidad nueva 1: búsqueda de libros por autor."""
    autor = request.args.get("autor", "")
    conn = get_connection()
    cur = conn.cursor()
    search_query = (
        "SELECT * FROM libros WHERE autor LIKE ? ORDER BY id;"
        if isinstance(conn, sqlite3.Connection) else
        "SELECT * FROM libros WHERE autor ILIKE %s ORDER BY id;"
    )
    cur.execute(search_query, (f"%{autor}%",))
    libros = cur.fetchall()
    cur.close()
    conn.close()
    return render_template("index.html", libros=libros, filtro_autor=autor)


@app.route("/disponibles")
def disponibles():
    """Funcionalidad nueva 2: filtro de libros con copias disponibles."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM libros WHERE copias > 0 ORDER BY id;")
    libros = cur.fetchall()
    cur.close()
    conn.close()
    return render_template("index.html", libros=libros, filtro_disponibles=True)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)