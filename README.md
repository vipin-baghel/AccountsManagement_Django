# Finance Management App

A Django-based project for managing finance of a small-medium enterprise.

## Overview

This project provides a web application for managing projects, transactions, and generating reports. It uses Django as the web framework and Postgres as the database.

## Features

* Project management: Create, update, and delete projects.
* Transaction management: Create, update, and delete transactions (income and expenses) for each project.
* Reporting: Generate reports for each project, including income, expenses, and profit and various insights.

## Setup and Run with Docker Compose

Follow these steps to set up and run the project using Docker Compose.

### Prerequisites

- Docker

### Getting Started

1. **Clone the repository**

2. **Create and configure the `.env` file**:

    Create a `.env` file in the root of your project and add the following environment variables:

    ```dotenv
    DB_NAME=postgres
    DB_USER=postgres
    DB_PASSWORD=postgres
    DB_HOST=db_server
    DB_PORT=5432

    SECRET_KEY=your-secret-key
    DEBUG=True
    ALLOWED_HOSTS=*
    CSRF_TRUSTED_ORIGINS=https://your-domain.com

    DJANGO_SUPERUSER_USERNAME=admin
    DJANGO_SUPERUSER_EMAIL=admin@example.com
    DJANGO_SUPERUSER_PASSWORD=admin
    ```

3. **Run Docker Compose**:

    Build and start the services using Docker Compose:

    ```sh
    docker-compose up --build
    ```

4. **Access the application**:

    Once the services are up and running, you can access the Django application at `http://localhost:8000`.



## Contributing

Contributions are welcome! If you'd like to contribute to this project, please fork the repository and submit a pull request with your changes.

