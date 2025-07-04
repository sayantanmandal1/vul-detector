from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_post_analyze_endpoint():
    response = client.post("/analyze", json={
        "code": "def test():\n    eval('print(1)')",
        "language": "python"
    })

    assert response.status_code == 200
    data = response.json()
    assert "vulnerabilities" in data
    assert any("eval" in v["description"] for v in data["vulnerabilities"]) 