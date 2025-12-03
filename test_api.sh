#!/bin/bash

# Test script for Flask E-commerce API
# This script tests all endpoints to ensure they work correctly

BASE_URL="http://localhost:5000/api"

echo "=========================================="
echo "Flask E-commerce API Test Script"
echo "=========================================="
echo ""

# Test 1: Register a new user
echo "1. Testing user registration..."
REGISTER_RESPONSE=$(curl -s -X POST "$BASE_URL/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "username": "testuser",
    "password": "testpassword123"
  }')
echo "Response: $REGISTER_RESPONSE"
echo ""

# Test 2: Login
echo "2. Testing user login..."
LOGIN_RESPONSE=$(curl -s -X POST "$BASE_URL/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "testpassword123"
  }')
echo "Response: $LOGIN_RESPONSE"
TOKEN=$(echo $LOGIN_RESPONSE | python3 -c "import sys, json; print(json.load(sys.stdin).get('access_token', ''))")
echo "Token: $TOKEN"
echo ""

# Test 3: Get profile
echo "3. Testing get profile..."
curl -s -X GET "$BASE_URL/auth/profile" \
  -H "Authorization: Bearer $TOKEN"
echo ""
echo ""

# Test 4: Create a product
echo "4. Testing product creation..."
PRODUCT_RESPONSE=$(curl -s -X POST "$BASE_URL/products/" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "name": "Test Laptop",
    "description": "A high-performance laptop",
    "price": 999.99,
    "stock": 10,
    "category": "electronics",
    "image_url": "https://example.com/laptop.jpg"
  }')
echo "Response: $PRODUCT_RESPONSE"
PRODUCT_ID=$(echo $PRODUCT_RESPONSE | python3 -c "import sys, json; data = json.load(sys.stdin); print(data.get('product', {}).get('id', ''))" 2>/dev/null || echo "")
echo "Product ID: $PRODUCT_ID"
echo ""

# Test 5: Get all products
echo "5. Testing get all products..."
curl -s -X GET "$BASE_URL/products/"
echo ""
echo ""

# Test 6: Get product by ID
echo "6. Testing get product by ID..."
curl -s -X GET "$BASE_URL/products/$PRODUCT_ID"
echo ""
echo ""

# Test 7: Update product
echo "7. Testing product update..."
curl -s -X PUT "$BASE_URL/products/$PRODUCT_ID" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "price": 899.99,
    "stock": 15
  }'
echo ""
echo ""

# Test 8: Create an order
echo "8. Testing order creation..."
ORDER_RESPONSE=$(curl -s -X POST "$BASE_URL/orders/" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d "{
    \"items\": [
      {
        \"product_id\": $PRODUCT_ID,
        \"quantity\": 2
      }
    ]
  }")
echo "Response: $ORDER_RESPONSE"
ORDER_ID=$(echo $ORDER_RESPONSE | python3 -c "import sys, json; data = json.load(sys.stdin); print(data.get('order', {}).get('id', ''))" 2>/dev/null || echo "")
echo "Order ID: $ORDER_ID"
echo ""

# Test 9: Get all orders
echo "9. Testing get all orders..."
curl -s -X GET "$BASE_URL/orders/" \
  -H "Authorization: Bearer $TOKEN"
echo ""
echo ""

# Test 10: Get order by ID
echo "10. Testing get order by ID..."
curl -s -X GET "$BASE_URL/orders/$ORDER_ID" \
  -H "Authorization: Bearer $TOKEN"
echo ""
echo ""

# Test 11: Update order status
echo "11. Testing update order status..."
curl -s -X PUT "$BASE_URL/orders/$ORDER_ID" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "status": "processing"
  }'
echo ""
echo ""

# Test 12: Search products
echo "12. Testing product search..."
curl -s -X GET "$BASE_URL/products/?search=laptop"
echo ""
echo ""

echo "=========================================="
echo "All tests completed!"
echo "=========================================="
