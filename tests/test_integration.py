import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from app.app import app

def cliente():
    app.testing = True
    return app.test_client()

def test_cargar_pagina_principal():
    c = cliente()
    respuesta = c.get("/")
    assert respuesta.status_code == 200

def test_ruta_nuevo_libro_carga():
    c = cliente()
    respuesta = c.get("/nuevo")
    assert respuesta.status_code == 200

def test_busqueda_por_autor_funciona():
    c = cliente()
    respuesta = c.get("/buscar?autor=Cervantes")
    assert respuesta.status_code == 200

def test_filtro_disponibles_funciona():
    c = cliente()
    respuesta = c.get("/disponibles")
    assert respuesta.status_code == 200