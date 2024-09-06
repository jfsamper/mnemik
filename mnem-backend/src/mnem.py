from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, current_user, get_jwt_identity
from flask_cors import CORS

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'  # Update the secret key!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
jwt = JWTManager(app)
CORS(app, resources={r"/*": {"origins": "*"}})

# --------------------------------------------    Users / Login      -----------------------------------------------------------
# Dummy data to simulate a database
users = [
    {"id": 1, "username": "admin", "password": "admin_pass"},
    {"id": 2, "username": "master", "password": "master_pass"},  
    {"id": 3, "username": "player", "password": "player_pass"}  
]

# Handle CORS preflight requests
@app.route('/<path:path>', methods=['OPTIONS'])
def handle_cors_options(path):
    return jsonify({}), 200

# Define a login route
@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')

    # Find the user in the users list
    user = next((user for user in users if user['username'] == username and user['password'] == password), None)

    if user:
        # Create an access token
        access_token = create_access_token(identity=user['id'])
        return jsonify({'success': True, 'access_token': access_token}), 200
    else:
        return jsonify({'success': False, 'message': 'Invalid credentials'}), 401

@app.route('/logout')
@jwt_required()
def logout():
    return jsonify({'message': 'Logged out successfully'}), 200

@app.route('/verify', methods=['POST'], endpoint='verifyToken')
def verifyToken():
        return jsonify({'message': 'Token verified successfully'}), 200

@app.route('/register', methods=['POST'], endpoint='create_user')
@jwt_required()
def create_user():
    if current_user.username not in ['admin']:
        return jsonify({'error': 'Insufficient permissions'}), 403
    
    new_user = request.json
    users.append(new_user)
    return jsonify(new_user), 201

if __name__ == '__main__':
    app.run(debug=True)


# --------------------------------------------    Database       -----------------------------------------------------------
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

# --------------------------------------------    Campaigns         ------------------------------------------------------------

@app.route('/api/campaigns/list', methods=['GET'], endpoint='get_campaigns')
def get_campaigns():
    return jsonify(campaigns), 200

@app.route('/api/campaigns/create', methods=['POST'], endpoint='create_campaign')
@jwt_required()
def create_campaign():
    if (current_user.username not in ['admin', 'master']) or current_user.exists() == False:
        return jsonify({'error': 'Insufficient permissions'}), 403
    data = request.json
    print(data) # test, remove later
    new_campaign = Campaign(data.get('campaign_id'), data.get('name'), data.get('admin_id'))
    campaigns.append(new_campaign)
    response = jsonify({'message': 'Campaign created successfully!'}), 201
    return response

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

@app.route('/api/campaigns/<int:campaign_id>/players', methods=['POST'], endpoint='add_player')
@jwt_required()
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

@app.route('/api/campaigns/<int:campaign_id>/masters', methods=['POST'], endpoint='add_master')
@jwt_required()
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

@app.route('/api/campaigns/<int:campaign_id>/masters', methods=['DELETE'], endpoint='remove_master')
@jwt_required()
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

@app.route('/api/campaigns/<int:campaign_id>/players', methods=['DELETE'], endpoint='remove_player')
@jwt_required()
def remove_player(campaign_id):
    data = request.json
    campaign = next((campaign for campaign in campaigns if campaign.campaign_id == campaign_id), None)
    if campaign:
        campaign.players.remove(data['player_id'])
        return jsonify(campaign.__dict__), 200
    else:
        return jsonify({'error': 'Campaign not found'}), 404

# --------------------------------------------    Players         ------------------------------------------------------------
@app.route('/api/players', methods=['POST'], endpoint='create_player')
@jwt_required()
def create_player():
    data = request.json
    new_player = Player(data['player_id'], data['name'], data['campaign_id'])
    players.append(new_player)
    return jsonify(new_player.__dict__), 201

# Additional routes for adding/removing gold, items, etc.
@app.route('/api/players/<int:player_id>/gold', methods=['POST'], endpoint='add_gold')  
@jwt_required()
def add_gold(player_id):
    data = request.json
    player = next((player for player in players if player.player_id == player_id), None)
    if player:
        player.add_gold(data['amount'])
        return jsonify(player.__dict__), 200
    else:
        return jsonify({'error': 'Player not found'}), 404

@app.route('/api/players/<int:player_id>/gold', methods=['DELETE'], endpoint='remove_gold')
@jwt_required()
def remove_gold(player_id):
    data = request.json
    player = next((player for player in players if player.player_id == player_id), None)
    if player:
        player.remove_gold(data['amount'])
        return jsonify(player.__dict__), 200
    else:
        return jsonify({'error': 'Player not found'}), 404

@app.route('/api/players/<int:player_id>/items', methods=['POST'], endpoint='add_item')
@jwt_required()
def add_item(player_id):
    data = request.json
    player = next((player for player in players if player.player_id == player_id), None)
    if player:
        player.add_item(data['item_id'])
        return jsonify(player.__dict__), 200
    else:
        return jsonify({'error': 'Player not found'}), 404

@app.route('/api/players/<int:player_id>/items', methods=['DELETE'], endpoint='remove_item')
@jwt_required()
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

# --------------------------------------------    Items         ------------------------------------------------------------

@app.route('/api/items/<int:item_id>', methods=['GET'])
def get_item(item_id):
    item = next((item for item in items if item.item_id == item_id), None)
    if item:
        return jsonify(item.__dict__), 200
    else:
        return jsonify({'error': 'Item not found'}), 404

@app.route('/api/items/create', methods=['POST'], endpoint='create_new_item')
@jwt_required()
def create_new_item():
    if current_user.username not in ['admin', 'master']:
        return jsonify({'error': 'Insufficient permissions'}), 403
    
    # Create the item
    item = Item(name=request.json.get('name'))
    items.append(item)
    #db.session.add(item)
    #db.session.commit()

    return jsonify({'message': 'Item created successfully!'}), 201

@app.route('/api/items/list', methods=['GET'])
def get_items():
    current_items = []
    for item in items:
        current_items.append(item.__dict__)
    return jsonify(current_items), 200
@app.route('/api/items/<int:item_id>/update', methods=['PUT'], endpoint='update_item')
@jwt_required()
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

@app.route('/api/items/<int:item_id>', methods=['DELETE'], endpoint='delete_item')
@jwt_required()
def delete_item(item_id):
    item = next((item for item in items if item.item_id == item_id), None)
    if item:
        items.remove(item)
        return jsonify({'message': 'Item deleted'}), 200
    else:
        return jsonify({'error': 'Item not found'}), 404

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
