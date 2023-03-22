import collections
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By



@pytest.fixture(autouse=True)
def testing():
    pytest.driver = webdriver.Chrome("C:/Users/User/Desktop/Selenium/chromedriver.exe")
    # Задаем размер открываемого окна браузера
    pytest.driver.set_window_size(1920, 1080)
    # Переходим на страницу авторизации
    pytest.driver.get('http://petfriends.skillfactory.ru/login')

    yield

    pytest.driver.quit()

def test_pet_cards():
    # Вводим email
    pytest.driver.find_element(By.ID, 'email').send_keys('testz21@gmail.com')
    # Вводим пароль
    pytest.driver.find_element(By.ID, 'pass').send_keys('qwerty')
    # Нажимаем на кнопку входа в аккаунт
    pytest.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
    # Проверяем, что мы оказались на главной странице с питомцами пользователя
    assert pytest.driver.find_element(By.TAG_NAME, 'h1').text == "PetFriends"

    pytest.driver.implicitly_wait(2)
    images = pytest.driver.find_elements(By.CSS_SELECTOR, '.card-deck.card-img-top')
    pytest.driver.implicitly_wait(2)
    names = pytest.driver.find_elements(By.CSS_SELECTOR, '.card-deck.card-title')
    pytest.driver.implicitly_wait(2)
    descriptions = pytest.driver.find_elements(By.CSS_SELECTOR, '.card-deck.card-text')

    for i in range(len(names)):
        assert images[i].get_attribute('src') != ''
        assert names[i].text != ''
        assert descriptions[i].text != ''
        assert ', ' in descriptions[i]
        parts = descriptions[i].text.split(", ")
        assert len(parts[0]) > 0
        assert len(parts[1]) > 0

def test_pet_table():
    # Вводим email
    pytest.driver.find_element(By.ID, 'email').send_keys('testz21@gmail.com')
    # Вводим пароль
    pytest.driver.find_element(By.ID, 'pass').send_keys('qwerty')
    # Нажимаем на кнопку входа в аккаунт
    WebDriverWait(pytest.driver, 2).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'button[type="submit"]')))
    pytest.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
    # Нажимаем на кнопку входа на страницу с питомцами пользователя
    WebDriverWait(pytest.driver, 2).until(EC.presence_of_element_located((By.LINK_TEXT, 'Мои питомцы')))
    pytest.driver.find_element(By.LINK_TEXT, 'Мои питомцы').click()
    WebDriverWait(pytest.driver, 2).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div[1]')))
    text_for_count = pytest.driver.find_element(By.XPATH, '/html/body/div[1]/div/div[1]')
    count_pets = int(text_for_count.text.split('\n')[1].split(":")[1])
    half_count_pets = count_pets / 2

    #Проверяем, что мы оказались на главной странице с питомцами пользователя
    assert pytest.driver.find_element(By.TAG_NAME, 'h2').text == "Евгениус"
    list_row = pytest.driver.find_elements(By.TAG_NAME, 'tr')
    #Проверяем, количество присутствующих питомцев с количеством из статистики пользователя
    assert count_pets == len(list_row) - 1
    list_img = []
    list_name = []
    list_type = []
    list_age = []

    for each_elem in list_row:
        list_parameters = each_elem.find_elements(By.TAG_NAME, 'td')
        if len(list_parameters) > 0:
            if list_parameters[0] != "":
                list_name.append(list_parameters[0].text)
            if list_parameters[1] != "":
                list_type.append(list_parameters[1].text)
            if list_parameters[1] != "":
                list_age.append(list_parameters[2].text)
            if each_elem.find_element(By.TAG_NAME, 'img').get_attribute('src') != "":
                list_img.append(each_elem.find_element(By.TAG_NAME, 'img').get_attribute('src'))

    # #Проверяем, хотя бы у половины питомцев есть фото?
    assert len(list_img) > half_count_pets

    # Проверяем, у всех ли питомцев есть имя, порода, возраст
    for i in range(len(list_name)):
        assert list_name[i] != ''
        assert list_type[i] != ''
        assert list_age[i] != ''

    # Проверям, есть ли у питомцев повторяющиеся имена
    dictionary_duplicate = collections.Counter(list_name)
    assert len(dictionary_duplicate) > 0