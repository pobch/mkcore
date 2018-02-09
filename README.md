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
