# flaskr

## Notes of ***flaskr*** application ##

### __init__.py ###
1. `app = Flask(__name__, instance_relative_config=True)` creates the **Flask** instance.
    * `__name__` is the name of the current Python module. The app needs to know where it's located to set up some paths, and `__name__` is a convenient way to tell it that.
    * `instance_relative_config=True` tells the app that configuration files are relative to the **instance folder**.
        The instance folder is located outside the `flaskr` package and can hold local data that shouldn't be committed to version control, such as confiduration secrets and the database file.

2. **app.config.from_mapping()** sets some default configuration that the app will use:
    * **SECRET_KEY** is userd by Flask and extensions to keep data safe. It's set to `'dev'` to provide a convenient value during development, but it should be overridden with a random value when deploying.
    * `DATABASE` is the path where the SQLite datavase file will be saved. It's under **app.instance_path**, which is the path that Flask has chosen for the instance folder. You'll learn more about the datavase in the next section.

3. **app.config.from_pyfile()** overrides the default configuration with values taken from the `config.py` file in the instance folder if it exists. For example, when deploying, this can be used to set a real `SECRET_KEY`.
    * `test_config` can also be passed to the factory, and will be used instead of the instance configuration. This is so the tests you'll write later in the tutorial can be configured independently of any development values you have configured.

4. **os.makedirs()** ensures that **app.instance_path** exists. Flask doesn't create the instance folder automatically, but it needs to be created because your project will create the SQLite databese file there.

5. **@app.route()** creates a simple route so you can see the application working before getting into the rest of tutorial. it creates a connection between the URL `/hello` and a function that returns a responsem the string `'Hello, World!'` in this case.


#####To Run the application#####
`export FLASK_APP=flaskr`
`export FLASK_ENV=development`
`flask run`


### db.py ###
1. **g** is a special object that is unique for each request. It is used to store data that might be accessed by multiple functions during the request. The connection is stored and reused instead of creating a new connection if `get_db` is called a second time in the same request.
2. ##current_app## is another special object that points to the Flask application handling the request. Since you used an application factory, there is no application object when writing the rest of your code. `get_db` will be called when the application has been created and is handling a request, so ##current_app## can be used.
3. ##sqlite3.connect()## establishes a connection to the file pointed at by the `DATABASE` configuration key. This file doesn't have to exist yet, and won't until you initialize the database later.
4. ##sqlite3.Row## tells the connection to return rows that behave list dicts. This allows accessing the columns by name.
5. `close_db` checks if a connection was created by checking if `g.db` was set. If the connection exists, it is closed. Further down you will tell your application about the `close_db` function in the application factory so that it is called after each request.

6. ##open_resource()## opens a file relative to the `flaskr` packages, which is useful since you won't necessarily know where that location is when deploying the application later. `get_db` returns a database connection, which is used to execute the commands read from the file.
7. ##click.command()## defines a command line command called `init-db` that calls the `init_db` function and shows a success message to the user. Here is more about writing commands: http://flask.pocoo.org/docs/1.0/cli/#cli


### auth.py ###
A view function is the code you write to respond to requests to your applications.
Flask uses patterns to match the incoming request URL to the view that should handle it. The view returns data that Flask turns into an outgoing response. Flask can also go the other direction and generate a URL to a view based on its name and arguments.

a **Blueprint** is a way to organize a group of related views and other code. Rather than registering views and other code directly with an application, they are registered with a blueprint. Then the blueprint is registered with the application when it is available in the factory function.
Flaskr will have 2 blueprints, one for authentication functions and one for the blog posts functions. The code for each blueprint will go in a separate module.

1. **@bp.route** associates the URL `/register` with the `register` view function. When Flask receives a request to `/auth/register`, it will call the `register` view and use the return value as response.

2. If the user submitted the form, **request.method** will be `'POST'`. In this case, start validating the input

3. **request.form** is a special type of **dict** mapping submitted form keys and values. The user will input their `username` and `password`.

4. Validate the `username` and `password` are not empty

5. Validate that `username` is not already registered by querying the database and cheking if a result is returned. **db.execute** takes a SQL query with `?` placeholders for any user input, and a tuple of values to replace the placeholders with. The database library will take care of escaping the values so you are not vulnerable to a *SQL injection attack*.

**fetchone()** returns one row from the query. If the query returned no results, it returns None. Later, **fetchall()** is used, which returns a list of all results.

6. If validation succeeds, insert the new user data into the database. For securiity, passwords should never be stored in the database directly. Instead, **generate_password_hash()** is used to securely hash the password, and that hash is stored. Since this query modifies data, **db.commit()** needs to be called afterwards to save the changes.

7. After storing the user, they are redirected to the login page. **url_for()** generates the URL for the login view based on its name. This is preferable to writing the URL directly as it allows you to change the URL later without changing all code that links to it. **redirect()** generates a redirect response to the generated URL.

8. If validation fails, the error is shown to the user. **flash()** stores messages that can be retrieved when rendering the template.

9. When the user initially navigates to `auth/register`, or there was an validation error, an HTML page with the registration form should be shown. **render_template()** will render a template containing the HTML, which you'll write in the next step of the tutorial


***There are a few differences from the `register` view***
1.  The user is queried first and stored in a variable for later user.
2. **check_password_hash()** hashes the submitted password in the same way as the stored has and securely compares them. If they match, the password is valid.
3. **session** is a **dict** that stores data across requests. When validation succeeds, the user's `id` is stored in a new session. The data is stored in a *cookie* that is sent to the browser, and the browser then sends it back with subsequent requests. Flask securely *signs* the data so that it can't be tampered with.

**bp.before_app_request()** registers a function that runs before the view function, no matter what URL is requested.
`load_logged_in_user` checks if a user id is stored in the **session** and gets that user's data from the database, storing it on **g.user**, which lasts for the length of the request. If there is no user id, or if the id doesn't exist, `g.user` will be `None`.

####Logout####
To log out, you need to remove the user id from the **session**. The `load_logged_in_user` won't load a user on subsequent requests.

####Require Authentication in Other Views####
Creating, editing, and deleting blog posts will require a user to be logged in. A *decorator* can be used to check this for each view it's applied to.

####Endpoints and URLs####
The **url_for()** function generates the URL to a view based on a name and arguments. The name associated with a view is also called the *endpoint*, and by defauly it's the same as the name of the view function.

For example, the `hello()` view that was added to the app factory earlier in the tutorial has the name `'hello'` and can be linked to with `url_for('hello')`. If it took an argument, which you'll see later, it would be linked to using `url_for('hello', who='World')`.

When using a bluepring, the name of the blueprint is prepended to the name of the function, so the endpoint for the `login` function you wrote above is `'auth.login'` because you added it to the `'auth'` blueprint.




