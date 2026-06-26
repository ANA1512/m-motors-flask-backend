import pytest

def test_register(client):
    response = client.post('/register', json={
        'name': 'Test User',
        'email': 'newuser@test.com',
        'password': 'password123'
    })
    assert response.status_code == 201

def test_login_reussi(client):
    client.post('/register', json={
        'name': 'Test User',
        'email': 'logintest@test.com',
        'password': 'password123'
    })
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

def test_get_vehicule_inexistant(client):
    response = client.get('/vehicule/9999')
    assert response.status_code == 404

def test_create_vehicule_sans_token(client):
    response = client.post('/vehicule', json={'name': 'Tesla', 'price': 35000})
    assert response.status_code == 401

def test_get_me_sans_token(client):
    response = client.get('/me')
    assert response.status_code == 401

def test_get_me_avec_token(client):
    client.post('/register', json={
        'name': 'Test Me',
        'email': 'me@test.com',
        'password': 'password123'
    })
    login = client.post('/login', json={
        'email': 'me@test.com',
        'password': 'password123'
    })
    token = login.get_json()['token']
    response = client.get('/me', headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == 200

def test_create_dossier_sans_token(client):
    response = client.post('/dossier', json={'vehicule_id': 1, 'type_financement': 'achat'})
    assert response.status_code == 401

def test_get_dossier_sans_token(client):
    response = client.get('/dossier')
    assert response.status_code == 401

def test_create_dossier_avec_token(client):
    client.post('/register', json={
        'name': 'Dossier User',
        'email': 'dossier@test.com',
        'password': 'password123'
    })
    login = client.post('/login', json={
        'email': 'dossier@test.com',
        'password': 'password123'
    })
    token = login.get_json()['token']
    v = client.post('/vehicule', json={
        'name': 'Tesla', 'price': 35000, 'type': 'berline',
        'kilometrage': 0, 'marque': 'Tesla', 'transmission': 'auto',
        'places': 5, 'description': 'test'
    }, headers={'Authorization': f'Bearer {token}'})
    vehicule_id = v.get_json()['id']
    response = client.post('/dossier', json={
        'vehicule_id': vehicule_id,
        'type_financement': 'achat',
        'revenu_mensuel': 2000,
        'statut': 'en attente'
    }, headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == 201

def test_register_email_deja_existant(client):
    client.post('/register', json={
        'name': 'User A',
        'email': 'doublon@test.com',
        'password': 'password123'
    })
    response = client.post('/register', json={
        'name': 'User B',
        'email': 'doublon@test.com',
        'password': 'autrepassword'
    })
    assert response.status_code == 409