from api import PetFriends
from settings import valid_email, valid_password, invalid_email, invalid_password, invalid_auth_key

pf = PetFriends()

# 1. Ввод неверных регистрационных данных
def test_get_api_key_for_invalid_user(email=invalid_email, password=invalid_password):
    status, result = pf.get_api_key(email, password)
    assert status == 403
    assert 'key' not in result

# 2. Ввод верного пароля и неверного email
def test_get_api_key_for_invalid_email(email=invalid_email, password=valid_password):
    status, result = pf.get_api_key(email, password)
    assert status == 403
    assert 'key' not in result


# 3. Ввод неверного пароля и верного email
def test_get_api_key_for_invalid_password(email=valid_email, password=invalid_password):
    status, result = pf.get_api_key(email, password)
    assert status == 403
    assert 'key' not in result

# 4. Удаление питомца из общего списка (питомца другого пользователя)
def test_unsuccessful_delete_self_pet():
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, pets = pf.get_list_of_pets(auth_key, "pets")

# Берём id любого питомца из общего списка и отправляем запрос на удаление
    pet_id = '0eab9182-05d4-4b9f-a9e1-7a7e525f5ee8'
    status, _ = pf.delete_pet(auth_key, pet_id)
    assert status == 403
# Ожидаем код 403, однако доступ открыт и можно легко удалить любого питомца из приюта (прошу прощения, парочку удалила)


# 5.Обновление информации питомца по id
def test_successful_update_self_pet_info(name='Soul_2', animal_type='Horse_2', age=3):

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Если список не пустой, то пробуем обновить имя, тип и возраст первого питомца по id
    if len(my_pets['pets']) > 0:
        pet_id = '762e2c10-83de-45fe-944e-d9a25614cac0'
        status, result = pf.update_pet_info(auth_key, pet_id, name, animal_type, age)

        # Проверяем что статус ответа = 200 и имя питомца соответствует заданному
        assert status == 200
        assert result['name'] == name
    else:
        # если спиок питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")


# 6. Добавление питомца без фото
def test_create_pet_simple(name='Ted', animal_type='Laska',
                                     age='1'):
    """Проверяем что можно добавить питомца с корректными данными без фото"""

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.create_pet_simple(auth_key, name, animal_type, age)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name


# 7. Добавление фото к последнему добавленному питомцу
def test_set_pet_photo(pet_photo='images/mir.jpg'):
    """Проверяем возможность добавление фото питомца по id"""

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Если список не пустой, то пробуем добавить фото
    if len(my_pets['pets']) > 0:
        status, result = pf.set_pet_photo(auth_key, my_pets['pets'][0]['id'], pet_photo)
        # Проверяем что статус ответа = 200
        assert status == 200
    else:
        # если спиок питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")


# 8. Удаление питомца из своего списка питомца с неверным auth_key

def test_delete_pet_with_invalid_auth_key():
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(invalid_auth_key, pet_id)
    # Проверяем что статус ответа = 403 и доступ закрыт
    assert status == 403

# 9. Обновление информации о питомце с неверным ключом auth_key

def test_update_pet_info_invalid_auth_key(name='Лео', animal_type='Крыса', age=1):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    status, result = pf.update_pet_info(invalid_auth_key, my_pets['pets'][0]['id'], name, animal_type, age)
    assert status == 403

# 10. Удаление питомца
def test_successful_delete_self_pet():

    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем - если список своих питомцев пустой, то добавляем нового и опять запрашиваем список своих питомцев
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Tom", "Cat", "7", "images/de-1200.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Берём id первого питомца из списка и отправляем запрос на удаление
    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)

    # Ещё раз запрашиваем список своих питомцев
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем что статус ответа равен 200 и в списке питомцев нет id удалённого питомца
    assert status == 200
    assert pet_id not in my_pets.values()
