from InstagramAPI import InstagramAPI
from flask import Flask, render_template, redirect, request, url_for
from forms import LoginForm
from database import db_session
from flask_login import LoginManager, login_required, login_user, logout_user, current_user, UserMixin
from models import User
from sqlalchemy import asc
import config
import time

global api
api = None

app = Flask(__name__)
app.debug = True
app.config.from_object(config)

# Integration von Flask-Login
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

#loads user id
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

#shutdown
@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()
 
#loads basic page 
@app.route('/')
def index():
    return render_template('index.jinja')

#logs user in. writes data i ndatabase if user is new, else remembers user in database. CAREFUL PASSWORDS NOT HASED YET!!!
@app.route("/login", methods=["GET", "POST"])
def login():
    global api
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        api = InstagramAPI(username, password)
        Instalogin = api.login()
        api.getProfileData()
        user_id=api.LastJson['user']['pk']
        print user_id
        user = User.query.filter_by(username=form.username.data).first()
        if user is not None:
            if Instalogin == True:
                return redirect(url_for('logged_in'))       
        else:        
            new_user = User(id=user_id, username=form.username.data, password=form.password.data, active=form.active.data)
            if Instalogin == True:
                db_session.add(new_user)
                db_session.commit()
                return redirect(url_for('logged_in'))
                print "logged in"
                return redirect(request.args.get('next') or url_for('logged_in'))
    else:
        print "login failed"
        return render_template('login.jinja', form=form)
    return render_template('login.jinja', form=form)

# shows the logged_in page. leads to info page    
@app.route("/logged_in")          
def logged_in():
    users = User.query.order_by(asc('username')).all()
    print users
    return render_template('logged_in.jinja', users=users)
  
#logout function  
@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash('Logged out successfully')
    return redirect(url_for('index'))
    
# shows the followers, following and unfollwers  
@app.route("/info/<user_id>", methods=["GET", "POST"])    
def info(user_id):

    user = User.query.filter_by(id=user_id).first()
    print user_id
    followers   = []
    next_max_id = True
    while next_max_id:
        print next_max_id
        #first iteration hack
        if next_max_id == True: next_max_id=''
        _ = api.getUserFollowers(user_id,maxid=next_max_id)
        followers.extend ( api.LastJson.get('users',[]))
        next_max_id = api.LastJson.get('next_max_id','')
        time.sleep(1)
        
    following   = []
    user = User.query.filter_by(id=user_id).first()
    next_max_id = True
    while next_max_id:
        print next_max_id
        #first iteration hack
        if next_max_id == True: next_max_id=''
        _ = api.getUserFollowings(user_id,maxid=next_max_id)
        following.extend ( api.LastJson.get('users',[]))
        next_max_id = api.LastJson.get('next_max_id','')
        time.sleep(1)    
        
        
    followers_list=followers
    user_list = map(lambda x: x['username'] , followers_list)
    followers_set= set(user_list)
    print len(followers_set)
    follower = len(followers_set)
    
    following_list=following
    user_list = map(lambda x: x['username'] , following_list)
    following_set= set(user_list)
    print len(following_set)
    following = len(following_set)
    
    not_following_back=following_set-followers_set
    print not_following_back
    n_follow = sorted(not_following_back)
    print n_follow
      
    return render_template('info.jinja', user=user, follower=follower, following=following, n_follow=n_follow)
 
# should show the unfollower not working atm    
@app.route("/unfollowers/<user_id>", methods=["GET", "POST"])     
def unfollowers(user_id): 

    user = User.query.filter_by(id=user_id).first()
    
    followers   = []
  
    next_max_id = True
    while next_max_id:
        print next_max_id
        #first iteration hack
        if next_max_id == True: next_max_id=''
        _ = InstagramAPI.getUserFollowers(user_id,maxid=next_max_id)
        followers.extend ( InstagramAPI.LastJson.get('users',[]))
        next_max_id = InstagramAPI.LastJson.get('next_max_id','')
        time.sleep(1)
        
    followers_list=followers
    user_list = map(lambda x: x['username'] , following_list)
    following_set= set(user_list)
    user_list = map(lambda x: x['username'] , followers_list)
    followers_set= set(user_list)
    
    not_following_back=following_set-followers_set
    
    return render_template('info.jinja', user=user, not_following_back=not_following_back)
    
