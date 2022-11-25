import requests
import pytest
from api.api import PetFriends
from api.settings import valid_email, valid_pswrd,unvalid_email,unvalid_pswrd,unvalid_auth_key

pf = PetFriends()


def test_get_api_key_for_valid_user(email=valid_email, password=valid_pswrd):
    """Получить api ключ для зарегестрированного пользователя"""
    status, result = pf.get_api_key(email, password)
    assert status == 200
    assert "key" in result


def test_get_all_pets_list_valid_user(filter=None):
    """Получить список ВСЕХ питомцев для зарегестрированного пользователя"""
    _, auth_key = pf.get_api_key(valid_email, valid_pswrd)
    status, result = pf.get_pets_list(auth_key, filter)
    assert status == 200
    assert len(result['pets']) > 0


def test_add_pet_with_photo_for_valid_user(name='Strelka',animal_type='Belka',age='3',pet_photo='images/belka.jpg'):
    """Добавить питомца с фото для зарегистрированного пользователя"""
    _, auth_key=pf.get_api_key(valid_email,valid_pswrd)
    status,result=pf.add_new_pet_with_photo(auth_key,name,animal_type,age,pet_photo)
    assert status==200
    assert result['name']==name

def test_successful_delete_self_pet():
    """Проверяем возможность удаления питомца"""

    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_pswrd)
    _, my_pets = pf.get_pets_list(auth_key, "my_pets")

    # Проверяем - если список своих питомцев пустой, то добавляем нового и опять запрашиваем список своих питомцев
    if len(my_pets['pets']) == 0:
        pf.add_new_pet_with_photo(auth_key, "Суперкот", "кот", "3", "images/cat1.jpg")
        _, my_pets = pf.get_pets_list(auth_key, "my_pets")

    # Берём id первого питомца из списка и отправляем запрос на удаление
    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)

    # Ещё раз запрашиваем список своих питомцев
    _, my_pets = pf.get_pets_list(auth_key, "my_pets")

    # Проверяем что статус ответа равен 200 и в списке питомцев нет id удалённого питомца
    assert status == 200
    assert pet_id not in my_pets.values()


def test_successful_update_self_pet_info(name='Мурзик', animal_type='Котэ', age="5"):
    """Проверяем возможность обновления информации о питомце"""

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_pswrd)
    _, my_pets = pf.get_pets_list(auth_key, "my_pets")

    # Если список не пустой, то пробуем обновить его имя, тип и возраст
    if len(my_pets['pets']) > 0:
        status, result = pf.put_pet(auth_key, my_pets['pets'][0]['id'],name,animal_type,age)

        # Проверяем что статус ответа = 200 и имя питомца соответствует заданному
        assert status == 200
        assert result['name'] == name
    else:
        # если спиок питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")


def test_get_api_key_unvalid_user(email=unvalid_email,password=unvalid_pswrd):
    """проверяем получение клюа для незарегистрированного пользователя"""
    status,result=pf.get_api_key(email,password)
    assert status != 200
    assert "key" not in result


def test_get_my_pets_list_for_unvalid_user(filter='my_pets'):
    """Проверяем может ли незарегестрированный пользователь получить список его питомцев"""
    auth_key = unvalid_auth_key
    status, result = pf.get_pets_list_for_unvalid_user(auth_key, filter)
    assert status != 200


def test_get_all_pets_list_for_unvalid_user(filter=''):
    """Проверяем может ли незарегестрированный пользователь получить список всех питомцев"""
    auth_key = unvalid_auth_key
    status = pf.get_pets_list_for_unvalid_user(auth_key, filter)
    assert status != 200

def test_add_pet_without_photo_for_valid_user(name='Strelka',animal_type='Belka',age='3',pet_photo=""):
    """Добавить питомца без фото для зарегистрированного пользователя, ждем код ответа 400"""
    _, auth_key=pf.get_api_key(valid_email,valid_pswrd)
    status=pf.add_new_pet_without_photo(auth_key,name,animal_type,age,pet_photo)
    assert status==400

