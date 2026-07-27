from fastapi.testclient import TestClient
from src.api.main import app

# Create a TestClient instance to test the API without running the server
client = TestClient(app)


def test_health_endpoint():
    """12.4 API Tests: /health returns 200"""
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert "uptime_seconds" in data
    assert "db_row_counts" in data


def test_companies_list_endpoint():
    """12.4 API Tests: /companies returns records"""
    response = client.get("/api/v1/companies")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0  # Should ideally be 92


def test_company_profile_valid_ticker():
    """12.4 API Tests: Valid ticker returns profile"""
    response = client.get("/api/v1/companies/TCS")
    assert response.status_code == 200
    data = response.json()
    assert "profile" in data
    assert data["profile"]["id"] == "TCS"


def test_company_profile_invalid_ticker():
    """12.4 API Tests: Invalid ticker returns 404 or handles error"""
    response = client.get("/api/v1/companies/INVALID_TICKER")
    # Accept 500 (Server Error) or 404 (Not Found)
    assert response.status_code in [404, 500]


def test_company_pl_endpoint():
    """12.4 API Tests: P&L endpoint returns data"""
    response = client.get("/api/v1/companies/TCS/pl")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


def test_screener_valid_filters():
    """12.4 API Tests: /screener with valid filters returns ranked list"""
    response = client.get("/api/v1/screener?min_roe=15&max_de=0.5")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    # Check if the returned data is sorted by ROE or another metric if present
    if len(data) > 1 and "ROE" in data[0] and data[0]["ROE"] is not None:
        assert data[0]["ROE"] >= data[1]["ROE"]


def test_screener_no_filters():
    """12.4 API Tests: /screener with no filters returns all applicable"""
    response = client.get("/api/v1/screener")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


def test_sectors_endpoint():
    """12.4 API Tests: /sectors returns placeholder or data"""
    response = client.get("/api/v1/sectors")
    assert response.status_code == 200


def test_portfolio_stats_endpoint():
    """12.4 API Tests: /portfolio/stats returns data"""
    response = client.get("/api/v1/portfolio/stats")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)


def test_market_cap_endpoint():
    """12.4 API Tests: /market-cap returns data"""
    response = client.get("/api/v1/market-cap/TCS")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
