# CareMate - A Digital Companion for Elderly Care

CareMate is a user-friendly application designed to assist elderly individuals and their caregivers by addressing common challenges such as medication management, safety monitoring, health tracking, and emotional well-being. Built using Python and Tkinter, CAREMATE offers a simple, intuitive, and non-intrusive experience for users with minimal technical skills.

**Features**
- Daily Reminders: Voice and popup notifications for medications and appointments, triggered based on a CSV schedule.
- Safety Monitoring: Alerts for falls or missed check-ins displayed in a clear table, ensuring accountability.
- Health Monitoring: Visual display of vitals like BP, glucose, and heart rate to identify abnormal trends early.
- Motivational Quotes: Categorized quotes with voice narration to boost morale and combat loneliness.
- Exercise Suggestions: Personalized activity recommendations to encourage movement and physical well-being.
- Emergency & Contact Access: One-click access to emergency help or family contacts for instant support.
- Voice Assistance & Fullscreen UI: Easy navigation for users with limited technical skills.

**Methodology**

We adopted a user-centric and problem-driven approach by identifying pain points through research and feedback. Our focus was on simplicity, accessibility, and reliability:
- Developed using Python with Tkinter for a full-screen, intuitive GUI.
- Utilized CSV files for lightweight data storage and easy modification.
- Integrated pyttsx3 for voice interaction to enhance accessibility.
- Ensured offline functionality, reducing dependency on internet connectivity.
- Designed with soft pastel themes, large interactive elements, and clutter-free visuals for elderly users.

**Technologies Used**

- Python - Core programming language for application logic.
- Tkinter - Used to build a fullscreen and user-friendly GUI.
- CSV Files - Stores data in a structured, lightweight, editable format.
- pyttsx3 - Enables voice interaction for accessibility.
- Custom Styling - Soft pastel themes with large interactive elements for elderly users.
  
The system relies on three CSV datasets to manage user data efficiently:
- daily_reminders.csv - Stores medication and appointment schedules.
- health_monitoring.csv - Contains daily vitals like BP, glucose, and heart rate.
- safety_monitoring.csv - Records check-ins and safety alerts for accountability.

**Usage Guide**

Once the application is running:
- Click "Reminders" to view and manage upcoming medications/appointments.
- Navigate to "Safety Monitoring" for alerts and check-ins.
- Use "Health Monitoring" to see daily vitals and track abnormal trends.
- Motivational Quotes can be accessed for a mood boost.
- Exercise Suggestions offer activity recommendations.
- Emergency Contacts provide instant access to help in critical situations.

All data is stored in CSV files, ensuring users can easily modify schedules, health logs, and safety entries externally if needed.

