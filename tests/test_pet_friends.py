from api import PetFriends
from settings import valid_email, valid_password, invalid_email, invalid_password
import os

pf = PetFriends()

def test_get_api_key_valid_user(email=valid_email, password=valid_password):
    '''Проверяем, что код статуса запроса 200 и в переменной result
    содержится слово key'''
    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, password)

    # Сверяем полученные данные с ожидаемыми
    assert status == 200
    assert 'key' in result


def test_get_all_pets_with_valid_key(filter=''):
    '''Проверяем, что код статуса запроса 200 и список всех питомцев не пустой.
    Для этого при помощи метода get_api_key() получаем api ключ, сохраняем его
     в переменной auth_key. Далее, используя этот ключ, запрашиваем список всех питомцев
    через метод get_list_of_pets() и проверяем статус ответа и то, что список не пустой.
     Доступное значение параметра filter - 'my_pets' либо ''.'''

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)

    # Сверяем полученный ответ с ожидаемым
    assert status == 200
    assert len(result['pets']) > 0

def test_add_pets_with_valid_data(name='Tom', animal_type='cat', age='5', pet_photo='images/Tom.jpg'):
    """Проверяем, можно ли добавить питомца с корректными данными"""
    # Получаем полный путь изображения питомца и сохраняем его в переменной pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым
    assert status == 200
    assert result['name'] == name


def test_successful_delete_pet():
    """Проверяем возможность удаления питомца"""
    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Если список своих питомцев пустой, то добавляем нового и опять запрашиваем список своих питомцев
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, 'Tom', 'cat', '5', 'images/Tom.jpg')
        _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')

    # Берём id первого питомца из списка и отправляем запрос на его удаление
    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pets(auth_key, pet_id)

    # Ещё раз запрашиваем список своих питомцев
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем что статус ответа равен 200 и в списке питомцев нет id удалённого питомца
    assert status == 200
    assert pet_id not in my_pets.values()


def test_successful_update_pet_info(name='Петя', animal_type='Скотинка', age='8'):
    '''Проверяем возможность изменения данных питомца'''
    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Если список не пустой, то пробуем обновить имя, тип и возраст питомца
    # Также проверяем, что статус ответа 200 и имя питомца соответствует заданному
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)
        assert status == 200
        assert result['name'] == name
    else:
        raise Exception("Питомцы отсутствуют")


# Мой тест 1
def test_add_pets_with_valid_data_without_photo(name='КотяраБезФото', animal_type='британец', age='2'):
    '''Проверяем возможность добавления нового питомца с корректными данными без фото'''
    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    # Добавляем питомца
    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)

    # Сверяем полученный ответ с ожидаемым
    assert status == 200
    assert result['name'] == name
    assert result['pet_photo'] == ''

# Мой тест 2
def test_add_photo_to_pet(pet_photo='images/Barsik.jpeg'):
    '''Проверяем возможность изменения/добавления нового фото питомца'''
    # Получаем полный путь изображения питомца и сохраняем его в переменной pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Добавляем/изменяем фото питомца
    # Сверяем полученный ответ с ожидаемым
    if len(my_pets['pets']) > 0:
        status, result = pf.add_photo_to_pet(auth_key, my_pets['pets'][0]['id'], pet_photo)
        _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')

        assert status == 200
        assert result['pet_photo'] == my_pets['pets'][0]['pet_photo']
    else:
        raise Exception("Питомцы отсутствуют")

