# money_exchange

## Setup

in route of project create .env file and add these environment variables for database setting:
```
db_name=<Database Name>
db_user=<Database User>
db_pass=<Database Password>
db_host=<Database Host>
db_port=<Database Port>
```

## Using Docker
To start server you can simply run:

`docker-compose up`

Ro run django management commands you can run this command:

`docker-compose run --rm app python manage.py help`