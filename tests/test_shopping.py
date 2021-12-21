from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import operator


def test_shopping(driver):
    driver.get("https://www.amazon.com/")
    assert "Amazon.com. Spend less. Smile more" in driver.title
    elem = driver.find_element(By.XPATH, '//*[@id="twotabsearchtextbox"]')
    elem.clear()
    elem.send_keys("case")
    elem.send_keys(Keys.RETURN)
    assert "No results found." not in driver.page_source

    """enumeration elements"""
    customer_reviews = {}
    WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.XPATH, '//div[contains(@data-component-type, "s-search-result")]')))
    all_products = driver.find_elements(By.XPATH, '//div[contains(@data-component-type, "s-search-result")]')
    for element in all_products:
        number_reviews = element.find_element(By.CSS_SELECTOR, 'span.a-size-base a-color-base s-underline-text').text.replace(',', '')
        assert number_reviews.isdigit()
        customer_reviews[element] = int(number_reviews)  # saving product in dict as key

    amazon_price = 0
    while True:
        """finding max value of reviews and price check"""
        max_customer_reviews = max(customer_reviews.items(), key=operator.itemgetter(1))[0]
        try:
            prod_price_amazon = max_customer_reviews.find_element(By.XPATH, './/span[@class="a-price"]')
            amazon_price = \
            prod_price_amazon.find_element(By.XPATH, './/span[@class="a-offscreen"]').get_attribute('innerHTML').split('$')[1]
            assert amazon_price.isdigit()
            break
        except Exception:
            customer_reviews.pop(max_customer_reviews)
    print(amazon_price)

    driver.get("https://www.bestbuy.com")
    assert "Best Buy International: Select your Country - Best Buy" in driver.title
    driver.find_element(By.XPATH, '//a[@class="us-link"]').click()

    close_popup = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.XPATH, './/button[@class="c-close-icon c-modal-close-icon"]')))
    close_popup.click()  # closing pop up
    elem = driver.find_element(By.XPATH, '//*[@id="gh-search-input"]')
    elem.clear()
    elem.send_keys("case")
    elem.send_keys(Keys.RETURN)
    assert "No results found." not in driver.page_source

    best_buy_customer_reviews = {}

    WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, '//li[contains(@class, "sku-item")]')))
    list_products = driver.find_elements(By.XPATH, '//li[contains(@class, "sku-item")]')
    for element in list_products:
        try:
            reviews_list = element.find_element(By.XPATH, './/span[contains(@class, "c-reviews")]').text.replace('(', '').replace(')', '').replace(' ', '')
            assert reviews_list.isdigit()
            best_buy_customer_reviews[element] = int(reviews_list)
        except Exception:
            pass
    best_price = 0
    while True:
        max_customer_reviews = max(best_buy_customer_reviews.items(), key=operator.itemgetter(1))[0]
        try:
            product_price_best_buy = max_customer_reviews.find_element(By.XPATH,
                                                          './/div[contains(@class, "priceView-customer-price")]')
            best_price = \
            product_price_best_buy.find_element(By.XPATH, './/span[@aria-hidden="true"]').get_attribute('innerHTML').split('$')[1]
            assert best_price.isdigit()
            break
        except Exception:
            best_buy_customer_reviews.pop(max_customer_reviews)
    print(best_price)
    # once script completed the line below should be uncommented.
    assert amazon_price > best_price
    driver.close()
