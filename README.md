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

When you run the project for very first time and you don't have database yet, need to add an entry for `Service Fee` from admin page. 


## Using Docker

To start using docker you still need to pass the environment variables mentioned above. For that you can use the following in .env file:
```
db_host=db
db_name=app
db_user=postgres
db_pass=supersecretpassword
db_port=5432
```
To start server you can simply run:

`docker-compose up`

Ro run django management commands you can run this command:

`docker-compose run --rm app python manage.py help`

For very first time when you run the server, you need to add an entry for `Service Fee` from admin page