import json
import requests


class PetFriends:
    def __init__(self):
        self.base_url = "https://petfriends.skillfactory.ru/"

    def get_api_key(self, email: str, password: str) -> json:
        """Метод делает запрос к API сервера и возвращает статус запроса и результат в формате json
        с уникальным ключём пользователя, найденного по указанным email и паролю"""

        headers = {
            "email": email,
            "password": password
        }
        res = requests.get(self.base_url + "api/key", headers=headers)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except:
            result = res.text
        return status, result

    def get_list_of_pets(self, auth_key: json, filter: str = "") -> json:
        """Метод делает запрос к API сервера и возвращает статус запроса и результат в формате json
        со списком найденных питомцев, совпадающих с фильтром. На данный момент фильтр может иметь
        либо пустое значение - получить список всех питомцев, либо 'my_pets' - получить список собственных питомцев"""
        headers = {"auth_key": auth_key["key"]}
        filter = {"filter": filter}

        res = requests.get(self.base_url + "api/pets", headers=headers, params=filter)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except:
            result = res.text
        return status, result

    def add_new_pet(self, auth_key: json, name: str, animal_type: str, age: str, pet_photo: str):
        """Метод отправляет (постит) на сервер данные о добавляемом питомце и возвращает статус
                запроса на сервер и результат в формате JSON с данными добавленного питомца"""
        headers = {"auth_key": auth_key["key"]}
        data = {
            'name': name,
            'animal_type': animal_type,
            'age': age,
        }
        file = {'pet_photo': (pet_photo, open(pet_photo, 'rb'), 'image/jpeg')}
        res = requests.post(self.base_url + 'api/pets', headers=headers, data=data, files=file)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except:
            result = res.text
        return status, result

    def delete_pet_from_basedata(self, auth_key: json, pet_id: json) -> int:
        headers = {"auth_key": auth_key["key"]}
        pet_id = (pet_id["pets"])[0]["id"]
        res = requests.delete(self.base_url + f'api/pets/{pet_id}', headers=headers)
        status = res.status_code
        return status

    def update_pet_info(self, auth_key: json, pet_id: json, name: str, animal_type: str, age: int) -> json:
        """Метод отправляет запрос на сервер об обновлении данных питомуа по указанному ID и
        возвращает статус запроса и result в формате JSON с обновлённыи данными питомца"""

        headers = {'auth_key': auth_key['key']}
        pet_id = (pet_id["pets"])[0]["id"]
        data = {
            'name': name,
            'age': age,
            'animal_type': animal_type
        }

        res = requests.put(self.base_url + f'api/pets/{pet_id}', headers=headers, data=data)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except:
            result = res.text
        return status, result


    def add_new_pet_without_photo(self, auth_key: json, name: str, animal_type: str, age: str):
        """Метод отправляет (постит) на сервер данные о добавляемом питомце без фото и возвращает статус
                запроса на сервер и результат в формате JSON с данными добавленного питомца без фото"""
        headers = {"auth_key": auth_key["key"]}
        data = {
            'name': name,
            'animal_type': animal_type,
            'age': age,
        }
        res = requests.post(self.base_url + 'api/create_pet_simple', headers=headers, data=data)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except:
            result = res.text
        return status, result


    def add_photo_of_pet(self, auth_key: json, pet_id: json, pet_photo: str):
        """Метод отправляет (постит) на сервер фото питомца по его id и возвращает статус
                запроса на сервер и результат в формате JSON с данными питомца с фото"""
        headers = {"auth_key": auth_key["key"]}
        pet_id = (pet_id["pets"])[0]["id"]

        file = {'pet_photo': (pet_photo, open(pet_photo, 'rb'), 'image/jpeg')}
        res = requests.post(self.base_url + f'api/pets/set_photo/{pet_id}', headers=headers, files=file)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except:
            result = res.text
        return status, result