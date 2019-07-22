# flaskTutor

***This project is created for following the flask tutoring.***

### For quickstart application
The reference page is http://flask.pocoo.org/docs/1.0/quickstart/#accessing-request-data

#### Convert types: ###
types | description
--- | ---
`string` | (default) accepts any text without a slash
`int` | accepts positive integers
`float` | accepts positive floating point values
`path` | like `string` but also accepts slash
`uuid` | accepts UUID strings




### For tutoring application ###
The reference page is http://flask.pocoo.org/docs/1.0/tutorial/
*This tutorial will walk you through creating a basic blog application called Flaskr.*


### The Application Factory ###
The '__init__.py' is working as the *application factory* for this project. An **Flask** instance will be created within this function(the factory): 
Any configuration, registration, and other setup the application needs will happen inside the function, and the application (the instance) will be returned.