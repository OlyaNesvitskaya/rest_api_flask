# REST API для автопарка

Созданы следующие таблицы(модели) - Driver, Vehicle, User

Перечень endpoint'ов с аутентификацией для следующих операций:
User:
+ POST /register - регистрация пользователя
```
Request:
{
    "email": "user@gmail.com",
    "name": "test_user",
    "password": "123456"
}
```

```
Response:
{
    "message": "Registration completed successfully"
}
```


+ POST /login - авторизация 
```
Request:
{
    "email": "user@gmail.com",
    "password": "123456"
}
```

```
Response:
{
    "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY0MjM1NjUwMCwianRpIjoiZGI0ODc4NjgtNTExNi00MWI0LWE5NDItODRkZTQxZTc5NmY0IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6MSwibmJmIjoxNjQyMzU2NTAwLCJleHAiOjE2NDI0NDI5MDB9.jiHx5Ym1VRNZdVBzzdOybdCnhFNJWPqFr8DPffTFwMc"
}
```
Driver:
+ GET /drivers/driver/ - вывод списка водителей

```
Response:
[
    {
        "created_at": "13/01/2022",
        "first_name": "Sergei",
        "id": 1,
        "last_name": "Petrov",
        "updated_at": "13/01/2022"
    },
    {
        "created_at": "14/01/2022",
        "first_name": "Ivan",
        "id": 2,
        "last_name": "Ivanov",
        "updated_at": null
    }
]
```

+ GET /drivers/driver/<driver_id>/ - получение информации по определенному водителю

```
Response:
{
    "created_at": "13/01/2022",
    "first_name": "Sergei",
    "id": 1,
    "last_name": "Petrov",
    "updated_at": "13/01/2022"
}
```

+ POST /drivers/driver/ - создание нового водителя

```
Request:
{
    "first_name": "Denis",
    "last_name": "Mihailov"
}
```

```
Response:
{
    "message": "New driver added successfully."
}
```

+ PUT /drivers/driver/<driver_id>/ - редактирование водителя

```
Request:
{
    "last_name": "Krilov"
}
```

```
Response:
{
    "created_at": "13/01/2022",
    "first_name": "Sergei",
    "id": 1,
    "last_name": "Krilov",
    "updated_at": "16/01/2022"
}
```
+ DELETE /drivers/driver/<driver_id>/ - удаление водителя
```
Response:
{
    "message": "Driver deleted successfully"
}
```

Vehicle:
+ GET /vehicles/vehicle/ - вывод списка машин

```
Response:
[
    {
        "created_at": "14/01/2022",
        "driver": {
            "created_at": "14/01/2022",
            "first_name": "Yurii",
            "id": 5,
            "last_name": "Fokin",
            "updated_at": null
        },
        "driver_id": 5,
        "id": 1,
        "make": "Kia",
        "model": "Sportage",
        "plate_number": "FF 1234 EE",
        "updated_at": "14/01/2022"
    },
    {
        "created_at": "14/01/2022",
        "driver": null,
        "driver_id": null,
        "id": 2,
        "make": "Mersedes",
        "model": "Benz",
        "plate_number": "ЕЕ 1111 РР",
        "updated_at": null
    }
]
```
+ GET /vehicles/vehicle/?with_drivers=yes - вывод списка машин с водителями

```
Response:
[
    {
        "created_at": "14/01/2022",
        "driver": {
            "created_at": "14/01/2022",
            "first_name": "Yurii",
            "id": 5,
            "last_name": "Fokin",
            "updated_at": null
        },
        "driver_id": 5,
        "id": 1,
        "make": "Kia",
        "model": "Sportage",
        "plate_number": "LL 1234 PP",
        "updated_at": "14/01/2022"
    }
]
```
+ GET /vehicles/vehicle/?with_drivers=no - вывод списка машин без водителей
```
Response:
[
    {
        "created_at": "14/01/2022",
        "driver": null,
        "driver_id": null,
        "id": 2,
        "make": "Kia",
        "model": "Rio",
        "plate_number": "АА 7845 ОО",
        "updated_at": "14/01/2022"
    }
]
```
+ GET /vehicles/vehicle/<vehicle_id> - получение информации по определенной машине
```
Response:
{
    "created_at": "14/01/2022",
    "driver": null,
    "driver_id": null,
    "id": 2,
    "make": "Kia",
    "model": "Rio",
    "plate_number": "АА 7845 ОО",
    "updated_at": "14/01/2022"
}
```
+ POST /vehicles/vehicle/ - создание новой машины
```
Request:
{
    "make": "BMW",
    "model": "X5",
    "plate_number": "BB 5555 FF"
}
```

```
Response:
{
    "message": "New vehicle added successfully."
}
```
+ PUT /vehicles/vehicle/<vehicle_id>/ - редактирование машины
```
Request:
{
"plate_number": "BB 5655 FF"
}
```

```
Response:
{
    "created_at": "16/01/2022",
    "driver": null,
    "driver_id": null,
    "id": 8,
    "make": "BMW",
    "model": "X5",
    "plate_number": "BB 5655 FF",
    "updated_at": "16/01/2022"
}
```
+ POST /vehicles/set_driver/<vehicle_id>/?set_driver=yes - сажаем водителя в машину
```
Response:
{
    "message": "Driver added successfully."
}
```
+ POST /vehicles/set_driver/<vehicle_id>/?set_driver=no - высаживаем водителя из машины
```
Response:
{
    "message": "Driver deleted successfully."
}
```
+ DELETE /vehicles/vehicle/<vehicle_id>/ - удаление машины
```
Response:
{
    "message": "Vehicle deleted successfully"
}
```