from flask import Flask, render_template, request, redirect, session, flash
import re
from datetime import datetime, date, time

emailRegex = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')
pwordRegex = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).+$')
dateRegex = re.compile(r'^[0-9]{4}-[0-9]{2}-[0-9]{2}$')

app = Flask(__name__)
app.secret_key = 'RegistrationFormValidation'

@app.route('/')
def index():
    return render_template("RegistrationForm.html")

@app.route('/verify', methods=['POST'])
def verify_info():
    # verify first name criteria
    if len(request.form['fname']) == 0:
        flash('First Name cannot be blank', 'error')
        return redirect('/')
    elif any(char.isdigit() for char in request.form['fname']):
        flash('First Name cannot have numbers', 'error')
        return redirect('/')
    else:
        session['fname'] = request.form['fname']

    # verify last name criteria
    if len(request.form['lname']) == 0:
        flash('Last Name cannot be blank', 'error')
        return redirect('/')
    elif any(char.isdigit() for char in request.form['lname']):
        flash('Last Name cannot have numbers', 'error')
        return redirect('/')
    else:
        session['lname'] = request.form['lname']

    # verify email criteria
    if len(request.form['email']) == 0:
        flash('Email cannot be blank', 'error')
        return redirect('/')
    elif not emailRegex.match(request.form['email']):
        flash('Invalid email address', 'error')
        return redirect('/')
    else:
        session['email'] = request.form['email']

    # verify birth-date criteria
    print "the form date is: " + request.form['bdate']
    if request.form['bdate'] == '':
        flash('Birth-date cannot be blank', 'error')
        return redirect('/')
    elif not dateRegex.match(request.form['bdate']):
        flash('Birth-date is not valid', 'error')
        return redirect('/')
    elif datetime.now().strftime('%Y%m%d') <= "".join(request.form['bdate'].split("-")):
        flash('Birthdate must be in the past', 'error')
        return redirect('/')
    else:
        session['bdate'] = request.form['bdate']

    # verify password criteria
    if len(request.form['pword']) == 0:
        flash('Password cannot be blank', 'error')
        return redirect('/')
    elif len(request.form['pword']) < 9:
        flash('Password must be greater than 8 characters long', 'error')
        return redirect('/')
    elif not pwordRegex.match(request.form['pword']):
        flash('Password must contain at least one lowercase letter, one uppercase letter, and one digit', 'error')
        return redirect('/')
    else:
        session['pword'] = request.form['pword']

    # verify confirm password criteria
    if len(request.form['cpword']) == 0:
        flash('Confirm password cannot be blank', 'error')
        return redirect('/')
    elif request.form['cpword'] != request.form['pword']:
        flash('Passwords do not match', 'error')
        return redirect('/')
    else:
        session['cpword'] = request.form['cpword']
  
    flash('Thanks for submitting your information.', 'success')
    return redirect('/')

app.run(debug=True)