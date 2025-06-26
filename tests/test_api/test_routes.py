from flask.testing import FlaskClient


def test_create_item(client: FlaskClient):
    item_name = "flask_test_item_0"
    resp = client.post(
        "/item_count",
        json={
            "item_name": item_name,
            "item_count": 5,
        },
    )
    assert resp.status_code == 200

    resp = client.get("/all")
    assert resp.status_code == 200
    data = resp.get_json()
    assert len(data) == 1
    item = data[0]
    assert item["item_name"] == item_name
