# BurgerBlaze - API Documentation

Complete API Reference for BurgerBlaze Restaurant System.

## Base URL

- Development: `http://localhost:8000/api/`
- Production: `https://your-domain.com/api/`

## Authentication

The API uses Django REST Framework's default authentication. For operations requiring authentication, include a valid session or token.

## Menu Endpoints

### Get All Menu Items

```
GET /api/menu/
```

**Query Parameters:**
- `category` - Filter by category ID
- `search` - Search by item name

**Response:**
```json
{
  "count": 16,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "name": "Classic Cheeseburger",
      "description": "Flame-grilled beef patty with cheddar cheese...",
      "category": 1,
      "category_name": "Burgers",
      "price": "8.99",
      "image": "/media/menu-items/burger.jpg",
      "is_available": true,
      "is_vegetarian": false,
      "is_spicy": false
    }
  ]
}
```

### Get Items by Category

```
GET /api/menu/by_category/
```

**Response:**
```json
[
  {
    "category": {
      "id": 1,
      "name": "Burgers",
      "description": "Our signature flame-grilled burgers",
      "image": null
    },
    "items": [...]
  }
]
```

### Get Specials

```
GET /api/menu/specials/
```

**Response:**
```json
{
  "spicy": [...],
  "vegetarian": [...]
}
```

### Get Single Menu Item

```
GET /api/menu/{id}/
```

## Categories Endpoints

### Get All Categories

```
GET /api/categories/
```

**Response:**
```json
{
  "count": 4,
  "results": [
    {
      "id": 1,
      "name": "Burgers",
      "description": "Our signature flame-grilled burgers",
      "image": null
    }
  ]
}
```

### Get Items in Category

```
GET /api/categories/{id}/items/
```

## Orders Endpoints

### Create Order

```
POST /api/orders/
Content-Type: application/json
```

**Request Body:**
```json
{
  "customer_name": "John Doe",
  "customer_email": "john@example.com",
  "customer_phone": "555-123-4567",
  "notes": "No onions please",
  "items": [
    {
      "menu_item": 1,
      "quantity": 2,
      "special_instructions": "Extra cheese"
    },
    {
      "menu_item": 6,
      "quantity": 1,
      "special_instructions": ""
    }
  ]
}
```

**Response (201 Created):**
```json
{
  "id": 1,
  "order_number": "ORD-20240423144727",
  "customer_name": "John Doe",
  "customer_email": "john@example.com",
  "customer_phone": "555-123-4567",
  "status": "pending",
  "total_price": "28.97",
  "notes": "No onions please",
  "items": [...],
  "created_at": "2024-04-23T14:47:27Z",
  "updated_at": "2024-04-23T14:47:27Z"
}
```

### List All Orders

```
GET /api/orders/
```

### Get Orders by Phone

```
GET /api/orders/by_phone/?phone=555-123-4567
```

**Response:**
```json
[
  {
    "id": 1,
    "order_number": "ORD-20240423144727",
    ...
  }
]
```

### Get Single Order

```
GET /api/orders/{id}/
```

### Update Order Status

```
PATCH /api/orders/{id}/update_status/
Content-Type: application/json
```

**Request Body:**
```json
{
  "status": "confirmed"
}
```

**Valid Status Values:**
- `pending` - Order received, awaiting confirmation
- `confirmed` - Order confirmed and in queue
- `preparing` - Food is being prepared
- `ready` - Order ready for pickup
- `completed` - Order completed
- `cancelled` - Order was cancelled

### Update Order

```
PUT /api/orders/{id}/
PATCH /api/orders/{id}/
Content-Type: application/json
```

**Response:**
```json
{
  "id": 1,
  "order_number": "ORD-20240423144727",
  "status": "confirmed",
  ...
}
```

## Cart Endpoints

### Get or Create Cart

```
POST /api/cart/get_or_create/
Content-Type: application/json
```

**Request Body:**
```json
{
  "session_id": "session-1234567890"
}
```

**Response:**
```json
{
  "id": 1,
  "session_id": "session-1234567890",
  "items_list": [],
  "total": 0.0,
  "created_at": "2024-04-23T14:47:27Z"
}
```

