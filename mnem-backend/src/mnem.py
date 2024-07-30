from flask import Flask, jsonify, request, make_response, session
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_cors import CORS, cross_origin
from flask_session import Session

app = Flask(__name__)
cors = CORS(app, supports_credentials=True)
app.config['SECRET_KEY'] = 'your_secret_key'  # Replace with a real secret key
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_COOKIE_SAMESITE'] = 'None'
app.config['SESSION_COOKIE_SECURE'] = True
Session(app)

# Dummy data to simulate a database
users = [
    {"id": 1, "username": "admin", "password": "admin_pass"},  # Update the password field
    {"id": 2, "username": "master", "password": "master_pass"},  
    {"id": 3, "username": "player", "password": "player_pass"}  
]

# Flask-Login setup
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Define a User class for Flask-Login
class User(UserMixin):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

# Define a login route
@app.route('/login', methods=['POST', 'GET'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')

    # Find the user in the users list
    user = next((user for user in users if user['username'] == username and user['password'] == password), None)

    if user:
        # Create a User object and log in the user
        user_obj = User(user['id'], user['username'], user['password'])
        login_user(user_obj)
        #set session 'user_id' to user['id'] (type object 'Flask' has no attribute 'session')
        session['user_id'] = user['id']
        response = make_response(jsonify({'success': True}), 200)
        response.headers.add('Access-Control-Allow-Origin', 'http://localhost:3000')  # Replace with your actual origin
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        response.headers.add('Access-Control-Allow-Methods', 'GET, POST, OPTIONS, PUT, DELETE')
        return response
    else:
        return jsonify({'success': False, 'message': 'Invalid credentials'}), 401

@app.route('/logout')
@login_required
def logout():
    logout_user()
    #Flask session clear
    return jsonify({'message': 'Logged out successfully'}), 200

@app.route('/logged-in')
def check_logged_in():
    if current_user.is_authenticated:
        return jsonify({'loggedIn': True}), 200
    else:
        return jsonify({'loggedIn': False}), 200
    
@login_manager.user_loader
def load_user(user_id):
    # Find the user by ID
    user = next((user for user in users if user['id'] == user_id), None)
    if user:
        # Create a User object and return it
        user_obj = User(user['id'], user['username'], user['password'])
        return user_obj
    return None

# Define the request_loader function
@login_manager.request_loader
def load_user_from_request(request):
    # Extract the user information from the request
    # For example, if the user ID is in the 'user_id' field of the request JSON:
    user_id = request.json.get('user_id')
    if user_id:
        # Find the user by ID
        user = next((user for user in users if user['id'] == user_id), None)
        if user:
            # Create a User object and return it
            user_obj = User(user['id'], user['username'], user['password'])
            return user_obj
    return None

class Item:
    def __init__(self, item_id, name, price, weight):
        self.item_id = item_id
        self.name = name
        self.price = price  # Price in Gold
        self.weight = weight  # Weight in pounds

class Campaign:
    def __init__(self, campaign_id, name, admin_id):
        self.campaign_id = campaign_id
        self.name = name
        self.admin_id = admin_id  # The ID of the Admin user who created the campaign
        self.masters = []  # List of Master IDs
        self.players = []  # List of Player IDs

class Player:
    def __init__(self, player_id, name, campaign_id):
        self.player_id = player_id
        self.name = name
        self.campaign_id = campaign_id  # The ID of the Campaign the player belongs to
        self.gold = 0  # Amount of Gold the player has
        self.inventory = []  # List of Item objects

    def add_item(self, item):
        self.inventory.append(item)

    def remove_item(self, item):
        if item in self.inventory:
            self.inventory.remove(item)

    def add_gold(self, amount):
        self.gold += amount

    def remove_gold(self, amount):
        if self.gold >= amount:
            self.gold -= amount

    def net_worth(self):
        return sum(item.price for item in self.inventory) + self.gold

# Dummy data to simulate a database
items = []
campaigns = []
players = []

@app.route('/api/items', methods=['POST'])
def create_item():
    # Check if the user has the necessary permissions
    if not current_user.is_authenticated:
        return jsonify({'error': 'You must be logged in to create items'}), 401
    elif current_user.username not in ['admin']:
        return jsonify({'error': 'You do not have permission to create items'}), 403
    data = request.json
    new_item = Item(data['item_id'], data['name'], data['price'], data['weight'])
    items.append(new_item)
    return jsonify(new_item.__dict__), 201

@app.route('/api/items/<int:item_id>', methods=['GET'])
def get_item(item_id):
    item = next((item for item in items if item.item_id == item_id), None)
    if item:
        return jsonify(item.__dict__), 200
    else:
        return jsonify({'error': 'Item not found'}), 404

@app.route('/api/items/list', methods=['GET'])
def get_items():
    current_items = []
    for item in items:
        current_items.append(item.__dict__)
    return jsonify(current_items), 200
@app.route('/api/items/<int:item_id>', methods=['PUT'])
def update_item(item_id):
    data = request.json
    item = next((item for item in items if item.item_id == item_id), None)
    if item:
        item.name = data['name']
        item.price = data['price']
        item.weight = data['weight']
        return jsonify(item.__dict__), 200
    else:
        return jsonify({'error': 'Item not found'}), 404

@app.route('/api/items/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    item = next((item for item in items if item.item_id == item_id), None)
    if item:
        items.remove(item)
        return jsonify({'message': 'Item deleted'}), 200
    else:
        return jsonify({'error': 'Item not found'}), 404

@app.route('/api/campaigns/list', methods=['GET'])
def get_campaigns():
    return jsonify(campaigns)

@app.route('/api/campaigns', methods=['GET', 'POST', 'PUT', 'PATCH', 'DELETE', 'OPTIONS', 'HEAD'])
@cross_origin(supports_credentials=True)
@login_required
def create_campaign():
    if (current_user.username not in ['admin', 'master']) or current_user.exists() == False:
        return jsonify({'error': 'Insufficient permissions'}), 403
    data = request.get_json()
    print(data) # test, remove later
    new_campaign = Campaign(data['campaign_id'], data['name'], data['admin_id'])
    campaigns.append(new_campaign)
    response = make_response(jsonify(new_campaign.__dict__), 201)
    response.headers.add('Access-Control-Allow-Origin', 'http://localhost:3000') # Replace with your actual origin
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
    response.headers.add('Access-Control-Allow-Methods', 'GET', 'POST', 'PUT', 'PATCH', 'DELETE', 'OPTIONS', 'HEAD')
    response.headers.add('Content-Type', 'application/json')
    return response

@app.route('/api/players', methods=['POST'])
def create_player():
    data = request.json
    new_player = Player(data['player_id'], data['name'], data['campaign_id'])
    players.append(new_player)
    return jsonify(new_player.__dict__), 201

# Additional routes for adding/removing gold, items, etc.
@app.route('/api/players/<int:player_id>/gold', methods=['POST'])  
def add_gold(player_id):
    data = request.json
    player = next((player for player in players if player.player_id == player_id), None)
    if player:
        player.add_gold(data['amount'])
        return jsonify(player.__dict__), 200
    else:
        return jsonify({'error': 'Player not found'}), 404

@app.route('/api/players/<int:player_id>/gold', methods=['DELETE'])
def remove_gold(player_id):
    data = request.json
    player = next((player for player in players if player.player_id == player_id), None)
    if player:
        player.remove_gold(data['amount'])
        return jsonify(player.__dict__), 200
    else:
        return jsonify({'error': 'Player not found'}), 404

@app.route('/api/players/<int:player_id>/items', methods=['POST'])
def add_item(player_id):
    data = request.json
    player = next((player for player in players if player.player_id == player_id), None)
    if player:
        player.add_item(data['item_id'])
        return jsonify(player.__dict__), 200
    else:
        return jsonify({'error': 'Player not found'}), 404

@app.route('/api/players/<int:player_id>/items', methods=['DELETE'])
def remove_item(player_id):
    data = request.json
    player = next((player for player in players if player.player_id == player_id), None)
    if player:
        player.remove_item(data['item_id'])
        return jsonify(player.__dict__), 200
    else:
        return jsonify({'error': 'Player not found'}), 404

@app.route('/api/players/<int:player_id>/items', methods=['GET'])
def get_player_items(player_id):
    player = next((player for player in players if player.player_id == player_id), None)
    if player:
        return jsonify(player.inventory)
    else:
        return jsonify({'error': 'Player not found'}), 404

@app.route('/api/campaigns/<int:campaign_id>/players', methods=['GET'])
def get_players(campaign_id):
    campaign = next((campaign for campaign in campaigns if campaign.campaign_id == campaign_id), None)
    if campaign:
        return jsonify(campaign.players)
    else:
        return jsonify({'error': 'Campaign not found'}), 404

@app.route('/api/campaigns/<int:campaign_id>/masters', methods=['GET'])
def get_masters(campaign_id):
    campaign = next((campaign for campaign in campaigns if campaign.campaign_id == campaign_id), None)
    if campaign:
        return jsonify(campaign.masters)
    else:
        return jsonify({'error': 'Campaign not found'}), 404

@app.route('/api/campaigns/<int:campaign_id>/players', methods=['POST'])
@login_required
def add_player(campaign_id):
    if current_user.username not in ['admin', 'master']:
        return jsonify({'error': 'Insufficient permissions'}), 403
    
    data = request.json
    campaign = next((campaign for campaign in campaigns if campaign.campaign_id == campaign_id), None)
    if campaign:
        campaign.players.append(data['player_id'])
        return jsonify(campaign.__dict__), 200
    else:
        return jsonify({'error': 'Campaign not found'}), 404

@app.route('/api/campaigns/<int:campaign_id>/masters', methods=['POST'])
@login_required
def add_master(campaign_id):
    if current_user.username not in ['admin']:
        return jsonify({'error': 'Insufficient permissions'}), 403
    data = request.json
    campaign = next((campaign for campaign in campaigns if campaign.campaign_id == campaign_id), None)
    if campaign:
        campaign.masters.append(data['master_id'])
        return jsonify(campaign.__dict__), 200
    else:
        return jsonify({'error': 'Campaign not found'}), 404

@app.route('/api/campaigns/<int:campaign_id>/masters', methods=['DELETE'])
@login_required
def remove_master(campaign_id):
    if current_user.username not in ['admin']:
        return jsonify({'error': 'Insufficient permissions'}), 403
    data = request.json
    campaign = next((campaign for campaign in campaigns if campaign.campaign_id == campaign_id), None)
    if campaign:
        campaign.masters.remove(data['master_id'])
        return jsonify(campaign.__dict__), 200
    else:
        return jsonify({'error': 'Campaign not found'}), 404

@app.route('/api/campaigns/<int:campaign_id>/players', methods=['DELETE'])
def remove_player(campaign_id):
    data = request.json
    campaign = next((campaign for campaign in campaigns if campaign.campaign_id == campaign_id), None)
    if campaign:
        campaign.players.remove(data['player_id'])
        return jsonify(campaign.__dict__), 200
    else:
        return jsonify({'error': 'Campaign not found'}), 404


# Example usage:
# Creating an item
sword = Item(1, 'Sword', 100, 5)

# Creating a campaign and adding an admin ID
campaign1 = Campaign(1, 'Epic Quest', admin_id=1)

# Creating a player and adding them to a campaign
player1 = Player(1, 'Brave Adventurer', campaign_id=1)
player1.add_gold(500)  # Adding gold to the player's account
player1.add_item(sword)  # Adding an item to the player's inventory

# You can add more methods to these classes as needed for your application logic.

@app.route('/api/users', methods=['POST'])
@login_required
def create_user():
    if current_user.username not in ['admin']:
        return jsonify({'error': 'Insufficient permissions'}), 403
    
    new_user = request.json
    users.append(new_user)
    return jsonify(new_user), 201

if __name__ == '__main__':
    app.run(debug=True)