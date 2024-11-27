# Assets Allocation FastAPI Application

This document provides instructions for setting up and running the backend component of the Assets Allocation application.

## Setup

Install dependencies using `pip`:

```bash
pip install -r requirements.txt
```

If you want to run tests install additional packages:

```bash
pip install -r requirements_dev.txt
```

Populate the `.env` file with the appropriate values:

```bash
DATABASE_PATH="db/aaa.db" # Path to db file
DATABASE_SCHEMA_DIR="db/sql/" # Dir for schema files
DATABASE_IMPORT_DATA_DIR="db/data/" # Dir for import data, sample files located here
```

Then run `create_db.py` file for creating db and importing data.

## Running the Application

To run the application using `uvicorn`, execute the following command:

```bash
uvicorn app:fastapi_app
```

## API documentation

Swagger interface can be found on http://127.0.0.1:8000/docs

## Testing

Test environment variables located at `.env.test` file. Usually you don't need to change them.

Run tests by command:
```bash
ENVIRONMENT=test pytest tests/
```
