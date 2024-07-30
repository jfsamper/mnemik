import React, { useState, useSelector } from 'react';
import { createItem } from './services/items';

function CreateItem() {
    const [name, setName] = useState('');
    const [ID, setID] = useState(0);
    const [weight, setWeight] = useState(0);
    const [price, setPrice] = useState(0);
    const handleSubmit = async (event) => {
        event.preventDefault();
        // Submit the new item to your backend
        const newItem = { 
            item_id: parseInt(ID),
            name: name, 
            weight: weight, 
            price: price 
            };
        
        try {
            const response = await createItem(newItem);
            if (response.item_id) {
                alert('Item #' + response.item_id + ' created successfully!');
            } else {
                // Handle error case, e.g. show an error message
                alert('Unexpected error creating item:', response);
            }
            } catch (error) {
                if (error.response.data.error) {
                    // show error
                    alert(error.response.data.error);
                    // handle not logged in error
                    if (error.response.status === 401) {
                        // redirect to login page
                        window.location.href = '/login';
                    }
                } else if (error.response) {
                    alert(error.response.statusText);
                }
                console.error('Error creating item:', error);
            }
    };

    return (
        <div>
            <h2>Create Item</h2>
            <form onSubmit={handleSubmit}>
            <label>
                ID:
                <input type="number" value={ID} onChange={(e) => setID(e.target.value)} />
            </label>
            <br/>
            <label>
                Name:
                <input type="text" value={name} onChange={(e) => setName(e.target.value)} />
            </label>
            <br/>
            <label>
                Weight:
                <input type="number" value={weight} onChange={(e) => setWeight(e.target.value)} />
            </label>
            <br/>
            <label>
                Price:
                <input type="number" value={price} onChange={(e) => setPrice(e.target.value)} />
            </label>
            {/* Add other form fields as needed */}
            <button type="submit">Create Item</button>
            </form>
        </div>
    );
}

export default CreateItem;