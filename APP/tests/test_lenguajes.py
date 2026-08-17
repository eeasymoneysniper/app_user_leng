from fastapi.testclient import TestClient
from PRACTICA.main import app


def test_obtener_lenguajes():
    client = TestClient(app)
    response = client.get("/usuarios/1/lenguajes")
    assert response.status_code == 200
    
