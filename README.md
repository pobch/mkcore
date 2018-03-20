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

## Running migration
```
    make migrate
```

## Admin page
`http://127.0.0.1:8000/admin/`

## Room API
Go to `http://127.0.0.1:8000/rooms/` (Don't forget `/` at the end)
- Use `GET` to list all rows in the database.
- Use `POST` to create a new row.

Go to `http://127.0.0.1:8000/rooms/<pk>/` to get/change/delete each row by pk (the 'id' column)
- Use `GET`, `PUT`, `DELETE`

## Account API
- `http://127.0.0.1:8000/accounts/`
- `http://127.0.0.1:8000/accounts/<pk>/`



# Docker

## Development
```
make dev
```

## Finding host IP in docker network
```
docker run -it python:3.6-alpine /bin/sh -c "/sbin/ip route|awk '/default/ { print \$3 }'"
```
