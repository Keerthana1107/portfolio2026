POCKETSMART AI – PROJECT DEVELOPMENT

1. Introduction

The Project Development phase describes the actual implementation of PocketSmart AI.

PocketSmart AI is developed as a web-based application using FastAPI for the backend, Jinja2 templates for the frontend, SQLite for data storage, and Google Gemini for AI-based recommendations.

2. Project Structure

The application is organized into different components:

• Backend
• Frontend
• Database
• AI Recommendation Service
• Authentication
• Static Resources
• Tests
• Configuration Files

3. Backend Development

The backend is developed using Python and FastAPI.

The backend manages:

• Application startup
• Web routes
• Authentication
• User sessions
• Planner requests
• Database operations
• AI recommendations
• Image uploads

The main application entry point is:

main.py

4. Application Routes

The application contains separate route modules for different functions.

The main route modules include:

• pages.py
• auth.py
• planners.py
• session.py

These routes handle page rendering, authentication, planner requests, and session-related operations.

5. Authentication Development

The authentication system provides:

• User registration
• User login
• Password verification
• Password hashing
• Session creation
• Session validation
• User logout

Authentication protects application pages that require a logged-in user.

6. Database Development

SQLite is used as the database for the application.

The database service manages:

• Database initialization
• User records
• Recommendation records
• Recommendation history

The database functionality is implemented through the database service module.

7. Frontend Development

The frontend is developed using:

• HTML
• CSS
• JavaScript
• Jinja2 templates

The main frontend pages include:

• Home Page
• Login Page
• Registration Page
• Dashboard
• Home Budget Planner
• Party Budget Planner
• Jewelry Budget Planner
• History Page

8. Home Interior Planner Development

The Home Interior Planner accepts information such as:

• Budget
• Room types
• Item quantities
• Additional requirements

The submitted information is processed by the backend and passed to the recommendation service.

9. Party Planner Development

The Party Planner accepts:

• Budget
• Number of guests
• Event type
• Venue type
• Requirements
• Additional information

The backend processes the submitted information and generates recommendations.

10. Jewelry Planner Development

The Jewelry Planner accepts:

• Budget
• Occasion
• Style preference
• Optional outfit image

The uploaded image is handled by the backend when provided.

The planner sends the user's requirements to the recommendation service.

11. AI Recommendation Development

The application integrates Google Gemini for AI-based recommendations.

The recommendation service prepares the user's requirements and sends them to the configured AI service.

The returned response is processed and displayed to the user.

The AI recommendation functionality is implemented through the recommendation service.

12. Fallback Recommendation Development

A fallback mechanism is included to maintain application functionality when the AI service is unavailable or returns an unusable response.

The fallback system provides predefined recommendations based on the planner information.

13. Recommendation History Development

Generated recommendations are stored in the database for logged-in users.

The History page allows users to view their previous recommendations.

This provides users with access to their earlier planning results.

14. Image Upload Development

The Jewelry Planner supports optional outfit image uploads.

The backend validates and processes the uploaded file before using it as additional information for the recommendation process.

15. Static Files Development

Static resources are used for the application interface.

These include:

• CSS files
• JavaScript files
• Images
• Icons

The static resources are served by the FastAPI application.

16. Template Development

Jinja2 templates are used to create the web pages.

The templates include common layout components such as:

• Navigation
• Footer
• Page content
• Forms
• Dashboard components

This helps maintain a consistent interface throughout the application.

17. Configuration

The application uses environment variables for configuration.

The environment configuration can include:

• Gemini API key
• Database configuration
• Application settings
• Secret values

Sensitive information should not be committed directly to the repository.

18. Dependencies

The main dependencies include:

• FastAPI
• Uvicorn
• Jinja2
• python-multipart
• python-dotenv
• itsdangerous
• Google Generative AI
• httpx
• pytest

The dependencies are listed in:

requirements.txt

19. Testing Development

Testing files are included to verify application functionality.

Testing covers areas such as:

• Application startup
• Page responses
• Authentication
• Planner functionality
• Database operations
• Recommendation functionality

20. Development Result

The development phase produces a complete web-based PocketSmart AI application.

The developed system connects the frontend, backend, database, authentication system, planner modules, and AI recommendation service.

21. Conclusion

The Project Development phase converts the planned design and requirements into an actual working application.

PocketSmart AI provides users with a web interface for budget planning, personalized recommendations, and recommendation history while integrating Artificial Intelligence into the planning process.
