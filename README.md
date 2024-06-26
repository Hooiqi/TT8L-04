# Event Management System README
# Web
http://tt8l04.pythonanywhere.com/

# Dependencies (pip install)
pip install -r requirements.txt

# Set up flask virtual environment
https://flask.palletsprojects.com/en/3.0.x/installation/

# Start the development server:
python app.py

# Admin Guide:
To create a new event:
-Log in as an admin.
-Click "Create Event" and fill out the required details.
-Manage event drafts and user request (accept/reject)

# User Guide:
-Login/ Sign up as an user
-Request to join society to get membership
-View events by category, time, organiser and location
-Buy ticket for events 

# Database setup:
1. Ensure MySQL server is running.
2. Create a database named event_management_system.
3. Import the database structure and initial data from Dump.sql:
  mysql -u root -p event_management_system < Dump.sql
4. In app.py, update the database URI based on format : 
  app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqldb://<user>:<password>@<host>[:<port>]/<dbname>'

For example, user=root, password=abc, <host>[:<port>]=localhost, <dbname>=event_management_system: 
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqldb://root:abc@localhost/event_management_system'

# Stripe payment:
card number for testing: 4242 4242 4242 4242
