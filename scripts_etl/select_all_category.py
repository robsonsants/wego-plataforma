import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
import time, csv, requests, os, redis
from pymongo import MongoClient
import base64

# Configuração inicial do Selenium e WebDriver
chrome_options = webdriver.ChromeOptions()
driver = webdriver.Chrome(options=chrome_options)
driver.maximize_window()  # Maximiza a janela do navegador
wait = WebDriverWait(driver, 30)

r = redis.Redis(
  host='redis-10819.c80.us-east-1-2.ec2.redns.redis-cloud.com',
  port=10819,
  password='*****')

# Função para armazenar dados no Redis
def store_in_redis(event_data):
    # Converta os dados do evento para o formato JSON
    event_json = json.dumps(event_data)
    # Armazene os dados do evento no Redis
    r.rpush('scraped_events', event_json)
    print(f"Armazenado no Redis: {event_json}")

# 1 ler as categorias automaticamente
# Lista de categorias a serem processadas
categorias = ["Festas e shows", "Cursos e Workshops", "Saúde e Bem-Estar", "Infantil", "Religião e Espiritualidade",
              "Esportes", "Games e Geek", "Gastronomia", "Moda e Beleza", "Arte, Cinema e Lazer", "Pride"]

# Navega para a página desejada
driver.get('https://www.sympla.com.br/eventos/rio-de-janeiro-rj/todos-eventos')
# Conjunto para manter o controle dos eventos processados e evitar duplicações
eventos_processados = set()

# Tenta fechar o pop-up de cookies
try:
    close_cookies_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".onetrust-close-btn-handler.onetrust-close-btn-ui.banner-close-button.ot-close-icon")))
    close_cookies_button.click()
except (TimeoutException, NoSuchElementException):
    print("Pop-up de cookies não encontrado ou já fechado.")

# Processa cada categoria
for categoria in categorias:
    start_time = time.time()
    # Abre o seletor de categorias
    try:
        category_selector_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".FilterButtonstyle__ButtonLabel-sc-15y04i8-3.bAzaCa")))
        category_selector_button.click()

        specific_category = wait.until(EC.element_to_be_clickable((By.XPATH, f"//div[contains(text(), '{categoria}')]")))
        specific_category.click()
    except (TimeoutException, NoSuchElementException):
        print(f"Não foi possível selecionar a categoria {categoria}.")
        continue

    # Navega pelas páginas da categoria
    pagina_atual = 1
    while True:
        print(f"Processando página {pagina_atual} da categoria '{categoria}'...")

        with open(f'Sympla_{categoria}.csv', mode='a', newline='', encoding='utf-8') as file:  # modo 'a' para adicionar dados
            writer = csv.writer(file)
            if pagina_atual == 1:
                writer.writerow(['Nome do Evento', 'Data', 'Localização', 'Imagem'])  # Cabeçalho só na primeira página

            # Espera até que os eventos estejam visíveis na página
            try:
                # Espera até que os eventos estejam visíveis na página
                events = wait.until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'a.EventCardstyle__CardLink-sc-1rkzctc-3.eDXoFM.sympla-card')))
            except TimeoutException:
                print(f"Erro ao carregar eventos da página {pagina_atual} da categoria {categoria}.")
                break

            for event in events:
                    try:
                        event_title = event.find_element(By.CSS_SELECTOR, 'h3.EventCardstyle__EventTitle-sc-1rkzctc-7').text

                        # Verifica se o evento já foi processado
                        if event_title in eventos_processados:
                            continue
                        eventos_processados.add(event_title)

                        event_date = event.find_element(By.CSS_SELECTOR, 'div.EventCardstyle__EventDate-sc-1rkzctc-6').text
                        location = event.find_element(By.CSS_SELECTOR, 'div.EventCardstyle__EventLocation-sc-1rkzctc-8').text
                        image_element = event.find_element(By.CSS_SELECTOR, 'div.EventCardstyle__ImageContainer-sc-1rkzctc-1.iiFeFT img')
                        image_url = image_element.get_attribute('src')

                        # Baixa a imagem e converte para base64
                        response = requests.get(image_url)
                        if response.status_code == 200:
                            image_base64 = base64.b64encode(response.content).decode('utf-8')

                        # Armazena os dados do evento no Redis
                        event_data = {'title': event_title, 'date': event_date, 'location': location, 'image_base64': image_base64}
                        store_in_redis(str(event_data))

                        #writer.writerow([event_title, event_date, location, image_url])

                    except NoSuchElementException:
                        print("Um dos elementos não foi encontrado.")
                    except Exception as e:
                        print(f"Ocorreu um erro ao processar o evento: {e}")

        try:
            # Rola 60% da altura da página para baixo
            driver.execute_script("window.scrollBy(0, document.body.scrollHeight * 0.6);")
            time.sleep(2)  # Aguarda um momento para a ação ser concluída

            # Encontra o botão Próximo e clica
            next_button_selector = "button.DesktopPaginatorstyle__PaginationItem-sc-1g1li4n-1.DesktopPaginatorstyle__PrevNext-sc-1g1li4n-2.hNyJjx"
            next_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, next_button_selector)))
            next_button.click()

            pagina_atual += 1
            time.sleep(5)
        except TimeoutException:
            print(f"Última página alcançada ou botão Próximo não encontrado para a categoria {categoria}.")
            break
    
    end_time = time.time()  # Marca o final do processamento da categoria
    time_taken = end_time - start_time  # Calcula o tempo total gasto
    print(f"Tempo gasto para processar a categoria '{categoria}': {time_taken:.2f} segundos")    
    # Após processar todas as páginas da categoria, retorna à página inicial ou à seleção de categorias
    driver.get('https://www.sympla.com.br/eventos/rio-de-janeiro-rj/todos-eventos')

# Fecha o navegador após processar todas as páginas da categoria
driver.quit()
