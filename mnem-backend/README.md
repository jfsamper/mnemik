# Mnemik Backend
Backend server for MNEMIK.
## Requirements
1. Install Flask:
Install Flask using pip:
### `pip install Flask`
2. Install the required packages:
### `pip install flask_login flask_cors flask_session`
## Deploy Backend Server
Run backend server:
### `python src/mnem.py`
This will start the development server on [http://localhost:5000](http://localhost:5000) by default.
## Connect Your Frontend to the Backend:
Update your frontend API calls to point to the routes defined in your Flask application. For example:

### `fetch('http://localhost:5000/api/campaigns')`