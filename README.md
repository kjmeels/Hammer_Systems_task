# Hammer_systems



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
```

### Локальный запуск проекта 
```shell
docker compose build
docker compose up
```

| Доступ  | Ссылка                        |
|---------|-------------------------------|
| Админка | http://0.0.0.0:8000/admin/    |
| Сваггер | http://0.0.0.0:8000/api/docs/ |
