import secrets,os
from PIL import Image
from flask import url_for,render_template, flash, redirect, request,Response
from exercise.models import User,Post
from exercise.forms import RegistrationForm,LoginForm,UpdateAccountForm
from exercise import app,db,bcr
from flask_login import login_user,current_user,logout_user,login_required
from exercise.biceps import Biceps
posts = [
    {
        'author':'Janak Rajpurohit',
        'title':'Biceps Curl',
        'content':'Ecercise targetting your biceps',
        'date_posted':'July 20 2022'
    },
    {
        'author':'Sourav Andurkar',
        'title':'Push Ups',
        'content':'Ecercise Targeting Chest Muscles with core',
        'date_posted':'November 12 2022'
    }
]

@app.route('/')
def home():
    return render_template('home.html',posts=posts)   #variable posts will go in home.html which has value of posts(list)

@app.route('/about')
def about():
    return render_template('about.html',title="About")  #title variable is  pass to about.html with val 'about'

@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():       #if user is  already loggin then it will redirect to home page
        hashed_pw = bcr.generate_password_hash(form.password.data).decode('utf-8')
        # adding user to db
        # with app.app_context():
        user = User(username = form.username.data, email = form.email.data, password = hashed_pw)
        db.session.add(user)
        db.session.commit()
        flash(f"Account Created for {form.username.data}.", 'success')
        # print("Redirecting to login")
        return redirect(url_for("login"))
    else:
        print(form.errors)
    return render_template('register.html', title='Register', form=form)


@app.route("/login",methods=['GET','POST'])
def login():
    if current_user.is_authenticated:     #if user is  already loggin then it will redirect to home page
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcr.check_password_hash(user.password,form.password.data):
            login_user(user,remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next else redirect(url_for('home'))  #redirect to next page i.e.. account page if exsists else home
        else:
            # if form.password.data == db.query.filter_by(username=form.username.data)
            flash("Login Unsuccessfull, Please check email and password","danger")
    return render_template('login.html',title='Login',form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _ ,f_ext = os.path.splitext(form_picture.filename) 
    picture_fn = random_hex+f_ext
    # full hex filename path
    picture_path = os.path.join(app.root_path,'static/profile_pics',picture_fn)
    # resizing
    output_size = (125,125)
    i  =Image.open(form_picture)
    i.thumbnail(output_size)
    
    i.save(picture_path)
    return picture_fn


@app.route("/account",methods=["POST","GET"])
@login_required
def account():
    form = UpdateAccountForm()

    if form.validate_on_submit():
        if  form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash("Your account has been updated","success")
        return redirect(url_for("account"))
    elif request.method=="GET":   #if we are alreaady logged in then it will show curent user info
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static',filename='profile_pics/'+current_user.image_file)
    return render_template('account.html',title='Account',image_file=image_file,form=form)



# biceps
@app.route('/biceps')
def biceps():
    return render_template('biceps.html')

@app.route('/video')
def video():
    # returning response continuously to v_index.html, which has a func that provides frames
    return Response(Biceps.gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

