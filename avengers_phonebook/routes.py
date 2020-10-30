# Import the app variable from the init
from avengers_phonebook import app, db

# Import specific packages from flask
from flask import render_template,request, redirect, url_for

# Import Our Forms(s)
from avengers_phonebook.forms import UserInfoForm, LoginForm, PhoneForm

# Import of our models for the database
from avengers_phonebook.models import User, Post, check_password_hash

# Import for Flask Login functions - login_required
# login_user, current_user, logout_user
from flask_login import login_required,login_user,current_user,logout_user

db.create_all()

# Default Home Route
@app.route('/')
def home():
    return render_template('home.html')


# GET == Gathering Info
# POST == Sending Info
@app.route('/register', methods = ['GET','POST'])
def register():
    # Init our Form
    form = UserInfoForm()
    # Validation of our form
    if request.method == 'POST' and form.validate():
        # Get Information from the form
        name = form.name.data
        phone = form.phone.data
        email = form.email.data
        password = form.password.data
        # print the data to the server that comes from the form
        print(name,phone,email,password)

        # Creation/Init of our User Class (aka Model)
        user = User(name,phone,email,password)
        
        #Open a connection to the database
        db.session.add(user)  

        # Commit all data to the database
        db.session.commit()
        
    return render_template('register.html',user_form = form)

@app.route('/login', methods = ['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST' and form.validate():
        email = form.email.data
        password = form.password.data
        # Saving the logged in user to a variable
        logged_user = User.query.filter(User.email == email).first()
        # check the password of the newly found user
        # and validate the password against the hash value
        # inside of the database
        if logged_user and check_password_hash(logged_user.password, password):
            login_user(logged_user)
            return redirect(url_for('home'))
        else:
            return redirect(url_for('login'))
    return render_template('login.html', login_form = form)

#app.route('/logout')
#@login_required
#def logout():
#    logout_user()
#    return redirect(url_for('home'))

# Creation of phone route
@app.route('/phone', methods = ['GET', 'POST'])
@login_required
def phone():
    form = PhoneForm()
    if request.method == 'POST' and form.validate():
        title = form.title.data
        content = form.content.data
        user_id = current_user.id
        phone = Phone(title,content,user_id)

        db.session.add(phone)

        db.session.commit()
        return redirect(url_for('home'))
    return render_template('phone.html', phone_form = form)

# phone detail route to display phone number
@app.route('/phone/<int:phone_id>')
@login_required
def phone_detail(phone_id):
    phone = Phone.query.get_or_404(phone_id)
    return render_template('phone_detail.html', phone = phone)

@app.route('/phone/update/<int:phone_id>',methods = ['GET','POST'])
@login_required
def phone_update(phone_id):
    phone = Phone.query.get_or_404(phone_id)
    form = PhoneForm()

    if request.method == 'POST' and form.validate():
        title = form.title.data
        content = form.content.data
        user_id = current_user.id

        # Update the Database with new Info
        phone.title = title
        phone.content = content
        phone.user_id = user_id

        # Commit the changes to the database
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('phone_update.html', update_form = form)

@app.route('/phone/delete/<int:phone_id>', methods = ['GET','POST','DELETE'])
@login_required
def phone_delete(phone_id):
    phone = Phone.query.get_or_404(post_id)
    db.session.delete(phone)
    db.session.commit()
    return redirect(url_for('home'))