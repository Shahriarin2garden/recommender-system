from fastapi.testclient import TestClient

from tests.conftest import client


def test_health_endpoint():
    response = client.get('/health')
    assert response.status_code == 200
    payload = response.json()
    assert payload['status'] == 'healthy'
    assert 'database' in payload


def test_product_list_and_auth_flow():
    products = client.get('/api/v1/products/')
    assert products.status_code == 200
    assert isinstance(products.json(), list)

    register = client.post('/api/v1/auth/register', json={
        'email': 'demo@example.com',
        'username': 'demo',
        'full_name': 'Demo User',
        'password': 'Password123!'
    })
    assert register.status_code == 201, register.text

    login = client.post('/api/v1/auth/login', data={'username': 'demo@example.com', 'password': 'Password123!'}, headers={'Content-Type': 'application/x-www-form-urlencoded'})
    assert login.status_code == 200, login.text
    token = login.json()['access_token']
    assert token

    me = client.get('/api/v1/auth/me', headers={'Authorization': f'Bearer {token}'})
    assert me.status_code == 200


def test_recommendations_without_model_are_fallback():
    user_id = 1
    response = client.get(f'/api/v1/recommend/{user_id}?top_n=5')
    assert response.status_code == 200, response.text
    payload = response.json()
    assert 'recommendations' in payload
    assert isinstance(payload['recommendations'], list)


def test_cors_preflight_allows_localhost():
    response = client.options(
        '/api/v1/products/',
        headers={
            'Origin': 'http://localhost:3000',
            'Access-Control-Request-Method': 'GET',
        }
    )
    assert response.status_code == 200
    assert response.headers.get('access-control-allow-origin') == 'http://localhost:3000'
