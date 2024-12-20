import os
from website import create_app

app = create_app()

if __name__ == '__main__':
    # # For Production and Testing
    # app.run(debug=True, host='127.0.0.1', port=5000)

    # For Deployment on Render
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)




'''
RUN THESE MIGRATION COMMANDS TO SYNC THE DATABASE WITH THE MODEL, WHENEVER THE MODEL IS UPDATED


```
flask --app website/__init__.py db init     # Initialize flask application for database migrations and creates migrations folder
flask --app website/__init__.py db migrate -m "Initial migration"   # Generate migration scripts in migrations/versions
flask --app website/__init__.py db upgrade      # Apply migrations to the database
```

Here; 
website/__init__.py is the file containing app
"Initial migration" is a simple message, could be anything else as well, but prefered meaningful message

Note: Run them one by one in terminal, and check the migration script manually before running upgrade command
'''