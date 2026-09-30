POCKETSMART AI – PROJECT DOCUMENTATION

1. Introduction

PocketSmart AI is a web-based AI budget planning and recommendation application. It is designed to help users plan their spending and receive personalized recommendations based on their budget and preferences.

The application focuses on three major planning areas:

• Home Interior Planning
• Party Planning
• Jewelry Selection

2. Purpose of the Application

The purpose of PocketSmart AI is to provide users with a simple platform where they can enter their budget and requirements and receive useful recommendations.

The application combines budget planning with Artificial Intelligence to provide personalized results.

3. Problem Statement

Planning purchases and activities within a fixed budget can be difficult. Users may need to consider different requirements, preferences, quantities, and costs.

PocketSmart AI addresses this problem by providing budget-based recommendations through a web-based application.

4. Objectives

The main objectives of PocketSmart AI are:

• Provide an easy-to-use budget planning system.
• Generate personalized recommendations.
• Support multiple planning categories.
• Integrate Artificial Intelligence.
• Store recommendation history.
• Provide secure user authentication.
• Provide fallback recommendations when the AI service is unavailable.

5. Scope

The application covers:

• User registration and login
• Dashboard
• Home Interior Budget Planner
• Party Budget Planner
• Jewelry Budget Planner
• AI-based recommendations
• Recommendation history
• Optional outfit image upload
• Database storage
• Web-based user interface

6. Technology Stack

Frontend:

• HTML
• CSS
• JavaScript
• Jinja2

Backend:

• Python
• FastAPI
• Uvicorn

Database:

• SQLite

Artificial Intelligence:

• Google Gemini

Testing:

• pytest

Configuration:

• python-dotenv

7. System Architecture

PocketSmart AI follows a web application architecture.

The main components are:

• User Interface
• FastAPI Backend
• Authentication
• Planner Modules
• Recommendation Service
• Google Gemini AI
• SQLite Database

The general flow is:

User
↓
Web Browser
↓
FastAPI Backend
↓
Planner
↓
Recommendation Service
↓
Google Gemini AI
↓
Recommendation Result
↓
Database
↓
User Interface

8. Application Modules

8.1 Authentication Module

The authentication module provides:

• Registration
• Login
• Password hashing
• Session management
• Logout

8.2 Home Interior Planner

The Home Interior Planner accepts budget, room, quantity, and requirement information and provides budget-based recommendations.

8.3 Party Planner

The Party Planner accepts budget, guest count, event type, venue type, and other requirements and provides party planning recommendations.

8.4 Jewelry Planner

The Jewelry Planner accepts budget, occasion, style preferences, and an optional outfit image to provide jewelry recommendations.

8.5 Recommendation Service

The recommendation service processes planner information and generates recommendations using the AI service when available.

8.6 Fallback Recommendation System

The fallback system provides predefined recommendations when the AI service is unavailable or returns an unusable response.

8.7 History Module

The History module allows logged-in users to view their previous recommendations.

9. Database

SQLite is used to store application data.

The database stores information related to:

• Users
• Recommendations
• Recommendation history

10. User Interface

The main application pages include:

• Home Page
• Login Page
• Registration Page
• Dashboard
• Home Budget Planner
• Party Budget Planner
• Jewelry Budget Planner
• History Page

The interface provides navigation and forms that allow users to enter their requirements and view recommendations.

11. Security

The application uses security mechanisms such as:

• Password hashing
• Session-based authentication
• Protected routes
• Environment variables for sensitive configuration
• Input validation

12. API

The backend is implemented using FastAPI.

The application provides API routes for:

• Pages
• Authentication
• Planners
• Sessions

FastAPI also provides interactive API documentation.

13. Testing

The application is tested to verify:

• Registration
• Login
• Logout
• Dashboard
• Planner functionality
• AI recommendations
• Fallback recommendations
• Database operations
• Recommendation history
• Image upload
• API responses
• Error handling

14. Deployment

PocketSmart AI can be run locally using the FastAPI application server.

The application includes dependency and configuration files required for setup and execution.

The application can also be prepared for deployment to a suitable hosting environment.

15. Advantages

• Simple web-based interface
• Budget-oriented recommendations
• Multiple planning categories
• AI-powered recommendations
• Fallback recommendation system
• Recommendation history
• User authentication
• Optional image upload

16. Limitations

• AI recommendations depend on the configured AI service.
• Internet connectivity may be required for AI-based recommendations.
• Recommendations depend on the accuracy of the information entered by the user.
• The application is designed around the currently supported planning categories.

17. Future Enhancements

Possible future improvements include:

• Additional budget planning categories
• Improved recommendation personalization
• More advanced image analysis
• Additional AI models
• More detailed budget tracking
• Mobile-friendly improvements
• Advanced analytics
• Additional deployment options

18. Conclusion

PocketSmart AI provides a web-based solution for budget planning and personalized recommendations.

The system combines a user-friendly interface, FastAPI backend, SQLite database, authentication, multiple budget planners, and Artificial Intelligence.

The application demonstrates how AI can be integrated into a practical budget planning system to assist users with their everyday planning requirements.
