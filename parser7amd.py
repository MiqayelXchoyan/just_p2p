from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def get_bingx_amd():
    options = Options()
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

    try:
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install() , options=options))
        driver.implicitly_wait(2)

        def wait_and_click_modal():
            try:
                print("⏳ Проверка модального окна...")
                modal_button = WebDriverWait(driver, 3).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "div.ant-modal-wrap button span"))
                )
                modal_button.click()
                print("✅ Модальное окно закрыто.")
            except Exception:
                print("ℹ️ Модального окна нет или оно не кликабельно.")

        def get_trade_price():
            try:
                price = WebDriverWait(driver, 5).until(
                    EC.visibility_of_element_located((
                        By.CSS_SELECTOR,
                        "table > tbody > tr:nth-child(1) > td:nth-child(2) > div"
                    ))
                ).text
                return price
            except Exception as e:
                print(f"⚠️ Ошибка получения цены: {e}")
                return None

        print("🔄 Получение цены покупки AMD...")
        driver.get("https://bingx.paycat.com/en/p2p/self-selection?fiat=AMD&type=1")
        wait_and_click_modal()
        buy_price = get_trade_price()

        print("🔄 Получение цены продажи AMD...")
        driver.get("https://bingx.paycat.com/en/p2p/self-selection?fiat=AMD&type=2")
        wait_and_click_modal()
        sell_price = get_trade_price()

        return buy_price or "—", sell_price or "—"

    except Exception as ex:
        print(f"❌ Общая ошибка BingX AMD: {ex}")
        return "—", "—"

    finally:
        try:
            driver.quit()
        except:
            pass
