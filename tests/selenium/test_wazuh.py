import os
import json
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

# -----------------------------
# Configuration
# -----------------------------
WAZUH_URL = os.getenv("WAZUH_URL", "https://20.220.18.183")
TEST_USERNAME = os.getenv("kibanaserver")
TEST_PASSWORD = os.getenv("kibanaserver")
API_URL = os.getenv("WAZUH_API_URL", "https://20.220.18.183:55000")

# -----------------------------
# Selenium Setup
# -----------------------------
chrome_options = Options()
chrome_options.add_argument("--headless")  # run headless
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(options=chrome_options)

try:
    # 1. Navigate to Wazuh dashboard
    driver.get(WAZUH_URL)

    # 2. Validate HTTPS (simple check via URL)
    assert driver.current_url.startswith("https://"), "Dashboard not reachable over HTTPS"

    # 3. Validate page title and login form elements
    print("Page title:", driver.title)
    assert "Wazuh" in driver.title, "Unexpected page title"

    # Wait for login form elements
    wait = WebDriverWait(driver, 10)
    username_field = wait.until(EC.presence_of_element_located((By.ID, "username")))
    password_field = wait.until(EC.presence_of_element_located((By.ID, "password")))
    login_button = wait.until(EC.presence_of_element_located((By.XPATH, "//button[@type='submit']")))

    print("Login form elements are present")

    # 4. Optional: login using test account
    if TEST_USERNAME and TEST_PASSWORD:
        username_field.send_keys(TEST_USERNAME)
        password_field.send_keys(TEST_PASSWORD)
        login_button.click()

        # Validate landing page element (example: dashboard main panel)
        landing_panel = wait.until(EC.presence_of_element_located((By.ID, "dashboard-main-panel")))
        print("Successfully logged in, landing panel found")

finally:
    driver.quit()

# -----------------------------
# API Health Check
# -----------------------------
try:
    response = requests.get(f"{API_URL}/manager/info", verify=False, timeout=5)  
    assert response.status_code == 200, f"API returned status {response.status_code}"
    data = response.json()
    # Simple schema validation
    assert "version" in data, "Missing 'version' in API response"
    assert "cluster_name" in data, "Missing 'cluster_name' in API response"
    print("API health check passed:", json.dumps(data, indent=2))
except Exception as e:
    print("API health check failed:", e)

