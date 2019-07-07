# flaskr

## Notes of ***flaskr*** application ##

### __init__.pt ###
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
