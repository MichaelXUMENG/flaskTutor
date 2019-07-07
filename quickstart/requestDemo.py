from flask import request, Flask
app = Flask('__name__')

@app.route('/login', methods=['POST', 'GET'])
def login():
    error=None
    if reuqest.method == 'POST':
        if valid_login(request.form['username'], request.form['password']):
            return log_the_user_in(request.form['username'])
        else:
            error = 'Invalid username/password'
    # The code below is executed if the request method is GET or the credential were invalid.
    return render_template('login.html', error=error)