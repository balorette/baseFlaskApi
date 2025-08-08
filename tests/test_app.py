from app import create_app


def test_root():
    app = create_app()
    app.testing = True
    client = app.test_client()
    res = client.get('/')
    assert res.data == b'Hello World!'
