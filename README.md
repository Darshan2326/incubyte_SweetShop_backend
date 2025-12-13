# Sweet Shop API

A FastAPI-based backend for a sweet shop management system with user authentication and inventory management.


### AI Usage Policy (Important) ###
`I use AI for finding the solution and understadning the logc as well finding the shortest and efected way to implimentation and for debuging`
`i can proudly say that i use 20% AI , 10% of browser and 70% is my master logic.`
`All business logic, validations, database operations, and testing were implemented and refined by me. AI was used as a productivity tool, not as a replacement for understanding.`



## Project Structure

```
.
├── app/                 # Main application code
│   ├── __init__.py
│   ├── auth/           # Authentication dependencies
│   │   ├── __init__.py
│   │   └── dependencies.py
│   ├── sweets/         # Sweets management functionality
│   │   ├── __init__.py
│   │   ├── model.py
│   │   └── routes.py
│   ├── user/           # User management functionality
│   │   ├── __init__.py
│   │   ├── models.py
│   │   ├── routes.py
│   │   └── utils.py
│   └── database.py     # Database connection and collections
├── tests/              # Test files (pytest)
│   ├── __init__.py
│   ├── test_auth/      # Authentication tests
│   │   ├── __init__.py
│   │   └── test_dependencies.py
│   ├── test_sweets_TDD/ # Sweets functionality tests
│   │   ├── __init__.py
│   │   ├── test_inventory.py
│   │   ├── test_model.py
│   │   └── test_routes.py
│   ├── test_auth_TDD.py
├── main.py             # Application entry point
└── README.md           # This file
```

## Features

- User registration and authentication with JWT tokens
- Sweet product management (create, read, search, update)
- MongoDB integration for data persistence
- RESTful API design
- Comprehensive test suite using pytest

## API Endpoints

### Authentication

- `POST /api/auth/register` - Register a new user
- `POST /api/auth/login` - Login as an existing user

### Sweets Management

- `POST /api/sweets/addSweets` - Add a new sweet product
- `GET /api/sweets` - Get all sweet products
- `GET /api/sweets/search` - Search sweets by name, category, or price range [http://127.0.0.1:8000/api/sweets/search?category=Cakes&low_price=12]
- `PUT /update/{sweetID}` - Update a sweet product by ID [http://127.0.0.1:8000/update/5769e7df-8f5a-4ed9-b1f5-6c127b6a2ee1]

### Sweets inventory
- `POST /api/sweets/{SweetID}/purchese?quantity=2` - Purchase the sweet by giving the quanity [http://127.0.0.1:8000/api/sweets/a0e808df-970b-4658-a2fd-c16a9a647799/purchese?quantity=2]
- `POST /api/sweets/{SweetID}/restock?restoreQuantity=1` - restock the sweet by giving the quanity [http://127.0.0.1:8000/api/sweets/a0e808df-970b-4658-a2fd-c16a9a647799/restock?restoreQuantity=1]

## Setup and Installation

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set up environment variables (if any)
4. Run the application:
   ```bash
   uvicorn main:app --reload
   ```

## Running Tests

Tests are written using pytest. To run the tests:

```bash
pytest
```

## Database

This project uses MongoDB Atlas for data persistence. The connection is configured in `app/database.py`.

## Authentication

All sweets management endpoints require authentication. Include the JWT token in the Authorization header:

```
Authorization: Bearer <your-token-here>
```

Tokens are obtained through the registration or login endpoints.