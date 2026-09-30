POCKETSMART AI – PROJECT DESIGN

1. Introduction

The Project Design phase describes the overall design and structure of the PocketSmart AI application.

PocketSmart AI is designed as a web-based application that connects the user interface, backend services, database, and AI recommendation system.

2. System Architecture

The application follows a layered web application architecture.

The main components are:

• User Interface
• FastAPI Backend
• Authentication System
• Planner Modules
• Recommendation Service
• Google Gemini AI Service
• SQLite Database

3. System Flow

The basic system flow is:

User
↓
Web Browser
↓
FastAPI Application
↓
Authentication / Planner
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

If the AI service is unavailable, the system uses the fallback recommendation mechanism.

4. Frontend Design

The frontend provides the pages and forms required for user interaction.

The main pages include:

• Home Page
• Login Page
• Registration Page
• Dashboard
• Home Budget Planner
• Party Budget Planner
• Jewelry Budget Planner
• History Page

The frontend is developed using:

• HTML
• CSS
• JavaScript
• Jinja2 Templates

5. Backend Design

The backend is developed using Python and FastAPI.

The backend manages:

• User authentication
• Sessions
• Planner requests
• Recommendation generation
• Database operations
• Image uploads
• API endpoints

6. Authentication Design

The authentication system provides:

• User registration
• User login
• Password hashing
• Session management
• User logout
• Protected application pages

User authentication ensures that users can access their own application data and recommendation history.

7. Planner Design

PocketSmart AI contains three main planners.

7.1 Home Interior Planner

Input:

• Budget
• Room type
• Item quantities
• Additional information

Output:

• Budget-based home interior recommendations

7.2 Party Planner

Input:

• Budget
• Number of guests
• Event type
• Venue type
• Requirements
• Additional information

Output:

• Party planning recommendations
• Budget allocation suggestions

7.3 Jewelry Planner

Input:

• Budget
• Occasion
• Style preference
• Optional outfit image

Output:

• Jewelry recommendations
• Budget-based suggestions

8. AI Recommendation Design

The recommendation service receives information from the planner forms.

The information is converted into a structured request and sent to the configured Google Gemini AI service.

The AI response is then processed and displayed to the user.

If the AI service is unavailable, fallback recommendations are used.

9. Database Design

SQLite is used for storing application data.

The database stores information related to:

• Users
• Recommendations
• Recommendation history

The database allows users to access their previous recommendation information.

10. Image Upload Design

The Jewelry Planner provides an optional image upload feature.

The uploaded outfit image can be used as additional information during the jewelry recommendation process.

Uploaded files are handled by the backend and stored in the configured upload location.

11. Navigation Design

The application provides navigation between the main sections.

Public navigation includes:

• Home
• Features
• Testimonials
• Sign In
• Get Started

After login, application navigation provides:

• Dashboard
• Home Budget
• Party Budget
• Jewelry Budget
• History
• Logout

12. API Design

FastAPI provides the backend API and interactive API documentation.

The application provides routes for:

• Pages
• Authentication
• Planners
• Sessions

The interactive API documentation can be accessed through the FastAPI documentation endpoint.

13. Security Design

The system includes security measures such as:

• Password hashing
• Session-based authentication
• Environment variables for sensitive configuration
• Protected routes
• Input validation

14. Error Handling

The application should handle errors such as:

• Invalid login credentials
• Invalid form input
• Missing required fields
• Database errors
• AI service errors
• Invalid image uploads

Fallback recommendations help maintain functionality when the external AI service is unavailable.

15. Overall Design

The overall design connects the frontend, backend, database, and AI service into one web-based application.

The design allows users to enter their requirements, receive recommendations, save recommendation information, and view their previous recommendations through the application.
