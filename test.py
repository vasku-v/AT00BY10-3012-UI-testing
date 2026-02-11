"""
Testing https://lab.fi/fi

Automated UI tests for the LAB.fi website using Selenium WebDriver and pytest.
"""
import pytest
import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@pytest.fixture
def driver():
    service = Service(ChromeDriverManager().install())

    options = webdriver.ChromeOptions()
    # options.add_argument("--force-device-scale-factor=0.5")

    driver = webdriver.Chrome(service=service, options=options)
    driver.maximize_window()
    yield driver
    driver.quit()

def check_cookie_banner(driver):
    try:
        cookie_button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.ID, "ppms_cm_reject-all"))
        )
        cookie_button.click()
        print("Cookie banner accepted")
    except:
        print("No cookie banner found, continuing...")

def take_screenshot(driver, filename):
    os.makedirs("screenshots", exist_ok = True)

    timestamp = int(time.time())
    screenshot_file = f"screenshots/{filename}_{timestamp}.png"
    driver.save_screenshot(screenshot_file)
    print(f"Screenshot saved to {screenshot_file}")

def test_lab_fi_title(driver):
    print("Checking for correct page title")

    driver.get("https://lab.fi/fi")
    time.sleep(2)

    assert "LAB-ammattikorkeakoulu | LAB.fi" in driver.title
    time.sleep(2)

def test_lab_fi_meta_description(driver):
    print("Checking for correct meta description")

    driver.get("https://lab.fi/fi")
    time.sleep(2)

    meta_desc = driver.find_element(By.CSS_SELECTOR, "head > meta[name='description']")
    assert meta_desc.get_attribute("content") == "Opiskelun ja työn parhaat puolet. LAB-ammattikorkeakoulu on työelämän innovaatiokorkeakoulu, joka toimii Lahdessa, Lappeenrannassa ja verkossa."
    time.sleep(2)

def test_page_navigation(driver):
    print("Checking for correct page navigation")

    driver.get("https://lab.fi/fi")
    time.sleep(2)

    check_cookie_banner(driver)

    link = driver.find_element(By.CSS_SELECTOR, "a[href='/fi/koulutus/tekniikka']")
    link.click()

    WebDriverWait(driver, 10).until(EC.url_contains("/fi/koulutus/tekniikka"))

    filename = "screenshot_navigation"
    take_screenshot(driver, filename)

    assert "/fi/koulutus/tekniikka" in driver.current_url
    time.sleep(2)

def test_external_instagram_link(driver):
    print("Checking Instagram external link")

    driver.get("https://lab.fi/fi")
    time.sleep(2)

    check_cookie_banner(driver)

    link = driver.find_element(By.CSS_SELECTOR, "a[href='https://www.instagram.com/labfinland/']")
    link.click()

    WebDriverWait(driver, 10).until(lambda d: len(d.window_handles) > 1)

    driver.switch_to.window(driver.window_handles[1])

    WebDriverWait(driver, 10).until(EC.url_contains("instagram.com"))
    assert "instagram.com" in driver.current_url
    time.sleep(2)

def test_search_bar(driver):
    print("Checking search bar functionality")

    driver.get("https://lab.fi/fi")
    time.sleep(2)

    check_cookie_banner(driver)

    search_icon = driver.find_element(By.CSS_SELECTOR, 
                                      "button[data-once='toggleSearchBar']")
    search_icon.click()

    search_input = driver.find_element(By.CSS_SELECTOR, 
                                       "input[data-drupal-selector='edit-keywords']")
    search_input.send_keys("tekniikka\n")
    
    WebDriverWait(driver, 10).until(EC.url_contains("haku"))

    filename = "screenshot_search"
    take_screenshot(driver, filename)

    assert "haku" in driver.current_url
    time.sleep(2)

def test_front_page(driver):
    print("Checking that the front page looks OK")

    driver.get("https://lab.fi/fi")
    time.sleep(2)
    
    filename = "screenshot_frontpage"
    take_screenshot(driver, filename)

    time.sleep(2)
