# Flask E-commerce API - Copilot Instructions

## Project Overview
This is a Flask-based RESTful API for an e-commerce platform. The API provides endpoints for managing products, orders, and user authentication.

## Technology Stack
- **Framework**: Flask (Python web framework)
- **Database**: SQLite/PostgreSQL with SQLAlchemy ORM
- **Authentication**: JWT tokens or Flask-Login
- **API Design**: RESTful principles

## Project Structure
```
flask-ecommerce-api/
├── app/
│   ├── __init__.py          # Flask app factory
│   ├── models.py            # Database models (User, Product, Order, OrderItem)
│   ├── routes/              # API endpoints
│   │   ├── auth.py          # Authentication endpoints
│   │   ├── products.py      # Product CRUD operations
│   │   └── orders.py        # Order management
│   ├── config.py            # Configuration settings
│   └── utils.py             # Helper functions
├── tests/                   # Unit and integration tests
├── requirements.txt         # Python dependencies
├── .env                     # Environment variables (not in git)
├── .gitignore              # Git ignore rules
└── run.py                  # Application entry point
```

## Coding Standards

### Python Style
- Follow PEP 8 style guide
- Use type hints where appropriate
- Maximum line length: 100 characters
- Use docstrings for functions and classes

### Database Models
- Use SQLAlchemy ORM for all database operations
- Define relationships clearly (User → Orders, Order → OrderItems, etc.)
- Include timestamps (created_at, updated_at) on all models
- Use proper constraints (foreign keys, unique constraints)

### API Endpoints
- Follow RESTful conventions:
  - GET /products - List all products
  - GET /products/{id} - Get single product
  - POST /products - Create new product
  - PUT /products/{id} - Update product
  - DELETE /products/{id} - Delete product
- Use proper HTTP status codes (200, 201, 400, 401, 404, 500)
- Return JSON responses with consistent structure
- Include error handling and validation

### Security
- Use environment variables for sensitive data (database URLs, secret keys)
- Hash passwords using werkzeug.security or bcrypt
- Implement JWT authentication for protected endpoints
- Validate and sanitize all user inputs
- Use CORS appropriately for API access

## Testing
- Write unit tests for models and utility functions
- Write integration tests for API endpoints
- Use pytest as the testing framework
- Aim for >80% code coverage
- Test both success and error cases

## Development Workflow
1. Install dependencies: `pip install -r requirements.txt`
2. Set up environment variables in `.env` file
3. Initialize database: `python run.py init-db`
4. Run development server: `python run.py`
5. Run tests: `pytest`

## Deployment Instructions

### Deploy to Render (or similar PaaS)
**New Web Service:**
1. Create a new Web Service on your hosting platform
2. Connect your GitHub repository
3. Configure build settings:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn run:app`
4. Set environment variables:
   - `FLASK_ENV=production`
   - `SECRET_KEY=<your-secret-key>`
   - `DATABASE_URL=<your-database-url>`
5. Click Deploy

### Environment Variables Required
- `FLASK_ENV`: Set to 'development' or 'production'
- `SECRET_KEY`: Secret key for session management
- `DATABASE_URL`: Database connection string
- `JWT_SECRET_KEY`: Secret key for JWT token generation (if using JWT)

## Dependencies
Key packages to include in `requirements.txt`:
- Flask
- Flask-SQLAlchemy
- Flask-Migrate
- Flask-CORS
- python-dotenv
- gunicorn (for production)
- pytest (for testing)

## Common Tasks

### Adding a New Endpoint
1. Create route function in appropriate file under `app/routes/`
2. Add route decorator with HTTP method and path
3. Implement request validation
4. Perform business logic
5. Return JSON response with appropriate status code
6. Write tests for the endpoint

### Adding a New Model
1. Define model class in `app/models.py`
2. Include all necessary fields and relationships
3. Add repr method for debugging
4. Create database migration: `flask db migrate -m "Add Model"`
5. Apply migration: `flask db upgrade`
6. Write model tests

### Error Handling
- Use Flask error handlers for common HTTP errors
- Return consistent error response format:
  ```json
  {
    "error": "Error message",
    "status": 400
  }
  ```
- Log errors appropriately for debugging

## Best Practices
- Keep route handlers thin - move business logic to separate functions
- Use blueprints to organize routes
- Implement proper logging throughout the application
- Use database transactions for operations that modify multiple records
- Implement pagination for list endpoints
- Add rate limiting for API protection
- Document API endpoints (consider Swagger/OpenAPI)

## Notes
- This is an e-commerce API, so ensure proper handling of inventory, orders, and transactions
- Consider implementing cart functionality and checkout process
- Payment integration should be planned for future iterations
- Implement proper order status management (pending, processing, shipped, delivered)
