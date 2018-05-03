# Makrub Application

## STATUS:
Developing

## Prerequisites
- make
- pipenv
- postgresql
- redis

```
    pipenv shell
    pipenv install
```

## Setting up database in local environment
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

## Base url
`http://127.0.0.1:8000/`

## API end points
1. `api/auth/login/` use e-mail and password to receive jwt token
2. `api/auth/login/refresh/` refresh jwt token when it is nearly expired
3. `api/auth/login/verify/` send jwt token to verify
4. `api/auth/register/`
5. `api/users/` all users list
6. `api/users/<int:pk>/` an user detail
7. `api/users/profiles/` addition users' detail
8. `api/users/profiles/<int:pk>/`
9. `api/rooms/` all rooms list
10. `api/rooms/<int:pk>/` each room detail
11. `api/rooms/join/` a guest user's action to join the room by room_code and room_password
12. `api/rooms/unjoin/` a guest user's action to leave the room
13. `api/answers/` all answers list
14. `api/answers/<int:pk>/`

# Docker

## Development
```
make dev
```

## Finding host IP in docker network
```
docker run -it python:3.6-alpine /bin/sh -c "/sbin/ip route|awk '/default/ { print \$3 }'"
```
