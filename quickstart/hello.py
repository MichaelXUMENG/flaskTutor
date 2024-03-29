from flask import Flask
app = Flask('__name__')

@app.route('/')
def index():
    return 'Index Page'

@app.route('/hello')
def hello():
    return 'Hello, World!'

@app.route('/user/<username>')
def show_user_profile(username):
    # show the user profile for that user
    return "User %s" % username

@app.route('/post/<int:post_id>')
def show_post(post_id):
    # Show the post with given ID, the ID is an integer
    return "Post %d" % post_id

@app.route('/path/<path:subpath>')
def show_subpath(subpath):
    # Show the subpath after '/path'
    return 'Subpath is %s' % subpath