def test_add_pet_photo_for_valid_user(pet_photo='images/pit.jpg'):
    """Добавить питомцу фото для зарегестрированного пользователя"""
    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_pswrd)
    _, my_pets = pf.get_pets_list(auth_key, filter="my_pets")

    # Если список не пустой, то пробуем обновить его имя, тип и возраст
    if len(my_pets['pets']) > 0:
        status = pf.add_pet_photo(auth_key, pet_id=my_pets['pets'][0]['id'],pet_photo=pet_photo)

        # Проверяем что статус ответа = 200
        assert status == 200
    else:
        # если спиок питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")

def test_Negative_add_pet_with_name_1000_symbols(name='a'*1000,animal_type='Belka',age='3',pet_photo='images/belka.jpg'):
    """Добавить питомца с фото для зарегистрированного пользователя c именем в 1000 символов, если тест успешен ,
    то выводится сообщение в консоле о баге"""
    _, auth_key=pf.get_api_key(valid_email,valid_pswrd)
    status,result=pf.add_new_pet_with_photo(auth_key,name,animal_type,age,pet_photo)
    if status==200 or result['name']==name:
        print("БАГ!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    assert status==200
    assert result['name']==name
def test_Negative_add_pet_with_animal_type_1000_symbols(name='test',animal_type='b'*1000,age='3',pet_photo='images/belka.jpg'):
    """Добавить питомца с фото для зарегистрированного пользователя cтипом животного в 1000 символов, если тест успешен ,
    то выводится сообщение в консоле о баге"""
    _, auth_key=pf.get_api_key(valid_email,valid_pswrd)
    status,result=pf.add_new_pet_with_photo(auth_key,name,animal_type,age,pet_photo)
    if status==200 or result['name']==name:
        print("БАГ!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    assert status==200
    assert result['name']==name
def test_Negative_add_pet_with_age_1000_symbols(name='test',animal_type='test1',age='3'*1000,pet_photo='images/belka.jpg'):
    """Добавить питомца с фото для зарегистрированного пользователя c возрастом в 1000 символов,
     если тест успешен ,то выводится сообщение в консоле о баге"""
    _, auth_key=pf.get_api_key(valid_email,valid_pswrd)
    status,result=pf.add_new_pet_with_photo(auth_key,name,animal_type,age,pet_photo)
    if status==200 or result['name']==name:
        print("БАГ!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    assert status==200

    assert result['name']==name

def test_Negative_add_pet_with_age_negative_values(name='test',animal_type='test1',age='-3',pet_photo='images/belka.jpg'):
    """Добавить питомца с фото для зарегистрированного пользователя c возрастом с отрицательным значением,
     если тест успешен ,то выводится сообщение в консоле о баге"""
    _, auth_key=pf.get_api_key(valid_email,valid_pswrd)
    status,result=pf.add_new_pet_with_photo(auth_key,name,animal_type,age,pet_photo)
    if status==200 or result['name']==name:
        print("БАГ!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    assert status==200

    assert result['name']==name
def test_Negative_successful_delete_another_pet():
    """Проверяем возможность удаления не своего питомца ,
    Если тест успешен, то выводится сообщение в консоле о баге"""

    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_pswrd)
    _, other_pets = pf.get_pets_list(auth_key, filter=None)


    # Берём id первого питомца из списка и отправляем запрос на удаление
    pet_id = other_pets['pets'][-1]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)

    # Ещё раз запрашиваем список своих питомцев
    _, other_pets = pf.get_pets_list(auth_key, filter=None)

    if status==200 or pet_id not in other_pets.values():
        print("\nБАГ!!!!!!!!!!!!!!")

    # Проверяем что статус ответа равен 200 и в списке питомцев нет id удалённого питомца
    assert status == 200
    assert pet_id not in other_pets.values()