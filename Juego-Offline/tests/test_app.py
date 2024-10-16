import sys
import os
import pytest
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from app import app

@pytest.fixture
def client():
    # Configurar el cliente de prueba
    app.config['TESTING'] = True
    client = app.test_client()
    yield client

def test_get_metrics(client):
    response = client.get('/metrics')
    assert response.status_code == 200
    assert 'Content-Type' in response.headers
    assert response.headers['Content-Type'] == 'text/plain; version=0.0.4; charset=utf-8'

def test_registrar_disparo_acertado(client):
    data = {
        "acierto": True,
        "method": "POST",
        "endpoint": "/send_stat",
        "status_code": 200
    }
    response = client.post('/send_stat', json=data)
    assert response.status_code == 200
    assert response.json == {"message": "Estadística registrada", "acierto": True}

def test_registrar_disparo_fallado(client):
    data = {
        "acierto": False,
        "method": "POST",
        "endpoint": "/send_stat",
        "status_code": 200
    }
    response = client.post('/send_stat', json=data)
    assert response.status_code == 200
    assert response.json == {"message": "Estadística registrada", "acierto": False}
