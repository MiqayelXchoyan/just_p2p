from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def get_bingx_rub():
    options = Options()
    options.headless = True
    options.add_argument('--headless=new')
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--disable-infobars")
    options.add_argument("--disable-extensions")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                     "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36")
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install() , options=options))
    driver.implicitly_wait(3)

    def wait_and_click_modal():
        try:
            modal_button = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "div.ant-modal-wrap button span"))
            )
            modal_button.click()
        except:
            pass

    def get_trade_price():
        try:
            price = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, "td:nth-child(2) div"))
            ).text
            return price
        except:
            return None

    try:
        # Покупка
        driver.get("https://bingx.paycat.com/en/p2p/self-selection?fiat=RUB&type=1")
        wait_and_click_modal()
        buy_price = get_trade_price()

        # Продажа
        driver.get("https://bingx.paycat.com/en/p2p/self-selection?fiat=RUB&type=2")
        wait_and_click_modal()
        sell_price = get_trade_price()

        return buy_price or "—", sell_price or "—"

    except Exception as ex:
        print("⚠️ Ошибка в BingX (RUB):", ex)
        return "—", "—"

    finally:
        driver.quit()
