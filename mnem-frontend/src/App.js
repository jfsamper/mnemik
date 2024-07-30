import {
  BrowserRouter as Router,
  Routes,
  Route,
  Link
} from 'react-router-dom';
import logo from './logo.svg';
import ItemList from './ItemList';
import ItemDetail from './ItemDetail';
import CampaignList from './CampaignList';
import CampaignDetail from './CampaignDetail';
import CreateCampaign from './CreateCampaign';
import CreateItem from './CreateItem';
import Login from './Login';
// Import other components you want to route to

function App() {
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
}

function Home() {
  return (
    <div>
      <h2>Home</h2>
    </div>
  );
}

function NotFound() {
  return <h1>Not Found</h1>;
}

export default App;
