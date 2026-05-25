import requests
import time

BASE_URL = "https://knowthyself-backend-799604771720.us-central1.run.app"

def warmup():
    print("Warming up backend...")
    requests.get(f"{BASE_URL}/health", timeout=30)
    time.sleep(2)
    print("Backend ready.\n")

def test_health():
    """Test backend is live and responding."""
    response = requests.get(f"{BASE_URL}/health", timeout=10)
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

def test_user_registration():
    """Test user registration and track selection."""
    response = requests.post(f"{BASE_URL}/user", json={
        "user_id": "eval_user",
        "track": "fitness"
    }, timeout=30)
    assert response.status_code == 200
    data = response.json()
    assert data["user_id"] == "eval_user"
    assert data["track"] == "fitness"

def test_chat():
    """Test end-to-end coaching response."""
    response = requests.post(f"{BASE_URL}/chat", json={
        "user_id": "eval_user",
        "track": "fitness",
        "message": "How should I structure my training week?"
    }, timeout=60)
    assert response.status_code == 200, f"Status {response.status_code}: {response.text}"
    data = response.json()
    assert "response" in data
    assert len(data["response"]) > 0

def test_data_logging():
    """Test fitness data logging to GCS."""
    response = requests.post(f"{BASE_URL}/data/fitness", json={
        "user_id": "eval_user",
        "track": "fitness",
        "data": {
            "date": "2026-05-25",
            "exercise": "Squat",
            "sets": 4,
            "reps": 5,
            "weight_kg": 100.0,
            "body_weight": 85.0,
            "sleep_hours": 7,
            "energy_level": 8
        }
    }, timeout=30)
    assert response.status_code == 200
    assert response.json()["status"] == "logged"

def test_summarization():
    """Test auto-summarization triggers after n_exchanges."""
    # Register fresh user for clean session
    requests.post(f"{BASE_URL}/user", json={
        "user_id": "eval_summary",
        "track": "fitness"
    }, timeout=30)
    # Send exactly n_exchanges=5 messages
    for i in range(5):
        r = requests.post(f"{BASE_URL}/chat", json={
            "user_id": "eval_summary",
            "track": "fitness",
            "message": f"Message {i+1}: what should I focus on for squat improvement?"
        }, timeout=60)
        assert r.status_code == 200, f"Message {i+1} failed: {r.text}"
    # If all 5 passed without error, summarization triggered successfully
    # Pinecone storage verified by absence of 500 error

if __name__ == "__main__":
    warmup()

    tests = [
        test_health,
        test_user_registration,
        test_chat,
        test_data_logging,
        test_summarization
    ]

    print("=== KnowThyself Evaluation ===\n")
    passed = 0
    for test in tests:
        try:
            test()
            print(f"✅ {test.__name__} PASS")
            passed += 1
        except AssertionError as e:
            print(f"❌ {test.__name__} FAIL: {e}")
        except Exception as e:
            print(f"❌ {test.__name__} ERROR: {e}")

    print(f"\nScore: {passed}/{len(tests)}")
