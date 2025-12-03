# Flask E-commerce API

A production-ready RESTful API for an e-commerce platform built with Flask. This API provides endpoints for user authentication, product management, and order processing.

## Features

- **User Authentication**: Register, login, and profile management with JWT tokens
- **Product Management**: CRUD operations for products with search and filtering
- **Order Management**: Create, view, update, and cancel orders
- **Stock Management**: Automatic inventory tracking
- **Input Validation**: Comprehensive validation for all endpoints
- **Error Handling**: Proper error responses with meaningful messages
- **Database**: SQLAlchemy ORM with SQLite (easily switchable to PostgreSQL/MySQL)

## Technology Stack

- **Flask**: Web framework
- **Flask-SQLAlchemy**: ORM for database operations
- **Flask-JWT-Extended**: JWT authentication
- **Flask-Bcrypt**: Password hashing
- **Flask-CORS**: Cross-Origin Resource Sharing support
- **SQLite**: Database (development)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/irissphere/flask-ecommerce-api.git
cd flask-ecommerce-api
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create environment file:
```bash
cp .env.example .env
# Edit .env with your configuration
```

5. Run the application:
```bash
python run.py
```

The API will be available at `http://localhost:5000`

## API Endpoints

### Authentication

#### Register User
```http
POST /api/auth/register
Content-Type: application/json

{
  "email": "user@example.com",
  "username": "username",
  "password": "securepassword"
}
```

#### Login
```http
POST /api/auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "securepassword"
}
```

#### Get Profile (Authenticated)
```http
GET /api/auth/profile
Authorization: Bearer <access_token>
```

#### Update Profile (Authenticated)
```http
PUT /api/auth/profile
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "username": "newusername",
  "password": "newpassword"
}
```

### Products

#### Get All Products
```http
GET /api/products
GET /api/products?category=electronics
GET /api/products?min_price=10&max_price=100
GET /api/products?search=laptop
```

#### Get Product by ID
```http
GET /api/products/<product_id>
```

#### Create Product (Authenticated)
```http
POST /api/products
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "name": "Product Name",
  "description": "Product description",
  "price": 99.99,
  "stock": 100,
  "category": "electronics",
  "image_url": "https://example.com/image.jpg"
}
```

#### Update Product (Authenticated)
```http
PUT /api/products/<product_id>
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "name": "Updated Product Name",
  "price": 89.99,
  "stock": 150
}
```

#### Delete Product (Authenticated)
```http
DELETE /api/products/<product_id>
Authorization: Bearer <access_token>
```

### Orders

#### Get All Orders (Authenticated)
```http
GET /api/orders
Authorization: Bearer <access_token>
```

#### Get Order by ID (Authenticated)
```http
GET /api/orders/<order_id>
Authorization: Bearer <access_token>
```

#### Create Order (Authenticated)
```http
POST /api/orders
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "items": [
    {
      "product_id": 1,
      "quantity": 2
    },
    {
      "product_id": 2,
      "quantity": 1
    }
  ]
}
```

#### Update Order Status (Authenticated)
```http
PUT /api/orders/<order_id>
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "status": "processing"
}
```

Valid statuses: `pending`, `processing`, `shipped`, `delivered`, `cancelled`

#### Cancel Order (Authenticated)
```http
DELETE /api/orders/<order_id>
Authorization: Bearer <access_token>
```

## Database Models

### User
- `id`: Integer (Primary Key)
- `email`: String (Unique)
- `username`: String (Unique)
- `password_hash`: String
- `created_at`: DateTime

### Product
- `id`: Integer (Primary Key)
- `name`: String
- `description`: Text
- `price`: Float
- `stock`: Integer
- `category`: String
- `image_url`: String
- `created_at`: DateTime
- `updated_at`: DateTime

### Order
- `id`: Integer (Primary Key)
- `user_id`: Integer (Foreign Key)
- `status`: String
- `total`: Float
- `created_at`: DateTime
- `updated_at`: DateTime

### OrderItem
- `id`: Integer (Primary Key)
- `order_id`: Integer (Foreign Key)
- `product_id`: Integer (Foreign Key)
- `quantity`: Integer
- `price`: Float

## Configuration

The application can be configured using environment variables in the `.env` file:

- `FLASK_ENV`: Environment mode (development/production/testing)
- `SECRET_KEY`: Flask secret key
- `JWT_SECRET_KEY`: JWT secret key
- `DATABASE_URL`: Database connection URL

## Error Handling

The API returns appropriate HTTP status codes:

- `200 OK`: Successful GET, PUT requests
- `201 Created`: Successful POST requests
- `400 Bad Request`: Invalid input data
- `401 Unauthorized`: Invalid credentials
- `403 Forbidden`: Insufficient permissions
- `404 Not Found`: Resource not found
- `500 Internal Server Error`: Server errors

Error responses follow this format:
```json
{
  "error": "Error message description"
}
```

## Security Features

- Password hashing with bcrypt
- JWT token-based authentication
- CORS support for cross-origin requests
- Input validation for all endpoints
- SQL injection prevention through ORM

## Development

To run in development mode:
```bash
export FLASK_ENV=development  # On Windows: set FLASK_ENV=development
python run.py
```

## Production Deployment

For production deployment:

1. Set environment variables:
```bash
export FLASK_ENV=production
export SECRET_KEY=<strong-secret-key>
export JWT_SECRET_KEY=<strong-jwt-secret>
export DATABASE_URL=<production-database-url>
```

2. Use a production WSGI server (e.g., Gunicorn):
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 run:app
```

3. Consider using:
   - Nginx as a reverse proxy
   - PostgreSQL or MySQL for the database
   - Redis for caching
   - Docker for containerization

## License

This project is open source and available under the MIT License.