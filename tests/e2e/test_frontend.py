# tests/e2e/test_frontend.py

from bs4 import BeautifulSoup
from fastapi.testclient import TestClient

from src.main import app


class TestFrontendIntegration:
    """
    E2E/Integration tests for the Frontend Serving Layer.
    Verifies that the backend correctly serves the static assets and templates.
    """

    def setup_method(self):
        self.client = TestClient(app)

    def test_landing_page_renders_ok(self):
        """
        Verify that the root endpoint returns the landing page.
        """
        response = self.client.get("/")
        assert response.status_code == 200
        assert "text/html" in response.headers["content-type"]
        soup = BeautifulSoup(response.text, "html.parser")
        assert "Spriter | The Future" in soup.select_one("title").text
        assert soup.select_one(".landing-hero") is not None

    def test_dashboard_renders_ok(self):
        """
        Verify that the /dashboard endpoint returns the dashboard.
        """
        response = self.client.get("/dashboard")
        assert response.status_code == 200
        assert "text/html" in response.headers["content-type"]

        # Parse HTML to verify structure
        soup = BeautifulSoup(response.text, "html.parser")
        assert soup.select_one("title").text == "Spriter - Dashboard"
        assert soup.select_one(".app-container") is not None

        # Verify script import
        script = soup.select_one('script[type="module"]')
        assert script is not None
        assert script["src"] == "/static/js/main.js"

        # Verify Views exist
        assert soup.select_one("#dashboard-view") is not None
        assert soup.select_one("#simulator-view") is not None
        assert "hidden" in soup.select_one("#simulator-view")["class"]

    def test_static_files_serving(self):
        """
        Verify that static CSS/JS files are accessible.
        """
        # CSS
        css_response = self.client.get("/static/css/styles.css")
        assert css_response.status_code == 200
        assert "text/css" in css_response.headers["content-type"]

        # JS Services
        js_response = self.client.get("/static/js/services/sprite_service.js")
        assert js_response.status_code == 200
        assert (
            "application/javascript" in js_response.headers["content-type"]
            or "text/javascript" in js_response.headers["content-type"]
        )

    def test_health_check_api_json(self):
        """
        Verify that the API health check is still working and returning JSON
        (Regression test for backend mounting).
        """
        response = self.client.get("/health")
        assert response.status_code == 200
        assert response.json() == {"status": "ok", "version": "0.1.0"}
