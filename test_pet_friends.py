from api import PetFriends
from settings import valid_email, valid_password, invalid_email, invalid_password


pf = PetFriends()

def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    """Тест на получения ключа API с валидными данными"""
    status, result = pf.get_api_key(email, password)
    assert status == 200
    assert 'key' in result

def test_get_api_key_with_invalid_login(email=invalid_email, password=valid_password):
    """Тест на получения ключа API с неверным логином"""
    status, result = pf.get_api_key(email, password)
    assert status == 403
    assert 'key' not in result

def test_get_api_key_with_invalid_password(email=valid_email, password=invalid_password):
    """Тест на получения ключа API с неверным паролем"""
    status, result = pf.get_api_key(email, password)
    assert status == 403
    assert 'key' not in result

def test_get_all_pets_with_valid_key(filter=''):
    """Тест на то, что в списке питомцев больше одного животного, с валидным ключом API"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 200
    assert len(result['pets']) > 0

def test_get_all_pets_with_invalid_key(filter=''):
    """Тест на то, что в списке питомцев больше одного животного, с неверным ключом API"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    auth_key = {'key': 'ecc18c60009357ae13ba9e44ac5ea152b80178ec7b755c3f57a5c91'}
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 403

def test_post_add_new_info_about_pet_with_valid_key(name='Monja', animal_type='cat', age='1', pet_photo='images/cat.jpg'):
    """Тест на добавление питомца с фото с валидным ключом API"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.post_add_info_about_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 200
    assert result['name'] == name

def test_post_add_new_info_about_pet_with_invalid_key(name='Vanij', animal_type='cat', age='1', pet_photo='images/cat1.jpg'):
    """Тест на добавление питомца с фото с невалидным ключом API"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    auth_key = {'key': 'ecc18c60009357ae13ba9e44ac5ea152b80178ec7b755c3f57a5c91'}
    status, result = pf.post_add_info_about_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 403

def test_successful_delete_self_pet():
    """Тест на удаление питомца с валидным ключом API"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Суперкот", "кот", "3", "images/cat1.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    assert status == 200
    assert pet_id not in my_pets.values()

def test_successful_delete_self_pet_with_invalid_key():
    """Тест на удаление питомца с неверным ключом API"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    auth_key = {'key': 'ecc18c60009357ae13ba9e44ac5ea152b80178ec7b755c3f57a5c91'}
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Суперкот", "кот", "3", "images/cat1.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    assert status == 403

def test_put_update_info_about_pet_with_valid_key(name='Kyzma', animal_type='catty', age='8'):
    """Тест на обновление информации о питомце с валидным ключом API"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    if len(my_pets['pets']) > 0:
        status, result = pf.put_update_info_about_pet(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)
        assert status == 200
        assert result['name'] == name
    else:
        raise Exception("There is no my pets")

def test_put_update_info_about_pet_with_invalid_key(name='Petya', animal_type='catty', age='8'):
    """Тест на обновление информации о питомце с неверным ключом API"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    auth_key = {'key': 'ecc18c60009357ae13ba9e44ac5ea152b80178ec7b755c3f57a5c91'}
    status, result = pf.put_update_info_about_pet(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)
    assert status == 403

def test_post_add_new_info_about_pet_without_foto_with_valid_key(name='Ivan', animal_type='dog', age='5'):
    """Тест на добавление питомца без фото с валидным ключом API"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.post_add_new_pet_without_photo(auth_key, name, animal_type, age)
    assert status == 200
    assert result['name'] == name

def test_post_add_new_info_about_pet_without_foto_with_invalid_key(name='Masha', animal_type='dog', age='5'):
    """Тест на добавление питомца без фото с неверным ключом API"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    auth_key = {'key': 'ecc18c60009357ae13ba9e44ac5ea152b80178ec7b755c3f57a5c91'}
    status, result = pf.post_add_new_pet_without_photo(auth_key, name, animal_type, age)
    assert status == 403

def test_post_add_foto_pet_with_valid_key(pet_photo='images/cat1.jpg'):
    """Тест на добавление фото потимца с валидным ключом"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')
    if len(my_pets['pets']) > 0:
        status, result = pf.post_add_photo_of_pet(auth_key, my_pets['pets'][0]['id'], pet_photo)
        _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')
        assert status == 200
        assert result['pet_photo'] == my_pets['pets'][0]['pet_photo']
    else:
        raise Exception("There is no my pets")

def test_post_add_foto_pet_with_invalid_key(pet_photo='images/dog.jpg'):
    """Тест на добавление фото потимца с неверным ключом"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')
    auth_key = {'key': 'ecc18c60009357ae13ba9e44ac5ea152b80178ec7b755c3f57a5c91'}
    status, result = pf.post_add_photo_of_pet(auth_key, my_pets['pets'][0]['id'], pet_photo)
    assert status == 403