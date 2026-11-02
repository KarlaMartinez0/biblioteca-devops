import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from app.app import validar_libro

def test_validar_libro_con_titulo_vacio_es_invalido():
    valido, mensaje = validar_libro("", "Gabriel Garcia Marquez")
    assert valido is False
    assert "título" in mensaje.lower()

def test_validar_libro_con_autor_vacio_es_invalido():
    valido, mensaje = validar_libro("Cien anos de soledad", "")
    assert valido is False
    assert "autor" in mensaje.lower()

def test_validar_libro_con_datos_completos_es_valido():
    valido, mensaje = validar_libro("Cien anos de soledad", "Gabriel Garcia Marquez")
    assert valido is True
    assert mensaje == ""