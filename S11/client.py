import requests

BASE_URL = "http://127.0.0.1:8000"

def run_client_tests():
    print("--- Запуск тестирования клиентского приложения ---")
    
    # 1. Пробуем создать дисциплину
    test_data = {"name": "Информационные системы", "code": "ИСП.11"}
    response = requests.post(f"{BASE_URL}/disciplines/", json=test_data)
    print("Создание дисциплины:", response.status_code, response.json())
    
    if response.status_code == 200:
        disc_id = response.json().get("id")
        
        # 2. Получаем дисциплину по ID
        get_resp = requests.get(f"{BASE_URL}/disciplines/{disc_id}")
        print("Получение по ID:", get_resp.status_code, get_resp.json())
        
        # 3. Обновляем данные
        update_data = {"name": "Информационные системы и программирование"}
        up_resp = requests.put(f"{BASE_URL}/disciplines/{disc_id}", json=update_data)
        print("Обновление дисциплины:", up_resp.status_code, up_resp.json())
        
        # 4. Удаление (деактивация)
        del_resp = requests.delete(f"{BASE_URL}/disciplines/{disc_id}")
        print("Удаление (деактивация):", del_resp.status_code, del_resp.json())

if __name__ == "__main__":
    try:
        run_client_tests()
    except requests.exceptions.ConnectionError:
        print("Ошибка: Сервер service.py не запущен на порту 8000!")