import requests
import json
from requests_toolbelt.multipart.encoder import MultipartEncoder
class PetFriends:
    def __init__(self):
        self.base_url="https://petfriends.skillfactory.ru/"

    def get_api_key(self,email:str,pswrd:str) -> json:
        """Метод делает запрос на получение Api ключа
         и проверяет статус запроса 200"""


        headers={
            'email':email,
            'password':pswrd
        }
        res=requests.get(self.base_url+'api/key', headers=headers)
        status=res.status_code
        result=""
        try:
            result=res.json()
        except:
            result=res.text
        return status,result
    def get_pets_list(self,auth_key,filter):
        """Метод получет список питомцев и проверяет статус запроса
        Фильтр - по умолчанию"""

        headers={
            'auth_key':auth_key['key']
        }
        filter={'filter':filter}
        res=requests.get(self.base_url+'api/pets',headers=headers,params=filter)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except:
            result = res.text
        return status, result
    def add_new_pet_with_photo(self, auth_key: json, name: str, animal_type: str,
                    age: str, pet_photo: str) -> json:
        """Метод отправляет (постит) на сервер данные о добавляемом питомце с фото и возвращает статус
        запроса на сервер и результат в формате JSON с данными добавленного питомца"""

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
        result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        print(result)
        return status, result
    def delete_pet(self, auth_key: json, pet_id: str) -> json:
        """Метод отправляет на сервер запрос на удаление питомца по указанному ID и возвращает
        статус запроса и результат в формате JSON с текстом уведомления о успешном удалении.
        status при этом = 200"""
        headers = {'auth_key': auth_key['key']}

        res = requests.delete(self.base_url + 'api/pets/' + pet_id, headers=headers)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result
    def put_pet(self, auth_key: json, pet_id: str, name: str, animal_type: str,
                    age: str) -> json:
        """Метод отправляет на сервер запрос на изменение питомца по указанному ID и возвращает
        статус запроса и результат в формате JSON с текстом уведомления о успешном изменении.
        status при этом = 200"""
        data =  {
                  'name': name,
                  'animal_type': animal_type,
                  'age': age
              }
        headers = {'auth_key': auth_key['key']}

        res=requests.put(self.base_url+'/api/pets/'+pet_id, headers=headers,data=data)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result



    def get_pets_list_for_unvalid_user(self,auth_key,filter):
        """Метод получет список питомцев и проверяет статус запроса для незарегестрированного пользователя
        Фильтр - по умолчанию"""

        headers={
            'auth_key':auth_key
        }
        filter={'filter':filter}
        res=requests.get(self.base_url+'api/pets',headers=headers,params=filter)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except:
            result = res.text
        return status, result

    def add_new_pet_without_photo(self, auth_key: json, name: str, animal_type: str, age: str,pet_photo) -> json:
        """Метод отправляет (постит) на сервер данные о добавляемом питомце без фото и возвращает статус
        запроса на сервер и результат в формате JSON с данными добавленного питомца"""

        data ={
                'name': name,
                'animal_type': animal_type,
                'age': age,
                'pet_photo':pet_photo
            }
        headers = {'auth_key': auth_key['key']}

        res = requests.post(self.base_url + 'api/pets', headers=headers, data=data)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status

    def add_pet_photo(self, auth_key: json, pet_id, pet_photo: str) -> json:
        """Метод добавляет питомцу фото и возвращает статус
        запроса на сервер """

        data = MultipartEncoder(
            fields={
                'pet_photo': (pet_photo, open(pet_photo, 'rb'), 'image/jpeg')
            })
        headers = {'auth_key': auth_key['key'], 'Content-Type': data.content_type}

        res = requests.post(self.base_url + 'api/pets/set_photo/' + pet_id, headers=headers, data=data)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status