'''  
@app.route("/followers/<user_id>", methods=["GET", "POST"])    
def followers(user_id):

    user = User.query.filter_by(id=user_id).first()
    print user_id
  #  inforation = db_session.query(User).filter(User.id == id_user)
  #  print inforation
    followers   = []
    next_max_id = True
    while next_max_id:
        print next_max_id
        #first iteration hack
        if next_max_id == True: next_max_id=''
        _ = api.getUserFollowers(user_id,maxid=next_max_id)
        followers.extend ( api.LastJson.get('users',[]))
        next_max_id = api.LastJson.get('next_max_id','')
        time.sleep(1)
        
        
    following   = []
    user = User.query.filter_by(id=user_id).first()
    next_max_id = True
    while next_max_id:
        print next_max_id
        #first iteration hack
        if next_max_id == True: next_max_id=''
        _ = api.getUserFollowings(user_id,maxid=next_max_id)
        following.extend ( api.LastJson.get('users',[]))
        next_max_id = api.LastJson.get('next_max_id','')
        time.sleep(1)
        
    followers_list=followers
    user_list = map(lambda x: x['username'] , followers_list)
    followers_set= set(user_list)
    print len(followers_set)
    follower = len(followers_set)
    
    following_list=followers
    user_list = map(lambda x: x['username'] , following_list)
    following_set= set(user_list)
    print len(following_set)
    following = len(following_set)
    
    return render_template('followers.jinja', user=user, follower=follower, following=following)
 
#shows the amount of following for the logged in account   
@app.route("/following/<user_id>", methods=["GET", "POST"])     
def following(user_id):

    following   = []
    user = User.query.filter_by(id=user_id).first()
    next_max_id = True
    while next_max_id:
        print next_max_id
        #first iteration hack
        if next_max_id == True: next_max_id=''
        _ = api.getUserFollowings(user_id,maxid=next_max_id)
        following.extend ( api.LastJson.get('users',[]))
        next_max_id = api.LastJson.get('next_max_id','')
        time.sleep(1)
    
    following_list=following
    user_list = map(lambda x: x['username'] , following_list)
    following_set= set(user_list)
    print len(following_set)
    
    return render_template('following.jinja', user=user)
  
'''  
'''
#shows the amount of followers for the logged in account       
def follower():
    followers   = []
  
    next_max_id = True
    while next_max_id:
        print next_max_id
        #first iteration hack
        if next_max_id == True: next_max_id=''
        _ = InstagramAPI.getUserFollowers(user_id,maxid=next_max_id)
        followers.extend ( InstagramAPI.LastJson.get('users',[]))
        next_max_id = InstagramAPI.LastJson.get('next_max_id','')
        time.sleep(1)
        
    followers_list=followers
    user_list = map(lambda x: x['username'] , followers_list)
    followers_set= set(user_list)
    print len(followers_set)
    
   
#shows the amount of unfollowers for the logged in account       
def unfollower():
    followers   = []
  
    next_max_id = True
    while next_max_id:
        print next_max_id
        #first iteration hack
        if next_max_id == True: next_max_id=''
        _ = InstagramAPI.getUserFollowers(user_id,maxid=next_max_id)
        followers.extend ( InstagramAPI.LastJson.get('users',[]))
        next_max_id = InstagramAPI.LastJson.get('next_max_id','')
        time.sleep(1)
        
    followers_list=followers
    user_list = map(lambda x: x['username'] , following_list)
    following_set= set(user_list)
    user_list = map(lambda x: x['username'] , followers_list)
    followers_set= set(user_list)
    
    not_following_back=following_set-followers_set
    

# gives a list with unfollowers     
def show_unfollower():    
    followers   = []
  
    next_max_id = True
    while next_max_id:
        print next_max_id
        #first iteration hack
        if next_max_id == True: next_max_id=''
        _ = InstagramAPI.getUserFollowers(user_id,maxid=next_max_id)
        followers.extend ( InstagramAPI.LastJson.get('users',[]))
        next_max_id = InstagramAPI.LastJson.get('next_max_id','')
        time.sleep(1)
        
    followers_list=followers
    user_list = map(lambda x: x['username'] , following_list)
    following_set= set(user_list)
    user_list = map(lambda x: x['username'] , followers_list)
    followers_set= set(user_list)
    
    not_following_back=following_set-followers_set
  
    ''' 
    
if __name__ == "__main__":
    app.run()