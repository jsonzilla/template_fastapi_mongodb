
def test_catch_all(client):
    response = client.get('/')
    assert response.status_code == 200
    assert response.json() == {'message': 'running...'}
