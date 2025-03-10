# Node.js Backend API with MySQL

This backend API is developed using Node.js, Express, MySQL, and Docker to manage and serve user data efficiently. It includes a structured database schema with relational tables, secure practices against SQL injection, and environment-based configuration for sensitive information.

## 🚀 Project Setup

### Prerequisites
- Node.js (LTS version recommended)
- Docker and Docker Compose

### 🐳 Docker Setup (MySQL Database)

Start the MySQL container:

```bash
docker-compose up -d
```


### ⚙️ Environment Variables

Create a `.env` file with the following details:

```dotenv
PORT=3000
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=password
DB_NAME=avivodb
```

---

### 📦 Install Dependencies

Run the following commands:

```bash
npm install express mysql2 dotenv cors
```

Add scripts to your `package.json`:

```json
"scripts": {
  "start": "node src/index.js",
}
```

---

## 📂 Project Structure

```
backend
├── src
│   ├── config
│   │   └── db.js
│   ├── controllers
│   │   └── userController.js
│   ├── routes
│   │   └── userRoutes.js
│   └── index.js
├── db_data (created automatically by Docker)
├── docker-compose.yml
├── .env
└── package.json
```

---



## 🎯 API Endpoint

| Method | Endpoint | Description           |
|--------|----------|-----------------------|
| GET    | `/users` | Retrieve all users from database

**Example Request:**

```
GET http://localhost:3000/users
```

## 🐍 Python Migration Script 

Use this script to create your tables and relationships:



Run the migration script using:

```bash
python migrationScript.py
```


## 📚 API Usage

Start the backend service:

```bash
npm run dev
```

Access the API via:

```bash
GET http://localhost:3000/users
```



#   a v i v o a i b a c k e n d 
 
 
