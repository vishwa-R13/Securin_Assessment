# Securin_Assessment

# Recipe Search API

Simple Recipe Search API built using FastAPI and MongoDB.

---

# Installation

## Clone the Repository

```bash
git clone https://github.com/your-username/recipe-api.git
cd recipe-api
```

---

# Install Dependencies

```bash
pip install fastapi uvicorn pymongo python-dotenv
```

---

# Configure MongoDB

Create a `.env` file:

```env
MONGO_URI=your_mongodb_connection_string
```

---

# Upload Recipe Dataset

Place your JSON dataset file inside the project folder.

Run:

```bash
python upload_data.py
```

This uploads all recipe data into MongoDB.

---

# Run the API

```bash
uvicorn api:app --reload
```

Server runs at:

```bash
http://127.0.0.1:8000
```

---

# API Documentation

Open in browser:

```bash
http://127.0.0.1:8000/docs
```

---

# API Endpoints

## Get Recipes

```http
GET /api/recipes
```

Example:

```http
/api/recipes?page=1&limit=10
```

---

## Search Recipes

```http
GET /api/recipes/search
```

Examples:

```http
/api/recipes/search?title=chicken
```

```http
/api/recipes/search?rating=>=4.5
```

```http
/api/recipes/search?calories=<300
```

```http
/api/recipes/search?cuisine=Italian
```

---

# Author

Vishwa R
