# Docker Compose
## `docker-compose -f docker-compose.yml up --build --abort-on-container-exit`

# Uvicorn
## `uvicorn app.main:app --reload`

# PyBabel
1. `pybabel extract -F app/babel.cfg -o app/locales/messages.pot app .\.env`
2. `pybabel update -i app/locales/messages.pot -d app/locales`
3. `pybabel compile -d app/locales`

# Alembic
1. `alembic revision --autogenerate -m "<migration name>"`
2. `alembic upgrade head`   

# .env
- AUTH_SECRET_KEY - key for secure hashing the JWT tokens
- BOT_TOKEN - token of the bot for **webapp telegram url** support
- POSTGRES_USER - used only for docker
- POSTGRES_PASSWORD - used only for docker
- POSTGRES_HOST - used only for docker

# Database
### for local tests you can override *DATABASE_URL* & *ASYNC_DATABASE_URL* in .env with your own urls