from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def setup_driver():
    """Set up the WebDriver."""
    driver = webdriver.Chrome()  # Ensure you have the ChromeDriver in your PATH
    driver.maximize_window()
    return driver

def login(driver, username, password):
    """Log in to the SauceDemo website."""
    driver.get("https://www.saucedemo.com/")
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "user-name"))
    ).send_keys(username)
    driver.find_element(By.ID, "password").send_keys(password)
    driver.find_element(By.ID, "login-button").click()

def add_items_to_cart(driver):
    """Add the first two items to the cart."""
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "inventory_item"))
    )
    items = driver.find_elements(By.CLASS_NAME, "inventory_item")
    
    for i in range(2):
        items[i].find_element(By.CLASS_NAME, "btn_inventory").click()

def go_to_cart_and_checkout(driver):
    """Go to the cart and proceed to checkout."""
    driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "cart_item"))
    )
    driver.find_element(By.ID, "checkout").click()

def enter_checkout_information(driver, first_name, last_name, postal_code):
    """Enter checkout information."""
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "first-name"))
    )
    driver.find_element(By.ID, "first-name").send_keys(first_name)
    driver.find_element(By.ID, "last-name").send_keys(last_name)
    driver.find_element(By.ID, "postal-code").send_keys(postal_code)
    driver.find_element(By.ID, "continue").click()

def finish_checkout(driver):
    """Finish the checkout process and verify completion."""
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "finish"))
    ).click()
    complete_header = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "complete-header"))
    )
    assert complete_header.text == "THANK YOU FOR YOUR ORDER", "Checkout failed."

def logout(driver):
    """Log out of the SauceDemo website."""
    driver.find_element(By.ID, "react-burger-menu-btn").click()
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "logout_sidebar_link"))
    ).click()

def test_saucedemo():
    driver = setup_driver()
    try:
        login(driver, "standard_user", "secret_sauce")
        add_items_to_cart(driver)
        go_to_cart_and_checkout(driver)
        enter_checkout_information(driver, "John", "Doe", "12345")
        finish_checkout(driver)
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        logout(driver)
        driver.quit()

if __name__ == "__main__":
    test_saucedemo()
