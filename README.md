# Setup and Run Instructions for Scraping Candidates

### 1. Create a Virtual Environment

To begin, create a virtual environment to manage your project's dependencies:

```bash
    python -m venv venv
```

###  2. Activate the Virtual Environment

Activate the virtual environment with the following command:

### 

```bash
    source venv/bin/activate  # On Linux or macOS
    # On Windows, use: venv\Scripts\activate
```

### 3. Install Required Python Packages

Install all necessary Python dependencies by running:

```bash
    pip install -r requirements.txt
```

### 4. Set Up Postgres Database

Set up a Postgres database according to your environment’s instructions.

### 5. Configure Environment Variables
Create a .env file in the root of the project and include the following variable:

```
DATABASE_URL=<your_database_url>
RSS_URL=<your_rss_url>
```

### 6. Run Database Migrations

After configuring the database, run the alembic migrations to update the schema:


```bash
    alembic upgrade head
```

### 7. Scrape Vacancy Data

To scrape the vacancy data, run the following script:

```bass
    python -m scripts.parse
```

### 8. Run the Application

Finally, start the FastAPI application using Uvicorn:
```bash
    uvicorn main:app --reload
```

### 9. Access Swagger API Documentation
Once the server is running, you can access the auto-generated API documentation through Swagger by navigating to:

```
    http://127.0.0.1:8000/docs
```