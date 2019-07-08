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

a ##Blueprint## is a way to organize a group of related views and other code. Rather than registering views and other code directly with an application, they are registered with a blueprint. Then the blueprint is registered with the application when it is available in the factory function.
Flaskr will have 2 blueprints, one for authentication functions and one for the blog posts functions. The code for each blueprint will go in a separate module.

1.




