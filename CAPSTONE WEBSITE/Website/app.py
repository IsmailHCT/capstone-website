# Import necessary modules
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user, login_required
from web3 import Web3










#Testing Request to make sure thats blockchain API is connected
#Blockchain connection setup (Ethereum node)
alchemy_url = "https://eth-mainnet.g.alchemy.com/v2/KpozVmKeuKbzZRt2GOvjeyFzxxMVIIaW"
w3 = Web3(Web3.HTTPProvider(alchemy_url))


print(w3.is_connected()) # Check if connected successfully



#Debug Request to make sure thats blockchain API is connected

'''
import requests

url = "https://eth-mainnet.g.alchemy.com/v2/KpozVmKeuKbzZRt2GOvjeyFzxxMVIIaW"

payload = {
    "id": 1,
    "jsonrpc": "2.0",
    "method": "debug_traceTransaction",
    "params": ["0x9e63085271890a141297039b3b711913699f1ee4db1acb667ad7ce304772036b"]
}
headers = {
    "accept": "application/json",
    "content-type": "application/json"
}

response = requests.post(url, json=payload, headers=headers)

print(response.text)

'''
'''

#Contract

#Replace "Your_ABI_String_Here" with the actual ABI of your contract.
#Replace "0xContractAddress" with the actual address of your deployed contract.

# Define the contract address and ABI ( Smart Contract Details )
contract_address = "0xContractAddress"
contract_abi = json.loads('Your_ABI_String_Here')

# Create a contract instance
contract = web3.eth.contract(address=contract_address, abi=contract_abi)


#Contract


#Block Chain

'''


#Flask app setup / database
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///signup.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'your_secret_key' # secret key
db = SQLAlchemy(app)   
migrate = Migrate(app, db)
login_manager = LoginManager(app)
login_manager.login_view = 'login'




#SignIn
# Define User and User_panel models for database
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String)

    def __repr__(self):
        return f"<User(name='{self.name}', email='{self.email}')>"
 

#Panel    
# User_panel model for storing website login information
# Contains id, website, username, password, and user_id fields

class User_panel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    website = db.Column(db.String(255))
    username = db.Column(db.String(255))
    password = db.Column(db.String(255))
    user_id = db.Column(db.Integer)

# User loader function for Flask-Login
    
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Define routes for signup, login, logout, and panel management
@app.route('/')
def home():
     # Renders home page template
    return render_template('home.html')

# Handles user signup

@app.route('/signup', methods=['POST', 'GET'])
def signup():
    
    if request.method == 'POST':
        
        data = request.get_json()
        print(data)
        print("-------------------------------------")
        name = data.get('name')
       
        email = data.get('email')
        password =data.get('password')
        
        if not name or not email or not password:
            return jsonify({'error': 'Missing required fields'}), 400

        
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            # return "Email already exists. Please use a different email."
            return jsonify({'error': 'Email Already Exists. Please Use A Different Email.'}), 400
            # show ('Email already exists. Please use a different email.', 'warning')
            # return redirect('/signup')

        new_user = User(name=name, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()

        login_user(new_user)
        return jsonify({'message': 'Signup successful'}), 200
        # show ("Signup Successfully", 'success')
        # return redirect("/")

    return render_template('login.html', signup = True)

# Handles user login

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        
        data = request.get_json()
        
        
        email = data.get('email')
        password = data.get('password')
 
        user = User.query.filter_by(email=email, password=password).first()
        if user:
            login_user(user)
            return jsonify({'message': 'Login Successful'})
           
        else:
            flash('Invalid email or password.', 'error')
            return jsonify({'error':'Invalid email or password.'})
            
    else:
        return render_template('login.html', login = True)


# Saves panel data to the database
    
@app.route('/save_panel', methods=['POST'])
@login_required
def save_data():
    website = request.form.get('website')
    username = request.form.get('username')
    password = request.form.get('password')

    # Create a new User object
    new_user = User_panel(website=website, username=username, password=password, user_id = current_user.id)

    # Add the new user to the database
    db.session.add(new_user)
    db.session.commit()

    return redirect('/panel')

# Updates panel data in the database

@app.route('/update_model', methods=['POST'])
@login_required
def update_data():
    
    
    website = request.form.get('website')
    username = request.form.get('username')
    password = request.form.get('password')
    id = request.form.get('row_id')

    panel = User_panel.query.get(id)
    
    if website:
        panel.website = website
    
    if username:
        panel.username = username
    
    if password and not "***" in password:
        panel.password = password

    db.session.commit()

    return redirect('/panel')


@app.route('/logout')
def logout():
    logout_user()
    return redirect("/")

#make user log in to be able to access panel
#Renders panel page with user's saved login information 

@app.route('/panel')
@login_required
def panel():
    users = User_panel.query.filter_by(user_id = current_user.id).all()
    return render_template('panel.html', users = users)


# Deletes selected panels from the database

@app.route('/delete_panels', methods=['POST'])
def delete_panels():
    panel_ids = request.json.get('panels', [])
    if not panel_ids:
        return jsonify({"message": "No panels selected."}), 400
    
    # Delete panels with the given IDs
    for panel_id in panel_ids:
        panel = User_panel.query.get(panel_id)
        if panel:
            db.session.delete(panel)
    
    db.session.commit()
    return jsonify({"message": "Selected panels deleted successfully."}), 200

if __name__ == '__main__':
    app.run(debug=True) # Runs the Flask app in debug mode 
