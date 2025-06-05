from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime, timedelta
import time
import dateutil.parser

def parser(channel_link, keyword, target_days=7):
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Firefox(options=options)
    
    try:
        messages = []
        driver.get(f'{channel_link}?q={keyword}')
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'tgme_widget_message_wrap')))
        
        # Определяем диапазон дат
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=target_days-1)
        date_range = [start_date + timedelta(days=x) for x in range((end_date-start_date).days + 1)]
        
        collected_messages = {date.strftime('''%d.%m.%Y'''): [] for date in date_range}
        found_dates = set()
        scroll_attempts = 0
        max_attempts = 20
        
        while scroll_attempts < max_attempts:
            scroll_attempts += 1
            
            # Прокрутка и ожидание
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            
            # Парсинг текущего состояния страницы
            soup = bs(driver.page_source, 'html.parser')
            message_wraps = soup.find_all('div', class_='tgme_widget_message_wrap')
            
            for wrap in message_wraps:
                try:
                    # Парсим дату из ISO формата
                    time_element = wrap.find('time')
                    if not time_element or 'datetime' not in time_element.attrs:
                        continue
                        
                    iso_date = time_element['datetime']
                    message_date = dateutil.parser.parse(iso_date).date()
                    date_str = message_date.strftime('%d.%m.%Y')
                    
                    # Проверяем, входит ли дата в нужный диапазон
                    if message_date < start_date:
                        continue
                        
                    # Получаем текст сообщения
                    text_div = wrap.find('div', class_='tgme_widget_message_text')
                    if text_div:
                        message_text = text_div.get_text('\n', strip=True)
                        if date_str in collected_messages:
                            collected_messages[date_str].append(message_text)
                            found_dates.add(date_str)
                            
                except Exception as e:
                    print(f"Ошибка при обработке сообщения: {str(e)}")
                    continue
            
            # Прекращаем если нашли все даты или вышли за диапазон
            oldest_message_date = min([dateutil.parser.parse(wrap.find('time')['datetime']).date() 
                                   for wrap in message_wraps 
                                   if wrap.find('time') and 'datetime' in wrap.find('time').attrs],
                                   default=None)
            
            if oldest_message_date and oldest_message_date < start_date:
                break
                
        # Формируем результат только для найденных дат
        result = []
        for date in sorted(collected_messages.keys(), reverse=True):
            if collected_messages[date]:
                result.append(f"\n📅 {date}\n")
                result.extend([f"• {msg}" for msg in collected_messages[date]])
        
        return '\n'.join(result) if result else f"За последние {target_days} дней ничего не найдено"
        
    except Exception as e:
        return f"Ошибка: {str(e)}"
    finally:
        driver.quit()
