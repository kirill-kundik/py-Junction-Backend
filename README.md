# Junction Server Part Development

### Needed environment:

*  [python3.7+](https://www.python.org/downloads/)
*  [postgres9.6+](https://www.postgresql.org/download/)
*  *or* [Docker](https://www.docker.com/products/docker-desktop) with [docker-compose](https://docs.docker.com/compose/install/)

### Basic Setup:

*Non docker users*
1. Create a new virtual environment with `python -m venv venv` and activate it with `source venv/bin/activate`
2. Install app package with `pip install -e .`
3. Start postgres database server
4. Create new `.env` file (something like this schema and your parameters): 
```
POSTGRES_USER=postgres
POSTGRES_DB=junction_server
POSTGRES_PASSWORD=postgres
POSTGRES_HOST=postgres
POSTGRES_PORT=5432
POSTGRES_EXTERNAL_PORT=5432
APP_PORT=5000
APP_MODE=development
```
5. Create database with `POSTGRES_DB` name
6. Start migrations `alembic upgrade head` (sometimes you will need to run migrations just before the start)

*Docker users*
1. Create new `.env` file (something like this schema and your parameters): 
```
POSTGRES_USER=postgres
POSTGRES_DB=junction_server
POSTGRES_PASSWORD=postgres
POSTGRES_HOST=postgres
POSTGRES_PORT=5432
POSTGRES_EXTERNAL_PORT=5432
APP_PORT=5000
APP_MODE=development
```
2. Build an image with `docker-compose build`
3. Start postgres container with `docker-compose up postgres`

### Start the app:

*Non docker users*
1. Start server `gunicorn -w 4 -b 0.0.0.0:$APP_PORT "main:application"`

*Docker users*
1. Start the app container `docker-compose up web`
