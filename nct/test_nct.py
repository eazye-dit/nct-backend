import os
import tempfile

import pytest

import nct


@pytest.fixture
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
