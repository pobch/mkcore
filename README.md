# Makrub Application

## Prerequisites
- make
- pipenv
- postgresql
- redis

```
    pipenv shell
    pipenv install
```

## Setting up database
```
    createdb makrub
    createuser makrub
    psql makrub
    alter user makrub with encrypted password 'localpass';
    grant all privileges on database makrub to makrub ;
```

## Running development server
```
    make dev
```

## Running migration
```
    make migrate
```

## Room API
Go to `http://127.0.0.1:8000/api/` (Don't forget / at the end)
- Use `GET` to list all rows in the database.
- Use `POST` to create a new row.

Go to `http://127.0.0.1:8000/api/<pk>/` to get/change/delete each row by pk (the 'id' column)
- Use `GET`, `PUT`, `DELETE`

## JSON format:
```
{
    "id": <int,pk,auto-add>,
    "name": <string,maxlength=200>,
    "description": <text>,
    "user_id": <int>,
    "account_id": <int>,
    "documents": <text>
}
```
