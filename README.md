# CMS-SERVER-USERS

## Project Description 📝

The CMS Server Users is a Flask-based microservices server application designed to manage users and comments within a Content Management System (CMS). It provides a robust and efficient backend for user and comment-related functionalities.

## Prerequisites 🛠️

- **Python 3.11:** Ensure you have Python 3.11 or a compatible version installed on your system.

- **Python Libraries:** Install the required Python libraries using the provided `Pipfile.lock` file.
In addition, as part of a more readable form, dependencies along with versions are attached in a `Pipfile` file.


## Environment Variables ⚙️

1. Create a `.env` file in the project root directory.

2. Set the following environment variables in the `.env` file:

   ```plaintext
    DATABASE_URI=
   
    MAIL_USERNAME=
    MAIL_PASSWORD=
    MAIL_SERVER=
    MAIL_PORT=
    MAIL_USE_SSL=
    MAIL_USE_TLS=
    
    REGISTER_TOKEN_LIFESPAN=
    
    JWT_COOKIE_SECURE=
    JWT_TOKEN_LOCATION=
    JWT_SECRET_KEY=
    JWT_ACCESS_TOKEN_EXPIRES=
    JWT_REFRESH_TOKEN_EXPIRES=
    JWT_COOKIE_CSRF_PROTECT=
     
    APP_CONFIG=
   ```
    `DATABASE_URI` refers in this case to the production database. 

    `APP_CONFIG` gives you the ability to use the application under several configurations more broadly described within the `config.py` file.

## Running 🚀

1.  **Clone the repository**

    ```bash
    git clone https://github.com/WojciechKubak/CMS-SERVER-USERS
    cd CMS-SERVER-USERS
    ```

2. **Install dependencies**
    ```bash
    pip install pipenv
    pipenv install --ignore-pipfile
    pipenv shell
    ```

3. **Build docker containers**
    ```bash
    docker-compose up -d --build
    ```

4. **Apply database migrations**
    ```bash
    pipenv run alembic -n development upgrade head
    ```

5. **Access the application**

    Your application should now be accessible at http://localhost:8000. You can explore the API endpoints and use the Postman collection for testing and interacting with the application.


## Security in the application 🔒

### Authentication and Authorization

The application uses Flask-JWT-Extended for handling JSON Web Tokens (JWT) to manage user authentication. JWTs are issued upon successful login and are used to authenticate and authorize requests. The JWTs contain the user's identity and role, allowing the server to validate and control access to specific resources based on user roles.

### Password Hashing

To enhance security, user passwords are hashed using Flask-Bcrypt before being stored in the database. Bcrypt is a strong, adaptive hashing algorithm that protects user passwords from unauthorized access.

### Role-Based Access Control

The application implements role-based access control to restrict access to certain functionalities based on user roles. For example, only users with the "admin" role can perform administrative actions such as deleting users.

### JWT Token Refresh

JWT tokens have a limited lifespan. The application automatically refreshes access tokens using refresh tokens to ensure continuous access for users without requiring frequent re-authentication.

## Object-Relational Mapping (ORM) with SQLAlchemy 🗄️

### Database Configuration

The application utilizes SQLAlchemy as the Object-Relational Mapping (ORM) tool to interact with the database. SQLAlchemy simplifies database operations by allowing developers to use Python objects and methods rather than raw SQL queries. The configuration includes the definition of database models such as `UserModel` and `CommentModel`.

### Model Classes

The CMS Server Users utilizes the Active Record pattern for modeling database entities. Active Record integrates database logic directly into the model classes, making it convenient to interact with database tables. 
### ORM in Flask-RESTful

Flask-RESTful, combined with SQLAlchemy, simplifies the development of RESTful APIs. Resources such as `CommentResource` and `UserListResource` utilize ORM principles to interact with the database when handling HTTP requests.

## How to use 🔄

To interact with the server, you can use the following API endpoints:

- **GET /users/{id}**: Get user details by ID.
- **GET /users/{username}**: Get user details by username.
- **GET /users**: Get a list of all users.
- **POST /users/register**: Register a new user.
- **POST /users/activate**: Activate a user.
- **PUT /users/{id}**: Update user details by ID.
- **DELETE /users/{id}**: Delete a user by ID.

- **GET /comments/{id}**: Get comment details by ID.
- **GET /comments**: Get a list of all comments.
- **POST /comments**: Add a new comment.
- **PUT /comments/{id}**: Update comment content by ID.
- **DELETE /comments/{id}**: Delete a comment by ID.
- **GET /comments/user/{id}**: Get comments by user ID.
- **GET /comments/article/{id}**: Get comments by article ID.

## To-Do List 📋

### Refactoring Email Configuration
- Reimplement the `EmailConfig` class to follow Flask conventions, initializing it based on the Flask application object (`app`).

### Extended Routing for Administrators
- Expand the application's routing to include additional functionalities accessible only to administrators.

### User Authentication Decorator
- Develop a decorator to streamline the process of authenticating users and assigning roles.
- Replace manual role assignment with the new decorator to simplify code and enhance maintainability.

### Proxy Pattern Implementation
- Implement a proxy design pattern for the service layer, allowing the server to act as a proxy for other services.
- Configure the proxy to provide users with different sets of information based on their authorization levels.

## Testing 🧪

### Pytest Framework
The CMS Server Users application employs the Pytest framework for automated testing. Pytest provides a simple and effective way to write and execute tests, ensuring the robustness of the codebase.

#### Running Tests
To run the tests, follow these steps:

1. Switch the application to testing mode by setting the `APP_CONFIG` environment variable to `'testing'` in the `.env` file.

    ```env
    APP_CONFIG=testing
    ```

2. Install the necessary testing dependencies:

    ```bash
    pipenv install --dev
    ```

3. Execute the tests using Pytest:

    ```bash
    pipenv run pytest
    ```

### Test Coverage Report 📊
The application generates a coverage report in HTML format, providing insights into the percentage of code covered by tests. This report aids in identifying areas that require additional testing and ensures comprehensive test coverage.

#### Generating Coverage Report
To generate and view the coverage report, use the following commands:

```bash
pipenv run coverage html -d coverage_html 
```

This command will produce an HTML coverage report in the `coverage_html` directory. Open the generated `index.html` file in a web browser to view the detailed coverage information.
