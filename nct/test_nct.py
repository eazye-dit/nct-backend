import os
import tempfile
import pytest
import json
import nct

@pytest.fixture(scope="session")
def client():
    db_fd, nct.app.config['DATABASE'] = tempfile.mkstemp()
    nct.app.config['TESTING'] = True
    client = nct.app.test_client()

    yield client

    os.close(db_fd)
    os.unlink(nct.app.config['DATABASE'])

def test_index(client):
    rv = client.get('/', follow_redirects=True)
    assert b'available_endpoints' in rv.data

def login(client, username, password):
    return client.post('/api/login/', data=dict(
        username=username,
        password=password
    ), follow_redirects=True)

def logout(client):
    return client.get('/api/logout/', follow_redirects=True)

def test_login_logout(client):
    rv = login(client, "administrator", "notsecret")
    assert b'/admin/' in rv.data

    rv = client.get('/api/whoami/')
    assert b'Administrator' in rv.data

    rv = logout(client)
    assert b'/admin/' not in rv.data

    rv = login(client, "administratorx", "notsecret")
    assert b'Login details incorrect' in rv.data

def test_new_owner(client):
    rv = login(client, "administrator", "notsecret")
    assert b'/admin/' in rv.data

    payload = {"f_name": "Kate", "l_name": "Doe", "phone": "012345678"}
    rv = client.post('/api/admin/new/owner/', follow_redirects=True, content_type="application/json", data=json.dumps(payload))
    assert b'Success' in rv.data

    rv = logout(client)
    assert b'/admin/' not in rv.data

def test_new_vehicle(client):
    rv = login(client, "administrator", "notsecret")
    assert b'/admin/' in rv.data

    rv = client.get('/api/admin/search/?owner=kate doe', follow_redirects=True)
    resp = json.loads(rv.data)
    assert resp["status"] == 200

    owner = resp["owner"]["id"]

    payload = {"registration": "141D123", "owner": owner, "vin": "JN1BV7AR6EM691716", "make": "Toyota", "model": "Yaris", "colour": "Blue", "year": 2014}
    rv = client.post('/api/admin/new/vehicle/', follow_redirects=True, content_type="application/json", data=json.dumps(payload))
    resp = json.loads(rv.data)
    assert resp["status"] == 200

    rv = logout(client)
    assert b'/admin/' not in rv.data
