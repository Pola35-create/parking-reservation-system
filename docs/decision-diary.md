# Decision Diary

| # | Decision point | Chosen one | Why | Alternative(s) |
|---|---|---|---|---|
| 1 | Backend framework | FastAPI | Simple, modern, good API documentation, Swagger UI | Flask, Django |
| 2 | Database | SQLite | Lightweight and persistent, best for small projects | PostgreSQL, MySQL |
| 3 | ORM | SQLAlchemy | Good integration with FastAPI | SQLModel, raw SQL |
| 4 | Testing framework | Pytest | Simple and widely used | unittest |

## Reflection
During the development of the project, I faced several obstacles, mainly related to understanding how the different components of the backend should work together and setting up a proper testing environment. I overcame these issues by researching the technologies, testing out different approaches until I found the one that satisfied the most of my conditions, and gradually improving the implementation based on the errors I encountered. The biggest challenge was ensuring that the application was not only functional but also properly structured and testable. Setting up the database, API endpoints, and testing environment so that they worked together correctly required the most time and debugging and at the end to make sure it runs with one single command. Although it took me more than 4 hours altogether to complete this project, but the process helped me better understand the importance of separating responsibilities and designing the application in a maintainable way.