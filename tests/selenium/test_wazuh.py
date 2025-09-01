import pytest
from playwright.sync_api import sync_playwright

@pytest.fixture(scope="session")
def browser():
    with sync_playwright() as p:
        # Launch Chromium headless
        browser = p.chromium.launch(headless=False) 
        context = browser.new_context(ignore_https_errors=True)  
        browser.close()

@pytest.fixture
def page(browser):
    context = browser.new_context()
    page = context.new_page()
    yield page
    context.close()

def test_dashboard_https_and_login_elements(page):
    url = "https://20.220.18.183"
    username = "kibanserve"
    password = "kibanserve"

    # Go to the Wazuh/Kibana login page
    page.goto(url)

    # Fill login form (adjust selectors as needed)
    page.fill('input[name="username"]', username)
    page.fill('input[name="password"]', password)
    page.click('button[type="submit"]')

    # Wait for dashboard to load
    page.wait_for_selector("text=Overview")  # Adjust selector to a dashboard element

    # Assert something visible in dashboard
    assert page.is_visible("text=Overview")

