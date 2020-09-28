# PyTodo

A simple flask server and a command line client for todos

> This application has been created as a part of the **Learn π** lecture series going on at Institute of Technology, Nirma University.

## API Docs

1. Sign Up
    - Request:
        ```HTTP
        POST /signup HTTP/1.1
        Content-Type: application/json

        {
            "name": "John Doe",
            "password": "hell0wor1d"
        }
        ```
    - Response:
        ```HTTP
        HTTP/1.1 200 OK
        Content-Type: application/json

        {
            "202": "Success"
        }
        ```
2. Login
    - Request:
        ```HTTP
        POST /login HTTP/1.1
        Content-Type: application/json

        {
            "name": "John Doe",
            "password": "hell0wor1d"
        }
        ```
    - Response:
        ```HTTP
        HTTP/1.1 200 OK
        Content-Type: application/json

        {
            "202": "Success",
            "token": "JW6hjykcmm9i"
        }
        ```
3. User Info
    - Request:
        ```HTTP
        POST /user HTTP/1.1
        Content-Type: application/json

        {
            "token": "JW6hjykcmm9i"
        }
        ```
    - Response:
        ```HTTP
        HTTP/1.1 200 OK
        Content-Type: application/json

        {
            "202": "Success",
            "name": "John Doe"
        }
        ```
4. Logout
    - Request:
        ```HTTP
        POST /user HTTP/1.1
        Content-Type: application/json

        {
            "token": "JW6hjykcmm9i"
        }
        ```
    - Response:
        ```HTTP
        HTTP/1.1 200 OK
        Content-Type: application/json

        {
            "202": "Success"
        }
        ```
5. Creating a todo
    - Request:
        ```HTTP
        POST /new_todo HTTP/1.1
        Content-Type: application/json

        {
            "token": "JW6hjykcmm9i",
            "title": "First todo",
            "message": "hello world!"
        }
        ```
    - Response:
        ```HTTP
        HTTP/1.1 200 OK
        Content-Type: application/json

        {
            "202": "Success"
        }
        ```
6. Fetching all todos
    - Request:
        ```HTTP
        POST /view_todos HTTP/1.1
        Content-Type: application/json

        {
            "token": "JW6hjykcmm9i"
        }
        ```
    - Response:
        ```HTTP
        HTTP/1.1 200 OK
        Content-Type: application/json

        {
            "202": "Success",
            "todos": [
                {
                    "id": 1,
                    "message": "Awesome!!!!",
                    "title": "First todo"
                },
                {
                    "id": 2,
                    "message": "Alls well till now...",
                    "title": "Second todo"
                }
            ]
        }
        ```
7. Delete a todo
    - Request:
        ```HTTP
        POST /delete_todo HTTP/1.1
        Content-Type: application/json

        {
            "token": "JW6hjykcmm9i",
            "todo_id": 4
        }
        ```
    - Response:
        ```HTTP
        HTTP/1.1 200 OK
        Content-Type: application/json

        {
            "202": "Success",
            "deleted": {
                "id": 4,
                "message": "Complete API documentation",
                "title": "Fourth todo"
            }
        }
        ```
