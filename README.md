# Overview

In this project, I have created FastAPI aplication with PostgreSQL integration using SQLModel

---

# Installation and Startup

1. **Clone the repository:**
    
    ```bash
       git clone https://github.com/RomanRavlyk/HotelComplex.git
    ```   

2. **Install Python and dependencies:**
    
    Download Python 3.12.X (or a compatible version)

   Navigate to the project directory:
    
    ```bash
      cd app
    ```
    
    Install the required packages:
    
    ```bash
       pip install -r requirements.txt
    ```

3. **Configure the environment:**  
    Create a .env file in the project root and add your database connection information:  
    `DATABASE_URL=postgresql://username:password@localhost:5432/db_name`  

4. **Run the project**  
    ```bash
       uvicorn main:app --reload
    ```
5. **Access API documentation:**  
Open your browser and go to:
  Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)  
  ReDoc: [http://localhost:8000/redoc](http://localhost:8000/redoc) (optional)
