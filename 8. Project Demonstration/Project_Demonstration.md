POCKETSMART AI – PROJECT DEMONSTRATION

1. Introduction

The Project Demonstration phase presents the completed PocketSmart AI web application and explains how the main features of the system work.

The demonstration shows the complete flow from opening the website and registering a user to creating budget plans, receiving recommendations, and viewing recommendation history.

2. Demonstration Objectives

The demonstration aims to show:

• The working PocketSmart AI website
• User registration and login
• Dashboard navigation
• Home Interior Budget Planner
• Party Budget Planner
• Jewelry Budget Planner
• AI-based recommendations
• Recommendation history
• Optional outfit image upload
• User logout

3. Application Launch

The application is started using the configured FastAPI application.

After starting the application, the user opens the website through a web browser.

The home page displays the PocketSmart AI introduction and provides options to get started or sign in.

4. User Registration Demonstration

Steps:

1. Open the PocketSmart AI website.
2. Select the registration option.
3. Enter the required user information.
4. Submit the registration form.
5. Verify that the account is created successfully.

Expected Result:

A new user account is created and the user can proceed to log in.

5. User Login Demonstration

Steps:

1. Open the Login page.
2. Enter the registered username or email and password.
3. Submit the login form.
4. Verify successful authentication.

Expected Result:

The user is logged in and can access the application dashboard.

6. Dashboard Demonstration

After login, the dashboard is displayed.

The dashboard provides access to:

• Home Budget
• Party Budget
• Jewelry Budget
• History

The user can select the required planner from the dashboard.

7. Home Interior Budget Planner Demonstration

Steps:

1. Open the Home Budget Planner.
2. Enter the available budget.
3. Select the required room types.
4. Enter item quantities.
5. Add additional requirements if needed.
6. Submit the form.

Expected Result:

The system processes the entered information and displays home interior recommendations.

8. Party Budget Planner Demonstration

Steps:

1. Open the Party Budget Planner.
2. Enter the available budget.
3. Enter the number of guests.
4. Select the event type.
5. Select the venue type.
6. Enter the required items or additional information.
7. Submit the form.

Expected Result:

The system generates party planning recommendations based on the entered information.

9. Jewelry Budget Planner Demonstration

Steps:

1. Open the Jewelry Budget Planner.
2. Enter the budget.
3. Select the occasion.
4. Enter the preferred style.
5. Optionally upload an outfit image.
6. Submit the form.

Expected Result:

The system generates jewelry recommendations based on the user's budget and preferences.

10. AI Recommendation Demonstration

The submitted planner information is processed by the recommendation service.

When the Google Gemini AI service is available, the system uses it to generate personalized recommendations.

The generated recommendation is displayed to the user.

11. Fallback Recommendation Demonstration

If the AI service is unavailable or does not return a usable response, the application uses the fallback recommendation system.

Expected Result:

The user still receives a recommendation instead of the application failing completely.

12. Recommendation History Demonstration

Steps:

1. Generate a recommendation.
2. Open the History page.
3. View the previously generated recommendation.

Expected Result:

The user's previous recommendation information is displayed.

13. Logout Demonstration

Steps:

1. Open the application navigation.
2. Select Logout.
3. Verify that the user session is ended.

Expected Result:

The user is logged out and protected application pages are no longer accessible without logging in again.

14. API Documentation Demonstration

The FastAPI application provides interactive API documentation.

The documentation can be opened through the `/docs` endpoint.

The API documentation can be used to view and test the available API endpoints.

15. Complete Demonstration Flow

The complete application demonstration follows this sequence:

Website
↓
Registration
↓
Login
↓
Dashboard
↓
Select Planner
↓
Enter Budget and Requirements
↓
Generate Recommendation
↓
View Recommendation
↓
Save Recommendation
↓
View History
↓
Logout

16. Expected Demonstration Result

The demonstration should show that PocketSmart AI provides a complete web-based budget planning and recommendation workflow.

Users can register, log in, select a planner, enter their requirements, receive recommendations, view their recommendation history, and log out of the application.

17. Conclusion

The Project Demonstration phase presents the final working flow of PocketSmart AI.

The demonstration confirms the integration of the frontend, backend, database, authentication, budget planners, and AI recommendation system into a single web-based application.
