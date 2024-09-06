import React, { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import { getItems } from './services/items';

function ItemList() {
  const [items, setItems] = useState({id: 0, name: 'Test Item', price: 100, weight: 1});

  useEffect(() => {
    const fetchItems = async () => {
      const data = await getItems();
      setItems(data);
    }
    fetchItems()
  }, []);

  return (
    <div>
      <h2>Available Items</h2>
      {items && items.length > 0 ? (
        <ul>
          {items.map((item) => (
            <li key={item.id}>
              <Link to={`/items/${item.id}`}>{item.name} - 
              {item.price} Gold - {item.weight} lbs.
              </Link>
            </li>
          ))}
        </ul>
      ) : (
        <p>Loading items...</p>
      )}
      
      <Link to="/items/new">Create New Item</Link>
    </div>
  )};


export default ItemList;
