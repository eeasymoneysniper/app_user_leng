from fastapi.testclient import TestClient
from PRACTICA.main import app

def test_obtener_usuarios():
    client = TestClient(app)
    response = client.get("/usuarios")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    
def test_obtener_usuario():
    client = TestClient(app)
    response = client.get("/usuarios/1")
    assert response.status_code == 200
    assert isinstance(response.json(), dict)