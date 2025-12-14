# Sweet Shop API

A FastAPI-based backend for a sweet shop management system with user authentication and inventory management.


### what i leanr
- i knwo python fast API but in this assesment i learn to manageing well authantication and seurity



### AI Usage Policy (Important)

in backend i use pyhon fastAPI and i have enough experience in python to create API so for backend i used my own logic for authanticate i use ChatGPT AI and for run time error i use qoder AI, the list of open sorce usege are below

- used chatGPT for find batter way of API and masive logic
- for solve the run time error i use qoder and copilot


- **AI Co-authorship** :- ChatGPT , qoder , copilot.


### what i learn 
- i realy enjoy this assesment and i learn about the react now atleast i am capable to create basic react project.
- i learn Vercel and Render deployement with Github and gain my CICD skill.
- i learn the new errors that i didn't heread yet during the deployement.
- i realise my abiloty and productivity by this assesment
- backend is live in render website where i can perform CICD "https://incubyte-sweetshop-backend.onrender.com/"




### AI Usage Policy (Important) ###
`I use AI for finding the solution and understadning the logc as well finding the shortest and efected way to implimentation and for debuging`
`i can proudly say that i use 20% AI , 10% of browser and 70% is my master logic.`
`All business logic, validations, database operations, and testing were implemented and refined by me. AI was used as a productivity tool, not as a replacement for understanding.`


## API Integration

The frontend communicates with a backend API hosted at `https://incubyte-sweetshop-backend.onrender.com` for all data operations including:
- User authentication
- Sweet inventory management
- Purchase operations
- Search functionality


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
- `GET /api/sweets/search` - Search sweets by name, category, or price range 
   [https://incubyte-sweetshop-backend.onrender.com/api/sweets/search?category=Cakes&low_price=12]
- `PUT /update/{sweetID}` - Update a sweet product by ID 
   [https://incubyte-sweetshop-backend.onrender.com/update/5769e7df-8f5a-4ed9-b1f5-6c127b6a2ee1]

### Sweets inventory
- `POST /api/sweets/{SweetID}/purchese?quantity=2` - Purchase the sweet by giving the quanity  
   [https://incubyte-sweetshop-backend.onrender.com/api/sweets/a0e808df-970b-4658-a2fd-c16a9a647799/purchese?quantity=2]
- `POST /api/sweets/{SweetID}/restock?restoreQuantity=1` - restock the sweet by giving the quanity 
   [https://incubyte-sweetshop-backend.onrender.com/api/sweets/a0e808df-970b-4658-a2fd-c16a9a647799/restock?restoreQuantity=1]

## Setup and Installation

1. Clone the repository
   git clone https://github.com/Darshan2326/incubyte_SweetShop_backend.git


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