### Add Item to Cart

```
POST /api/cart/{id}/add_item/
Content-Type: application/json
```

**Request Body:**
```json
{
  "menu_item_id": 1,
  "quantity": 2
}
```

**Response:**
```json
{
  "id": 1,
  "session_id": "session-1234567890",
  "items_list": [
    {
      "id": 1,
      "menu_item": {...},
      "quantity": 2,
      "subtotal": 17.98
    }
  ],
  "total": 17.98,
  "created_at": "2024-04-23T14:47:27Z"
}
```

### Remove Item from Cart

```
POST /api/cart/{id}/remove_item/
Content-Type: application/json
```

**Request Body:**
```json
{
  "cart_item_id": 1
}
```

### Clear Cart

```
POST /api/cart/{id}/clear/
```

## Error Responses

### 400 Bad Request

```json
{
  "error": "Phone number required"
}
```

### 404 Not Found

```json
{
  "detail": "Not found."
}
```

### 500 Server Error

```json
{
  "error": "Internal server error"
}
```

## Status Codes

| Code | Meaning |
|------|---------|
| 200 | OK - Request succeeded |
| 201 | Created - Resource created successfully |
| 204 | No Content - Successfully deleted |
| 400 | Bad Request - Invalid parameters |
| 404 | Not Found - Resource doesn't exist |
| 500 | Server Error - Internal server error |

## Pagination

List endpoints support pagination with page numbers by default:

```
GET /api/menu/?page=2
GET /api/orders/?page=1
```

**Response includes:**
- `count` - Total number of items
- `next` - URL to next page
- `previous` - URL to previous page
- `results` - Array of items on current page

## Filtering

### By Category

```
GET /api/menu/?category=1
```

### By Search

```
GET /api/menu/?search=burger
```

## Examples

### Create an Order and Pay

```bash
# 1. Get available items
curl http://localhost:8000/api/menu/

# 2. Create order
curl -X POST http://localhost:8000/api/orders/ \
  -H "Content-Type: application/json" \
  -d '{
    "customer_name": "Jane Smith",
    "customer_email": "jane@example.com",
    "customer_phone": "555-987-6543",
    "items": [
      {"menu_item": 1, "quantity": 1},
      {"menu_item": 6, "quantity": 1}
    ]
  }'

# 3. Track order
curl http://localhost:8000/api/orders/by_phone/?phone=555-987-6543

# 4. Update status (admin only)
curl -X PATCH http://localhost:8000/api/orders/1/update_status/ \
  -H "Content-Type: application/json" \
  -d '{"status": "preparing"}'
```

### Manage Cart

```bash
# 1. Create cart
curl -X POST http://localhost:8000/api/cart/get_or_create/ \
  -H "Content-Type: application/json" \
  -d '{"session_id": "my-session-123"}'

# 2. Add items
curl -X POST http://localhost:8000/api/cart/1/add_item/ \
  -H "Content-Type: application/json" \
  -d '{"menu_item_id": 1, "quantity": 2}'

# 3. View cart
curl http://localhost:8000/api/cart/1/

# 4. Remove item
curl -X POST http://localhost:8000/api/cart/1/remove_item/ \
  -H "Content-Type: application/json" \
  -d '{"cart_item_id": 1}'

# 5. Clear cart
curl -X POST http://localhost:8000/api/cart/1/clear/
```

## Rate Limiting

Currently not implemented. Subject to backend server limits.

## CORS

CORS is enabled for local development:
- `http://localhost:3000`
- `http://localhost:8000`
- `http://127.0.0.1:3000`
- `http://127.0.0.1:8000`

For production, configure in `settings.py`:
```python
CORS_ALLOWED_ORIGINS = [
    "https://yourdomain.com",
    "https://www.yourdomain.com",
]
```

## Security

- Always validate input on the server side
- Sanitize order notes to prevent injection attacks
- Use HTTPS in production
- Implement rate limiting for production deployments
- Add authentication for admin operations

---

**API ready for integration!** Start building with BurgerBlaze. 🚀
