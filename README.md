# Nutrition Web
#### Video Demo:  https://youtu.be/FC3ZeeRjJjw
#### Description:
In this app you can check your daily nutrition selecting meals for breakfast, lunch and dinner. After this selection,
you can see the total amount of nutrients intake of a day. This app is pretty similar to the past project, but there are
new features like d3 charts and endpoints with json data.

Use this command to run flask:
```
flask run
```
#### Frameworks:
- Flask

#### Libraries: 
- D3 V3
- Bootstrap 5.2

#### templates Folder:

- addfood.html:
In this page you can add food with specific amount of nutrients. This nutrients must be per 100 grams of total amount.
- apologyze.html: This page was made to display a message with the specific error.
- changepass.html: A page made to change the password. It will display a message of success on the bottom or the page
apologyze with an error message.
- deletefood.html: This page was made to delete foods of the foods library using a combo box.
- deletemeal.html: It was made to delete meals of the meals plan using a combo box.
- food.html: A food library with nutrition facts. Was made with a table and a bar chart using the d3 library.
- index.html: The main page of the web app.
- layout.html: The main template with the nav bar and the footer.
- mealplan.html: This section was made to design the meal plan, adding food for lunch, breakfast and dinner using tables
and a pie chart.

#### flask_session Folder:
In this folder are stored the temp files of each session after a successful login.

#### venv Folder:
In this folder are stored the files of the python virtual environment.

#### flaskProject Folder:
- .env: Text file with an environmental variable to run flask in debug mode.
- app.py: The backend file with the functions and endpoints designed with flask.
- data.sql: The database backup just with data.
- identifiers.sqlite: the sqlite file with the db schema.
- login_helper.py: A python file with login functions used in the past project.