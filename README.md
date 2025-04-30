# Django Project

Django 5.1 Project
==================

This project is a Django 5.1 application configured with Poetry for dependency management and Docker Compose for containerized development. This README provides instructions on how to set up and work with the project.

Prerequisites
-------------

*   [Docker](https://docs.docker.com/get-docker/) and [Docker Compose](https://docs.docker.com/compose/install/) installed on your machine.
*   [Poetry](https://python-poetry.org/docs/#installation) for dependency management.

Setup
-----

### 1\. Clone the Repository

    git clone https://github.com/your-username/your-repository.git
    cd your-repository
        

### 2\. Build and Start Containers

Use Docker Compose to build and start the application containers:

    docker-compose up --build
        

This command will start the application and the database containers. By default, it will start the `web` service where Django runs and the `db` service for the PostgreSQL database.

### 3\. Install Dependencies

To install project dependencies, use Poetry:

    make install
        

### 4\. Migrate the Database

Run the initial migrations to set up the database schema:

    make migrate
        

### 5\. Create a Superuser

To create an admin user, run:

    make create-user
        

### 6\. Run the Development Server

Start the Django development server:

    make run
        

You can access the application at [http://localhost:8000/](http://localhost:8000/).

Makefile Commands
-----------------

Here are the available `Makefile` commands:

*   `install`: Install all dependencies using Poetry.
*   `poetry-shell`: Activate the Poetry shell.
*   `lint`: Run code linting using Flake8 and Pylint.
*   `format`: Format code using `isort` and `black`.
*   `startapp appname=users`: Create a new Django app. Replace `users` with your app name.
*   `migrate`: Apply database migrations.
*   `makemigrations`: Create new database migrations.
*   `run`: Run the Django development server.
*   `test`: Run tests using pytest.
*   `create-user`: Create a superuser for the Django admin.
*   `enter-docker`: Enter the Docker container's shell.

### Example Makefile Commands

    make install           # Install dependencies
    make migrate           # Apply database migrations
    make makemigrations    # Create new database migrations
    make run               # Start the Django development server
    make test              # Run tests
    make create-user       # Create a superuser
        

Docker Compose Commands
-----------------------

Here are some useful Docker Compose commands:

*   `docker-compose up --build`: Build and start the containers.
*   `docker-compose down`: Stop and remove the containers.
*   `docker-compose exec web /bin/bash`: Enter the `web` container's shell.

Accessing the Application
-------------------------

Once the containers are up and running, you can access the application at [http://localhost:8000/](http://localhost:8000/).

Troubleshooting
---------------

*   **If you encounter issues with database migrations**, ensure that the database service is running and accessible.
*   **For issues related to Docker containers**, check the container logs using `docker-compose logs`.
