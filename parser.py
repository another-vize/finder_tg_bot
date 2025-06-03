from bs4 import BeautifulSoup as bs
from selenium import webdriver
import time

# Модифицированная функция парсера
def parser(channel_link, keyword):
    driver = webdriver.Firefox()
    try:
        driver.get(f'{channel_link}?q={keyword}')
        
        # Даем странице время загрузиться
        driver.implicitly_wait(5)
        
        messages = []
        for _ in range(10):
            page_html = driver.page_source
            soup = bs(page_html, 'html.parser')
            
            datas = soup.find_all('div', class_='tgme_widget_message_service_date')
            news = soup.find_all('div', class_='tgme_widget_message_text js-message_text before_footer')
                        
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            
        for data, new in zip(datas, news):
            messages.append(f"{data.text}____{new.text}")
                
        return "\n\n".join(messages) if messages else "Ничего не найдено"
        
    finally:
        driver.close()
        driver.quit()