from api import PetFriends
from settings import valid_email, valid_password
import os

pf = PetFriends()


def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    """ Проверяем что запрос api ключа возвращает статус 200 и в результате содержится слово key"""
    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, password)
    assert status == 200
    assert "key" in result


def test_get_all_pets_with_valid_key(filter=""):
    """ Проверяем что запрос всех питомцев возвращает не пустой список.
        Для этого сначала получаем api ключ и сохраняем в переменную auth_key. Далее используя этого ключ
        запрашиваем список всех питомцев и проверяем что список не пустой.
        Доступное значение параметра filter - 'my_pets' либо '' """
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 200
    assert len(result["pets"]) > 0


def test_add_new_pet_with_valid_data(name='Гоша', animal_type='бегемот', age='1', pet_photo='images/2.jpg'):
    """Проверяем что можно добавить питомца с корректными данными"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    #pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name


def test_delete_pet_from_basedata():
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем - если список своих питомцев пустой, то добавляем нового и опять запрашиваем список своих питомцев
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, 'Гоша', 'бегемот', "1", "images/2.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    status = pf.delete_pet_from_basedata(auth_key, my_pets)
    assert status == 200


def test_successful_update_self_pet_info(name="Маруся", animal_type='Носорог', age=40):
    """Проверяем возможность обновления информации о питомце"""

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Если список не пустой, то пробуем обновить его имя, тип и возраст
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets, name, animal_type, age)

        # Проверяем что статус ответа = 200 и имя питомца соответствует заданному
        assert status == 200
        assert result['name'] == name
    else:
        # если список питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")


def test_add_new_pet_without_photo_with_valid_data(name='Миша', animal_type='Змея', age='6'):
    """Проверяем, что можно добавить питомца с корректными данными без фото"""
    # Запрашиваем ключ api и сохраняем в переменную auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name


def test_add_foto_of_pet_with_valid_data(pet_photo='images/1.jpg'):
    """Проверяем что можно добавить фото питомцу с корректными данными"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    #pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Если список не пустой и есть животные без фото, то пробуем добавить фото питомцу
    if len(my_pets['pets']) > 0:
        status, result = pf.add_photo_of_pet(auth_key, my_pets, pet_photo)
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

        assert status == 200
        assert result['pet_photo'] == my_pets['pets'][0]['pet_photo']
    else:
        raise Exception("Питомцы отсутствуют")


def test_add_new_pet_without_photo_with_invalid_data(name='Миша', animal_type='Змея', age='-86'):
    """Негативный тест. Проверяем, что нельзя добавить питомца с отрицательным числом в поле"""
    # Запрашиваем ключ api и сохраняем в переменную auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 400


def test_add_new_pet_without_name(name='', animal_type='бегемот', age='1', pet_photo='images/2.jpg'):
    """Проверяем что нельзя добавить питомца с пустым поле имени"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    #pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 400
    assert result['name'] != name


def test_get_api_key_with_wrong_password_and_correct_mail(email=valid_email, password="0"):
    """ Проверяем запрос с невалидным паролем и с валидным емейлом. Проверяем нет ли ключа в ответе"""
    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result

    status, result = pf.get_api_key(email, password)
    assert status == 403
    assert "key" not in result


def test_get_api_key_with_correct_password_and_wrong_mail(email="0", password=valid_password):
    """ Проверяем запрос с невалидным email и с валидным паролем. Проверяем нет ли ключа в ответе"""
    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result

    status, result = pf.get_api_key(email, password)
    assert status == 403
    assert "key" not in result