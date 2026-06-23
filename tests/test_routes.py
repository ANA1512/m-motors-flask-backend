def test_register(client):
    response = client.post('/register', json={
        'name': 'Test User',
        'email': 'newuser@test.com',
        'password': 'password123'
    })
    assert response.status_code == 201

def test_login_reussi(client):
    # D'abord créer un user
    client.post('/register', json={
        'name': 'Test User',
        'email': 'logintest@test.com',
        'password': 'password123'
    })
    # Puis se connecter
    response = client.post('/login', json={
        'email': 'logintest@test.com',
        'password': 'password123'
    })
    assert response.status_code == 200
    assert 'token' in response.get_json()

def test_login_echoue(client):
    response = client.post('/login', json={
        'email': 'inexistant@test.com',
        'password': 'mauvaismdp'
    })
    assert response.status_code == 401

def test_get_vehicules(client):
    response = client.get('/vehicules')
    assert response.status_code == 200
    assert isinstance(response.get_json(), list)