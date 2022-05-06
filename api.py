import requests
import json
from requests_toolbelt.multipart.encoder import MultipartEncoder


class PetFriends:
    """api библиотека к веб приложению Pet Friends."""
    def __init__(self):
        self.base_url = 'https://petfriends1.herokuapp.com/'

    def get_api_key(self, email: str, password: str) -> json:
        """Метод делает запрос к API сервера, возвращает статус запроса и результат в формате json
        с уникальным ключом пользователя, найденного по указанным email и password."""

        headers = {
            'email': email,
            'password': password
        }
        res = requests.get(self.base_url + 'api/key', headers=headers)
        status = res.status_code
        result = ''
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    def get_list_of_pets(self, auth_key: json, filter: str = '') -> json:
        """Метод делает запрос к API сервера, возвращает статус запроса и результат со списком найденных питомцев,
        совпадающих с фильтром в формате json. По умолчанию filter - пустое значение: получить список всех питомцев.
        Либо filter - 'my_pets': получить список моих питомцев."""
        headers = {'auth_key': auth_key['key']}
        filter = {'filter': filter}

        res = requests.get(self.base_url+'api/pets', headers=headers, params=filter)

        status = res.status_code
        result = ''
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    def post_create_pet_without_photo(self, auth_key: json, name: str,
                                      animal_type: str, age: str) -> json:
        """Метод делает запрос к API сервера, возвращает статус запроса и результат с данными нового питомца
        в формате json, созданного с использованием указанных данных:
        (name, animal_type, age в формате str; auth_key в формате json)."""
        data = {
                'name': name,
                'animal_type': animal_type,
                'age': age
        }
        headers = {'auth_key': auth_key['key']}

        res = requests.post(self.base_url + 'api/create_pet_simple', headers=headers, data=data)
        status = res.status_code
        result = ''
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    def post_add_information_about_new_pet(self, auth_key: json, name: str,
                                           animal_type: str, age: str, pet_photo: str) -> json:
        """Метод делает запрос к API сервера, возвращает статус запроса
        и результат с данными нового питомца в формате json, созданного с использованием
         указанных данных: (name, animal_type, age, pet_photo в формате str; auth_key в формате json)."""
        data = MultipartEncoder(
            fields={
                'name': name,
                'animal_type': animal_type,
                'age': age,
                'pet_photo': (pet_photo, open(pet_photo, 'rb'), 'image/jpeg')
            })
        headers = {'auth_key': auth_key['key'], 'Content-Type': data.content_type}

        res = requests.post(self.base_url + 'api/pets', headers=headers, data=data)
        status = res.status_code
        result = ''
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    def post_add_photo_of_pet(self, auth_key: json, pet_id: str, pet_photo: str) -> json:
        """Метод делает запрос к API сервера и возвращает статус запроса и результат с
        данными питомца в формате json, фото которого было изменено/добавлено с
        использованием указанных данных: (pet_id, pet_photo в формате str; auth_key в формате json)."""
        data = MultipartEncoder(
            fields={
                'pet_id': pet_id,
                'pet_photo': (pet_photo, open(pet_photo, 'rb'), 'image/jpeg')
            })
        headers = {'auth_key': auth_key['key'], 'Content-Type': data.content_type}

        res = requests.post(self.base_url + '/api/pets/set_photo/'+pet_id, headers=headers, data=data)
        status = res.status_code
        result = ''
        try:
            result = res.json()
        except:
            result = res.text
        return status, result

    def delete_pet_from_database(self, auth_key: json, pet_id: str):
        """Метод делает запрос к API сервера и возвращает статус запроса.
        Код состояния 200 означает, что питомец был успешно удален из базы данных,
        с использованием указанных данных (pet_id в формате str; auth_key в формате json).
        Код ошибки означает, что предоставленный auth_key неверен."""
        data = {
                'pet_id': pet_id,
            }
        headers = {'auth_key': auth_key['key']}

        res = requests.delete(self.base_url + '/api/pets/'+pet_id, headers=headers, data=data)
        status = res.status_code
        result = ''
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    def put_update_information_about_pet(self, auth_key: json, pet_id: str, name,
                                           animal_type, age) -> json:
        """Метод делает запрос к API сервера и возвращает статус запроса
        и результат с измененными данными питомца в формате json, созданный с использованием
        указанных данных: (name, animal_type, age, pet_photo в формате str; auth_key в формате json)."""
        data = {
                'name': name,
                'animal_type': animal_type,
                'age': age,
            }
        headers = {'auth_key': auth_key['key']}

        res = requests.put(self.base_url + '/api/pets/' + pet_id, headers=headers, data=data)
        status = res.status_code
        result = ''
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result