from api import PetFriends
from settings import *


pf = PetFriends()

def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    """Тест для проверки метода get_api_key.
     Проверяет статус код(200), результат на наличие параметра 'key'."""

    status, result = pf.get_api_key(email, password)

    assert status == 200
    assert 'key' in result


def test_get_all_pets_with_valid_key(filter=''):  # filter available values : my_pets (возвращает список "мои питомцы")
    """ Тест для проверки метода get_list_of_pets.
    Проверяет что запрос всех питомцев возвращает не пустой список.
    Для этого сначала получает api ключ и сохраняет в переменную auth_key. Далее, используя этот ключ,
    запрашивает список всех питомцев и проверяет, статус ответа 200 и что список 'pets' не пустой.
    Доступное значение параметра filter - 'my_pets' либо '' """

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)

    assert status == 200
    assert len(result['pets']) > 0


def test_create_pet_simple_without_photo_valid_key(name=valid_new_pets_name,
                                                   animal_type=valid_new_pets_animal_type, age=valid_new_pets_animal_age):
    """ Тест для проверки метода post_create_pet_without_photo. Проверяет запрос добавления нового питомца (без фото)
    с использованием корректных данных. Для этого сначала получает api ключ и сохраняет в переменную auth_key.
    Далее, используя этот ключ, добавляет в базу данных нового питомца и проверяет статус ответа 200,
    и что параметры (name,animal_type, age) в ответе соответствуют параметрам (name,animal_type,age) в запросе."""
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    status, result = pf.post_create_pet_without_photo(auth_key, name, animal_type, age)

    assert status == 200
    assert result['name'] == valid_new_pets_name
    assert result['animal_type'] == valid_new_pets_animal_type
    assert result['age'] == valid_new_pets_animal_age


def test_add_information_about_new_pet(name=valid_new_pets_name, animal_type=valid_new_pets_animal_type,
                                       age=valid_new_pets_animal_age, pet_photo=valid_pet_photo_1):
    """ Тест для проверки метода post_add_information_about_new_pet.
            Проверяет запрос добавления нового питомца с использованием корректных данных.
            Для этого сначала получает api ключ и сохраняет в переменную auth_key. Далее, используя этот ключ,
            добавляет в базу данных нового питомца и проверяет статус ответа (200), параметры (name,animal_type, age)
            в ответе соответствуют параметрам (name,animal_type, age) в запросе и параметр "pet_photo" не пустой."""

    _, auth_key = pf.get_api_key(valid_email, valid_password)

    status, result = pf.post_add_information_about_new_pet(auth_key, name, animal_type, age, pet_photo)

    assert status == 200
    assert result['name'] == valid_new_pets_name
    assert result['animal_type'] == valid_new_pets_animal_type
    assert result['age'] == valid_new_pets_animal_age
    assert len(result['pet_photo']) > 0


def test_add_photo_of_pet(name=valid_new_pets_name, animal_type=valid_new_pets_animal_type,
                          age=valid_new_pets_animal_age, pet_photo=valid_pet_photo_1, pet_photo_2=valid_pet_photo_2):
    """Тест для проверки метода post_add_photo_of_pet. Проверяет запрос на добавление/изменение фото питомца
    с использованием корректных данных.(name, animal_type, age, pet_photo_1, pet_photo_2).
    Для этого сначала получает api ключ и сохраняет в переменную auth_key. Далее, используя этот ключ, добавляет в
    базу данных нового питомца, затем добавляет/изменяет фото питомца, проверяет статус запроса (200)
    и несоответствие изначального фото(pet_photo_org) новому(pet_photo_new)"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)

    status, result = pf.post_add_information_about_new_pet(auth_key, name, animal_type, age, pet_photo)
    pet_id = result['id']
    pet_photo_org = result['pet_photo']

    status, result = pf.post_add_photo_of_pet(auth_key, pet_id, pet_photo_2)
    pet_photo_new = result['pet_photo']

    assert status == 200
    assert pet_photo_org != pet_photo_new


def test_delete_pet_from_database(name=valid_new_pets_name,
                                  animal_type=valid_new_pets_animal_type,
                                  age=valid_new_pets_animal_age):
    """Тест для проверки метода delete_pet_from_database. Проверяет запрос на удаление питомца из базы данных,
    используя корректные данные (name, animal_type,age, pet_id). Для этого сначала получает api ключ и сохраняет
    в переменную auth_key. Далее, используя этот ключ, добавляет в базу данных нового питомца, затем получает его
    pet_id и удаляет питомца с данным pet_id из базы данных. Проверяет статус ответа (200)"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.post_create_pet_without_photo(auth_key, name, animal_type, age)
    pet_id = result['id']
    status, result = pf.delete_pet_from_database(auth_key, pet_id)
    assert status == 200


def test_update_information_about_pet(name=valid_new_pets_name,
                                      animal_type=valid_new_pets_animal_type,
                                      age=valid_new_pets_animal_age,):
    """Тест для проверки метода put_update_information_about_pet. Проверяет запрос на добавление/изменение данных питомца
    с использованием корректных данных.(name, animal_type, age). Для этого сначала получает api ключ и сохраняет
    в переменную auth_key. Далее, используя этот ключ, добавляет в базу данных нового питомца, затем получает его
    pet_id и изменяет/добавляет информацию о питомце с данным pet_id в базе данных. Проверяет статус ответа (200),
    параметры (name,animal_type, age)в ответе соответствуют параметрам (name,animal_type, age) в запросе."""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.post_create_pet_without_photo(auth_key, name, animal_type, age)

    pet_id = result['id']
    status, result = pf.put_update_information_about_pet(auth_key, pet_id, name=valid_update_pets_name,
                                                         animal_type=valid_update_pets_animal_type,
                                                         age=valid_update_pets_animal_age)

    assert status == 200
    assert result['name'] == valid_update_pets_name
    assert result['animal_type'] == valid_update_pets_animal_type
    assert result['age'] == valid_update_pets_animal_age

