# Templates #

The template files will be stored in the `templates` directory inside the `flaskr` package.

Templates are files that contain static data as well as placeholders for dynamic data. A template is rendered 
with specific data to produce a final document. Flask uses the **Jinja** template library to render templates.

In your application, you will use templates to render **HTML** which will display in the user's browser. In Flask, Jinja 
is configured to *autoescape* any data that is rendered in HTML templates. This means that it's safe to render user 
input; any characters they've entered that could mess with the HTML, such as `<` and `>` will be *escaped* with *safe*
values that look the same in the browser but don't cause unwanted effects.

Jinja look and behaves mostly like Python. Special delimiters are used to distinguish Jinja syntax from the static 
data in the template. Anything between `{{` and `}}` is an expression that will be output to the final document. `{%`
and `%}` denotes a control flow statement like if and for. Unlike Python, blocks are denoted by start and end tags
rather than indentation since static text within a block could change indentation.

## The Base Layout ##

Each page in the application will have the same basic layout around a different body. Instead of writing the entire 
HTML structure in each template, each template will *extend* a base template and override specific sections.

**g** is automatically available in templates. Based on if `g.user` is set (from `load_logged_in_user`), either the user-name 
and a log out link are displayed, otherwise links to register and log in are displayed. **url_for()** is also automatically
available, and is used to generate URLs to views instead of writeing them out manually.

After the page title, and before the content, the template loops over each message returned by 
**get_flashed_message()**. You used **flash()** in the views to show error messages, and this is the code that will 
display them.

There are 3 blocks defined here that will be overridden in the other templates:

1. `{% block title %}` will change the title displayed in the browser's tab and window title.
2. `{% block header %}` is similar to `title` but will change the title displayed on the page.
3. `{% block content %}` is where the content of each page goes, such as the login form or a blog post.

The base template is directly in the `templates` directory. To keep the others organized, the templates for a blueprint
will be placed in a directory with the same name as the blueprint. (e.g. flaskr/templates/auth/register.html)

### Register ###

`{% extends 'base.html' %}` tells Jinja that this template should replace the blovks from the base template. All 
the rendered content must appear inside `{% block %}` tags that override blocks from the base template.

A useful pattern used here is to place `{% block title %}` inside `{% block header %}`. This will set the title block 
and then output the value of it into the header block, so that both the window and page share the same title without 
writing it twice.

The `input` tags are using the `required` attibute here. This tells the browser not to submit the form until those 
fields are filled in. If the user is using an older browser that doesn't support that attribute, or if they are using 
something besides a browser to make requests, you still want to validate the data in the Flask view. It's important 
to always fully validate the data on the server, even if the client does some validation as well.

## Register A User ##
Make sure the server is running, and then go to http://127.0.0.1:5000/auth/register


