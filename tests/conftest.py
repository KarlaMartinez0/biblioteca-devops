import pytest
from app.app import app

@pytest.fixture(scope="session", autouse=True)
def configurar_entorno_pruebas():
    """Configura Flask en modo testing."""
    app.config["TESTING"] = True