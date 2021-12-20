from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import operator
import time


def test_shopping(driver):
    driver.get("https://www.amazon.com/")
    assert "Amazon.com. Spend less. Smile more" in driver.title
    elem = driver.find_element(By.XPATH, '//*[@id="twotabsearchtextbox"]')
    elem.clear()
    elem.send_keys("case")
    elem.send_keys(Keys.RETURN)
    assert "No results found." not in driver.page_source
    time.sleep(3)

    customer_reviews = {}
    WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.XPATH, '//div[contains(@data-component-type, "s-search-result")]')))
    divs = driver.find_elements(By.XPATH, '//div[contains(@data-component-type, "s-search-result")]')
    for element in divs:
        spans = element.find_elements(By.CSS_SELECTOR, 'span')
        for span in spans:
            if span.get_attribute("aria-label") is not None and "star" not in span.get_attribute("aria-label"):
                reviews = span.get_attribute("aria-label").replace(',', '')
                if reviews.isdigit():
                    customer_reviews[element] = int(reviews)

    amazon_price = 0
    while True:
        max_customer_reviews = max(customer_reviews.items(), key=operator.itemgetter(1))[0]
        try:
            span_price = max_customer_reviews.find_element(By.XPATH, './/span[@class="a-price"]')
            amazon_price = \
            span_price.find_element(By.XPATH, './/span[@class="a-offscreen"]').get_attribute('innerHTML').split('$')[1]
            break
        except Exception:
            customer_reviews.pop(max_customer_reviews)

    # print(amazon_price)
    # time.sleep(3)

    driver.get("https://www.bestbuy.com")
    assert "Best Buy International: Select your Country - Best Buy" in driver.title
    driver.find_element(By.XPATH, '//a[@class="us-link"]').click()

    close = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.XPATH, './/button[@class="c-close-icon c-modal-close-icon"]')))
    close.click()
    elem = driver.find_element(By.XPATH, '//*[@id="gh-search-input"]')
    elem.clear()
    elem.send_keys("case")
    elem.send_keys(Keys.RETURN)
    assert "No results found." not in driver.page_source
    time.sleep(3)

    best_buy_customer_reviews = {}

    WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, '//li[contains(@class, "sku-item")]')))
    lis = driver.find_elements(By.XPATH, '//li[contains(@class, "sku-item")]')
    for element in lis:
        try:
            reviews = element.find_element(By.XPATH, './/span[contains(@class, "c-reviews")]').text.replace('(', '').replace(')', '').replace(' ', '')
            best_buy_customer_reviews[element] = int(reviews)
        except Exception:
            pass
    best_price = 0
    while True:
        max_customer_reviews = max(best_buy_customer_reviews.items(), key=operator.itemgetter(1))[0]
        try:
            div_price = max_customer_reviews.find_element(By.XPATH,
                                                          './/div[contains(@class, "priceView-customer-price")]')
            best_price = \
            div_price.find_element(By.XPATH, './/span[@aria-hidden="true"]').get_attribute('innerHTML').split('$')[1]
            break
        except Exception as e:
            best_buy_customer_reviews.pop(max_customer_reviews)
    # print(best_price)
    # once script completed the line below should be uncommented.
    assert amazon_price > best_price
    driver.close()
