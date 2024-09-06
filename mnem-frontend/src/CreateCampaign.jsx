import React, { useState } from 'react';
import { axiosInstance } from './services/auth';

function CreateCampaign() {
  const [name, setName] = useState('');
  const [campaign_id, setCampaign_id] = useState('');
  const [admin_id, setAdmin_id] = useState('');

const handleSubmit = async (event) => {
  event.preventDefault();
  try {
      const campaignData = {
        campaign_id: parseInt(campaign_id),
        name: name,
        admin_id: parseInt(0), // Replace with the actual admin/master ID
      };
      const response = await axiosInstance.post('/api/campaigns/create', campaignData);
      console.log(response); //remove me - test data !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

      if (response.status === 201) {
        // Handle success case, e.g. show a success message or redirect to a new page
        alert('Campaign created successfully!'); // Show a success message
      } else {
        // Handle error case, e.g. show an error message
        console.error('Error creating campaign:', response.data.error);
      }
  } catch (error) {
    console.error(error);
  }
};

  return (
    <div>
      <h2>Create Campaign</h2>
      <form onSubmit={handleSubmit}>
        <label>
          Name: 
          <input type="text" value={name} onChange={(e) => setName(e.target.value)} />
        </label>
        <br/>
        <label>
          Campaign ID: 
          <input type="number" value={campaign_id} onChange={(e) => setCampaign_id(e.target.value)} />
        </label>
        <br/>
        <label>
          Admin ID: 
          <input type="number" value={admin_id} onChange={(e) => setAdmin_id(e.target.value)} />
        </label>
        {/* Add other form fields as needed */}
        <br/>
        <button type="submit">Create Campaign</button>
      </form>
    </div>
  );
}

export default CreateCampaign;
