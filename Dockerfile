FROM node:current-alpine AS frontend-builder
WORKDIR /code
COPY ./frontend /code
COPY ./frontend/.env.loca[l] /code/.env

RUN npm ci
RUN npm run build-only

FROM python:3.13-alpine AS work

RUN mkdir /frontend
COPY --from=frontend-builder /code/dist /frontend

COPY ./entrypoint /run.sh
RUN chmod +x /run.sh

RUN mkdir /db
RUN mkdir /logs

RUN mkdir /backend
WORKDIR /backend
COPY ./backend .

COPY <<EOF .env
DATABASE_PATH="/db/aaa.db"
DATABASE_SCHEMA_DIR="/backend/db/sql/"
DATABASE_IMPORT_DATA_DIR="/backend/db/data/"
DATABASE_IMPORT_DATA_DELIMETER="|"
EOF

RUN --mount=type=cache,target=/root/.cache/pip python -m pip install --upgrade pip
RUN --mount=type=cache,target=/root/.cache/pip pip install -r requirements.txt
RUN chmod +x create_db.sh

ENTRYPOINT [ "/run.sh" ]
