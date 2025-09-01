import pytest
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# -----------------------------
# Configuration
# -----------------------------
WAZUH_URL = "https://20.220.18.183"
API_URL = "https://20.220.18.183:55000"  # Wazuh API endpoint
TEST_USERNAME = "kibanserve"
TEST_PASSWORD = "kibanserve"


# -----------------------------
# Pytest fixture for Selenium
# -----------------------------
@pytest.fixture(scope="session")
def chrome_driver():
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-extensions")
    options.add_argument("--remote-debugging-port=9222")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    yield driver
    driver.quit()


# -----------------------------
# UI Tests
# -----------------------------
def test_dashboard_https_and_login_elements(chrome_driver):
    chrome_driver.get(WAZUH_URL)

    # Check HTTPS
    assert chrome_driver.current_url.startswith("https://"), "Dashboard is not HTTPS"

    # Check page title
    assert "Wazuh" in chrome_driver.title, f"Unexpected page title: {chrome_driver.title}"

    # Wait for login form elements
    wait = WebDriverWait(chrome_driver, 10)
    username_field = wait.until(EC.presence_of_element_located((By.ID, "username")))
    password_field = wait.until(EC.presence_of_element_located((By.ID, "password")))
    login_button = wait.until(EC.presence_of_element_located((By.XPATH, "//button[@type='submit']")))

    assert username_field.is_displayed() and password_field.is_displayed() and login_button.is_displayed(), \
        "Login form elements are not visible"


def test_dashboard_login(chrome_driver):
    chrome_driver.get(WAZUH_URL)
    wait = WebDriverWait(chrome_driver, 10)

    # Fill in login form
    username_field = wait.until(EC.presence_of_element_located((By.ID, "username")))
    password_field = wait.until(EC.presence_of_element_located((By.ID, "password")))
    login_button = wait.until(EC.presence_of_element_located((By.XPATH, "//button[@type='submit']")))

    username_field.send_keys(TEST_USERNAME)
    password_field.send_keys(TEST_PASSWORD)
    login_button.click()

    # Check landing page element after login (example: dashboard main panel)
    landing_panel = wait.until(EC.presence_of_element_located((By.ID, "dashboard-main-panel")))
    assert landing_panel.is_displayed(), "Landing panel not found after login"


# -----------------------------
# API Health Check
# -----------------------------
def test_wazuh_api_health():
    try:
        response = requests.get(f"{API_URL}/manager/info", auth=(TEST_USERNAME, TEST_PASSWORD),
                                verify=False, timeout=5)  # skip SSL verification for self-signed
        assert response.status_code == 200, f"API returned status {response.status_code}"

        data = response.json()
        assert "version" in data, "Missing 'version' in API response"
        assert "cluster_name" in data, "Missing 'cluster_name' in API response"
    except Exception as e:
        pytest.fail(f"API health check failed: {e}")
