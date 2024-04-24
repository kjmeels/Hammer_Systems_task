# Hammer_systems

API реферальной системы

Ручка ```/api/users/get_code/``` - позволяет получить пользователю код для подтверждения номера

Ручка ```/api/users/validate_code/``` - позволеяет подтвердить номер пользователю и авторизироваться 

Ручка ```/api/users/send_invite_code/``` - позволяет отправить инвайт-код другого пользователя

Ручка ```/api/users/{username}/``` - позовлет получить данные (номер телефона и 
список номеров, которые использовали инвайт-код) пользователя 

## ENVs:
```
SITE_HOST=localhost
SECRET_KEY=my_secret_key
DEBUG=True
POSTGRES_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_PORT=5432
```

## Third party packages:
```
rest_framework
drf_spectacular
phonenumbers
django-phonenumber-field
```

### Локальный запуск проекта 
```shell
docker compose build
docker compose up
```

| Доступ  | Ссылка                          |
|---------|---------------------------------|
| Админка | http://127.0.0.1:8000/admin/    |
| Сваггер | http://127.0.0.1:8000/api/docs/ |
