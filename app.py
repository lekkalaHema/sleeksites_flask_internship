from flask import Flask, render_template, request, redirect, url_for, make_response
import uuid

app = Flask(__name__)

# Login route
@app.route('/', methods=['GET', 'POST'])
def login():
    # Check if user is already logged in
    if request.cookies.get('token'):
        return redirect(url_for('secret'))

    # If not, process login form
    if request.method == 'POST':
        # Validate credentials
        if request.form['username'] == 'user' and request.form['password'] == 'password':
            # Generate unique token
            token = str(uuid.uuid4())
            # Store token in user's browser cookies
            response = make_response(redirect(url_for('secret')))
            response.set_cookie('token', token)
            return response
        else:
            return render_template('login.html', error=True)
    else:
        return render_template('login.html', error=False)


# Secret route
@app.route('/secret')
def secret():
    # Check if user is logged in
    if request.cookies.get('token'):
        # If token is valid, show secret page
        return render_template('secret.html')
    else:
        # Otherwise, redirect to login page
        return redirect(url_for('login'))


# Logout route
@app.route('/logout')
def logout():
    # Delete token from user's browser cookies
    response = make_response(redirect(url_for('login')))
    response.delete_cookie('token')
    return response


if __name__ == '__main__':
    app.run(debug=True)
