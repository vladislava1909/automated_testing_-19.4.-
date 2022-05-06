from api import PetFriends
from settings import *

pf = PetFriends()
# test 1
def test_get_api_key_for_invalid_email_user(email=invalid_email, password=valid_password):
    """Тест для проверки метода get_api_key с неверным email. Проверяет статус код(403)
     и результат на наличие сообщения об ошибке 'This user wasn\'t found in database' в ответе.
     Код ошибки означает, что указанная комбинация электронной почты пользователя и пароля неверна."""

    status, result = pf.get_api_key(email, password)

    assert status == 403
    assert 'This user wasn\'t found in database' in result

# test 2
def test_get_api_key_for_invalid_password_user(email=valid_email, password=invalid_password):
    """Тест для проверки метода get_api_key с неверным password. Проверяет статус код(403)
     и результат на наличие сообщения об ошибке "This user wasn\'t found in database" в ответе.
     Код ошибки означает, что указанная комбинация электронной почты пользователя и пароля неверна."""

    status, result = pf.get_api_key(email, password)

    assert status == 403
    assert 'This user wasn\'t found in database' in result

# test 3
def test_get_my_pets_with_valid_key(filter='my_pets'):
    """ Тест для проверки метода get_list_of_pets. Проверяет что запрос списка моих питомцев возвращает
    не пустой список. Для этого сначала получает api ключ и сохраняет в переменную auth_key.
    Далее, используя этот ключ, запрашивает список всех питомцев и проверяет, статус ответа (200)
    и что список не пустой. Доступное значение параметра filter - 'my_pets' либо '' """

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)

    assert status == 200
    assert 'pets' in result

# test 4
def test_get_all_pets_with_invalid_key(filter=''):
    """ Тест для проверки метода get_list_of_pets. Проверяет что запрос списка всех питомцев
    не возвращает список при использовании неверного api key(invalid_auth_key),
    статус ответа при использовании неверного api key(invalid_auth_key). Доступное значение параметра filter:
    'my_pets' либо ''."""

    status, result = pf.get_list_of_pets(invalid_auth_key, filter)

    assert status == 403

# test 5
def test_create_pet_simple_without_photo_invalid_key(name=valid_new_pets_name,
                                                     animal_type=valid_new_pets_animal_type,
                                                     age=valid_new_pets_animal_age):
    """ Тест для проверки метода post_create_pet_without_photo. Проверяет запрос добавления нового питомца
    (без фото) при использовании неверного apikey(invalid_auth_key), статус ответа (403).
    Код ошибки означает, что предоставленный auth_key неверен."""

    status, result = pf.post_create_pet_without_photo(invalid_auth_key, name, animal_type, age)

    assert status == 403

# test 6
def test_create_pet_simple_without_photo_empty_data(name=empty_new_pets_name,
                                                     animal_type=empty_new_pets_animal_type,
                                                     age=empty_new_pets_animal_age):
    """ Тест для проверки метода post_create_pet_without_photo. Проверяет запрос добавления нового питомца
    (без фото) при использовании пустых значений (name=empty_new_pets_name,
    animal_type=empty_new_pets_animal_type, age=empty_new_pets_animal_age). Допускаются пустые значения
    данных полей: статус ответа (200),параметры (name,animal_type, age) в ответе соответствуют параметрам
    (name,animal_type,age) в запросе."""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.post_create_pet_without_photo(auth_key, name, animal_type, age)

    assert status == 200
    assert result['name'] == empty_new_pets_name
    assert result['animal_type'] == empty_new_pets_animal_type
    assert result['age'] == empty_new_pets_animal_age

# test 7
def test_add_photo_of_pet_invalid_auth_key(name=valid_new_pets_name, animal_type=valid_new_pets_animal_type,
                                           age=valid_new_pets_animal_age, pet_photo=valid_pet_photo_1, pet_photo_2=valid_pet_photo_2):
    """Тест для проверки метода post_add_photo_of_pet. Проверяет запрос на добавление/изменение фото питомца
    при использовании неверного apikey(invalid_auth_key), статус ответа (403).
    Код ошибки означает, что предоставленный auth_key неверен."""

    _, auth_key = pf.get_api_key(valid_email, valid_password)

    status, result = pf.post_add_information_about_new_pet(auth_key, name, animal_type, age, pet_photo)
    pet_id = result['id']

    status, result = pf.post_add_photo_of_pet(invalid_auth_key, pet_id, pet_photo_2)

    assert status == 403

# test 8
def test_delete_pet_from_database_invalid_auth_key(name=valid_new_pets_name,
                                                   animal_type=valid_new_pets_animal_type,
                                                   age=valid_new_pets_animal_age):
    """Тест для проверки метода delete_pet_from_database. Проверяет запрос на удаление питомца из базы данных,
    при использовании неверного apikey(invalid_auth_key), статус ответа (403).
    Код ошибки означает, что предоставленный auth_key неверен."""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.post_create_pet_without_photo(auth_key, name, animal_type, age)
    pet_id = result['id']
    status, result = pf.delete_pet_from_database(invalid_auth_key, pet_id)
    assert status == 403

# test 9
def test_update_information_about_pet_invalid_auth_key(name=valid_new_pets_name,
                                                       animal_type=valid_new_pets_animal_type,
                                                       age=valid_new_pets_animal_age,):
    """Тест для проверки метода put_update_information_about_pet. Проверяет запрос на добавление/изменение данных питомца
    при использовании неверного apikey(invalid_auth_key), статус ответа (403).
    Код ошибки означает, что предоставленный auth_key неверен."""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.post_create_pet_without_photo(auth_key, name, animal_type, age)

    pet_id = result['id']
    status, result = pf.put_update_information_about_pet(invalid_auth_key, pet_id, name=valid_update_pets_name,
                                                         animal_type=valid_update_pets_animal_type,
                                                         age=valid_update_pets_animal_age)

    assert status == 403

# test 10
def test_update_information_about_pet_empty_data(name=valid_new_pets_name,
                                                 animal_type=valid_new_pets_animal_type,
                                                 age=valid_new_pets_animal_age,):
    """Тест для проверки метода put_update_information_about_pet. Проверяет запрос на добавление/изменение данных питомца
    при использовании пустых значений (name=empty_new_pets_name,
    animal_type=empty_new_pets_animal_type, age=empty_new_pets_animal_age).При использовании пустых полей,
    данные питомца не меняются. Код ответа (200), поля (name, animal_type, age) в ответе совпадают с данными
    (name, animal_type, age) созданного питомца."""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.post_create_pet_without_photo(auth_key, name, animal_type, age)

    orig_name, orig_animal_type, orig_age = result['name'], result['animal_type'], result['age']
    pet_id = result['id']

    status, result = pf.put_update_information_about_pet(auth_key, pet_id, name=empty_new_pets_name,
                                                         animal_type=empty_new_pets_animal_type,
                                                         age=empty_new_pets_animal_age)
    assert status == 200
    assert result['name'] == orig_name
    assert result['animal_type'] == orig_animal_type
    assert result['age'] == orig_age



