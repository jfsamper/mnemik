import {
  BrowserRouter as Router,
  Routes,
  Route,
  Link
} from 'react-router-dom';
import { useState, useEffect } from 'react';
import logo from './logo.svg';
import ItemList from './ItemList';
import ItemDetail from './ItemDetail';
import CreateItem from './CreateItem';
import CampaignList from './CampaignList';
import CampaignDetail from './CampaignDetail';
import CreateCampaign from './CreateCampaign';
import Login from './Login';
// Import other components you want to route to
import { isAuthenticated } from './services/auth';

const App = () => {
  const [loggedIn, setLoggedIn] = useState(false);
  const handleLogin = async () => {
    const success = await isAuthenticated();
    if (success) {
      setLoggedIn(true);
    }
  };

  return (
    <Router>
      <div className="App">
      <header className="App-header">
      <br/> <a href='/'><img src={logo} height="40vmin" className="App-logo" alt="logo" /></a>
      <br/> <h1><b>M</b>nemik <b>I</b>nventory <b>K</b>eeper</h1>
      </header>
        <nav>
          <ul>
            <li>
              <Link to="/">Home</Link>
            </li>
            <li>
              <Link to="/items">Items</Link>
            </li>
            <li>
              <Link to="/campaigns">Campaigns</Link>
            </li>
            <li>
              <Link to="/login">Login</Link>
            </li>
            
            {/* Add other navigation links here */}
          </ul>
        </nav>
        {/* A <Routes> looks through its children <Route>s and
            renders the first one that matches the current URL. */}
        <Routes>
          <Route path="/items" element={<ItemList />} />
          <Route path="/items/*" element={<ItemDetail />} />
          <Route path="/items/new" element={<CreateItem />} />
          <Route path="/campaigns" element={<CampaignList />}  />
          <Route path="/campaigns/*" element={<CampaignDetail />} />
          <Route path="/campaigns/new" element={<CreateCampaign />} />
          <Route path="/login" element={<Login />} />
          <Route component={NotFound} />
          <Route path="/" element={<Home />} />
        </Routes>
      </div>
    </Router>
  );
};

function Home() {
  const [username, setUsername] = useState('');
  useEffect(() => {
    const storedUsername = localStorage.getItem('username');
    if (storedUsername) {
      setUsername(storedUsername);
    }
  }, []);
  return (
    <div>
      <h2>Home</h2>
      <p>Welcome to Mnemik</p>
      {!username && <p>Welcome Guest. To login please <Link to="/login">click here</Link>.</p>} 
      {username && <p>You are logged in as: {username}.</p>}
    </div>
  );
}

function NotFound() {
  return <h1>Not Found</h1>;
}

export default App;