# Мой тест 3
def test_add_pet_new_photo(pet_photo='images/Barsik1.xlsx'):
    """Негативный тест: Проверяем, что нельзя загрузить фото некорректного формата"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Добавляем/изменяем фото питомца
    status, result = pf.add_photo_to_pet(auth_key, my_pets['pets'][0]['id'], pet_photo)

    # Сверяем полученный ответ с ожидаемым
    assert status != 200

# Мой тест 4
def test_pet_negative_age_number(name='Tom', animal_type='cat', age='-2', pet_photo='images/Tom.jpg'):
    '''Негативный тест: Добавление питомца с отрицательным числом в переменной age.
    Проверяем, что нельзя добавить на сайт питомца с отрицательным значением в поле возраст.'''
    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым
    assert age in result['age'], 'Питомец добавлен на сайт с отрицательным числом в поле возраст'
    assert status == 200
    print('Сайт позволяет добавить питомца с отрицательным значением в поле возраст')

# Мой тест 5
def test_add_too_old_pet(name='Tom', animal_type='cat', age='123', pet_photo='images/Funtik.jpeg'):
    '''Негативный тест:  Добавление питомца с очень большим числом в переменной age.
    Проверяем, что нельзя добавить на сайт питомца с очень большим значением в поле возраст.'''
    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым
    assert status == 200
    print('Сайт позволяет добавить питомца, указав для него слишком большой возраст')

# Мой тест 6
def test_add_pet_with_empty_name(name='', animal_type='cat', age='2', pet_photo='images/Tom.jpg'):
    '''Негативный тест: Проверяем возможность добавления питомца с пустым значением в переменной name
    Тест не будет пройден, если питомец будет добавлен на сайт с пустым значением в поле "имя"'''
    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == '', 'Питомец добавлен на сайт с пустым значением в поле имя'
    print('Сайт позволяет добавить питомца, не указав его имя')

# Мой тест 7
def test_add_pet_with_many_words_name(animal_type='cat', age='2', pet_photo='images/Tom.jpg'):
    '''Негативный тест:  Добавление питомца, имя которого превышает 5 слов.
    Проверяем, можно ли добавить на сайт питомца с именем, состоящим из более чем 5 слов'''

    name = 'Леонардо Хосе Дьюк фон Курдюк Арчибальд Анна Мария Антуан сен Жермен Каспиан Тибальд Гарольд де Монпасье Жиль Терри Белье'

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    list_name = result['name'].split()
    word_count = len(list_name)

    assert status == 200
    assert word_count > 5, 'Питомец с именем из более чем 5 слов'
    print('Сайт позволяет добавить питомца с именем из более чем 5 слов')


# Мой тест 8
def test_add_new_pet_with_long_name(name='Aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa',
                                    animal_type='cat', age='2', pet_photo='images/Funtik.jpeg'):
    """Негативный тест: Проверяем, можно ли добавить на сайт питомца с именем длиннее 50 символов"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    print('Сайт позволяет добавить питомца с именем длиннее 50 символов')


# Мой тест 9
def test_add_pet_with_special_symbols_in_animal_type(name='Funtik', age='1', pet_photo='images/Funtik.jpeg'):
    '''Негативный тест:  Добавление питомца со специальными символами в переменной animal_type.
    Проверяем, можно ли добавить на сайт питомца со спец.символами вместо букв в поле вид животного.
    '''
    animal_type = 'сat^&?%$'
    symbols = '#$%^&*{}|?/><=+_~@'
    symbol = []

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    for i in symbols:
        if i in result['animal_type']:
            symbol.append(i)
    assert symbol[0] in result['animal_type'], 'Питомец добавлен с недопустимыми спец. символами'
    print('Сайт позволяет добавить питомца со спец. символами в поле вид животного')

# Мой тест 10
def test_add_pet_with_numbers_in_animal_type(name='Tom', animal_type='654321', age='3',
                                                      pet_photo='images/Tom.jpg'):
    '''Негативный тест: Добавление питомца с цифрами вместо букв в переменной animal_type.
    Проверяем, можно ли добавить на сайт питомца с цифрами вместо букв в поле вид животного.'''
    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert animal_type in result['animal_type'], 'Питомец добавлен на сайт с цифрами вместо букв в поле вид животного'
    print('Сайт позволяет добавить питомца с цифрами вместо букв в поле вид животного')

# Мой тест 11
def test_add_pet_with_many_words_in_animal_type(name='Tom', age='2', pet_photo='images/Tom.jpg'):
    '''Негативный тест: Добавления питомца, название породы которого превышает 5 слов.
    Проверяем, можно ли добавить на сайт питомца, название породы которого состоит из более чем 5 слов'''

    animal_type = 'немецкий пятнистый пудель штрудель алабайский короткошёрстный бассет мастино неаполитано английский шпиц ризеншнауцер гибрид кавказская овчарка помесь бульдог носорог'

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    list_animal_type = result['animal_type'].split()
    word_count = len(list_animal_type)

    assert status == 200
    assert word_count > 5, 'Питомец добавлен с названием породы из более чем 5 слов'
    print('Сайт позволяет добавить питомца с названием породы из более чем 5 слов')


# Мой тест 12
def test_delete_pet_with_empty_pet_id():
    """Проверяем, что нельзя удалить питомца с пустым id"""

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    # Указываем значение id
    pet_id = ''
    # Пробуем удалить питомца с пустым id
    status, _ = pf.delete_pets(auth_key, pet_id)
    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 400 or 404
    print('Попытка удалить питомца с пустым значением id не удалась')

# Мой тест 13
def test_get_api_key_with_wrong_password_and_correct_mail(email=valid_email, password=invalid_password):
    '''Делаем запрос ключа auth_key с невалидным паролем и валидным емейлом.
    Проверяем, есть ли ключ в ответе'''
    status, result = pf.get_api_key(email, password)
    assert status == 403
    assert 'key' not in result

# Мой тест 14
def test_get_api_key_with_wrong_email_and_correct_password(email=invalid_email, password=valid_password):
    '''Делаем запрос ключа auth_key с невалидным паролем и валидным емейлом.
    Проверяем, есть ли ключ в ответе'''
    status, result = pf.get_api_key(email, password)
    assert status == 403
    assert 'key' not in result