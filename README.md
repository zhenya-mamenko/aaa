# Asset Allocation Application (AAA)

A self-hosted application to simplify passive assets allocation.

![GitHub License](https://img.shields.io/github/license/zhenya-mamenko/aaa)
[![Backend tests](https://github.com/zhenya-mamenko/aaa/actions/workflows/pytest.yml/badge.svg)](https://github.com/zhenya-mamenko/aaa/actions/workflows/pytest.yml)
![Codecov](https://img.shields.io/codecov/c/github/zhenya-mamenko/aaa)
[![Frontend tests](https://github.com/zhenya-mamenko/aaa/actions/workflows/jest.yml/badge.svg)](https://github.com/zhenya-mamenko/aaa/actions/workflows/jest.yml)
[![Frontend e2e tests](https://github.com/zhenya-mamenko/aaa/actions/workflows/playwright.yml/badge.svg)](https://github.com/zhenya-mamenko/aaa/actions/workflows/playwright.yml)

## Features

* Maintain reference dictionaries for asset classes, categories, and particular assets
* Create asset allocation structures
* Monitor portfolio status
* Calculate replenishments and rebalancing

## Prerequisites

- Docker
- Alternatively: Python 3.13+ and NodeJS 22+

## Installation

1. Clone the repository
2. Create a directory to store the database

## Building and Running

You can fill the database with dictionaries' data, if you don't want to do it using app.
Data files with sample data located in `backend/db/data/` directory.

### Using Docker

Build the Docker image:

```bash
# Option 1: Use build script
./docker-build.sh

# Option 2: Manual build (specify platform as needed)
docker build --platform="linux/amd64" -t aaa .
```

Run the application:

```bash
# Option 1: Use run script (change path to the db in advance)
./docker-run.sh

# Option 2: Run Docker container manually
db_folder=. # Path on host where database will be stored
docker run -d --name aaa -p 3000:3000 -p 8000:8000 -v $db_folder:/db aaa
```

### Accessing the Application

After launching, the application will be available at: http://localhost:3000

### Network Access Configuration

To make the application accessible from other devices:

1. Before building, modify `frontend/.env`
2. Replace `127.0.0.1` with your host machine's IP address:
  ```
  VITE_AAA_API_URL=http://<host-ip>:8000/api/v1
  ```

Note: Ensure you've reviewed the platform-specific Docker build instructions at https://docs.docker.com/build/building/multi-platform/

## Additional Information

Detailed setup and manual running instructions can be found in the `frontend` and `backend` directories' README.md files.

## License

This project is licensed under the MIT License.

## Author

[Zhenya Mamenko](https://github.com/zhenya-mamenko/aaa)
