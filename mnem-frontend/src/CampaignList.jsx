import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { getCampaigns, getCampaign, createCampaign, updateCampaign, deleteCampaign } from './services/campaigns';

function CampaignList() {
  const [campaigns, setCampaigns] = useState([
    {id: 1, name: 'Arrakis'},
  ]);

  useEffect(() => {
    const fetchCampaigns = async () => {
      const data = await getCampaigns();
      setCampaigns(data);
    };

    fetchCampaigns();
  }, []);

  return (
      <div>
        <h2>Campaigns</h2>
        <ul>
          {campaigns.map((campaign) => (
            <li key={campaign.id}>
              <Link to={`/campaigns/${campaign.id}`}>{campaign.name}</Link>
            </li>
          ))}
        </ul>
        <br/>

        <Link to="/campaigns/new">Create New Campaign</Link>
      </div>
  );
}

export default CampaignList;
