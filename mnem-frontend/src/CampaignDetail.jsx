import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { getCampaign } from './services/campaigns';

function CampaignDetail() {
  const [campaign, setCampaign] = useState(null);
  const { campaignId } = useParams();

  useEffect(() => {
    // Fetch the details of the campaign based on campaignId
    const fetchCampaign = async () => {
      setCampaign(await getCampaign(campaignId));
    };
    fetchCampaign();
  }, [campaignId]);

  return (
    <div>
      {campaign ? (
        <>
          <h2>{campaign.name}</h2>
          {/* Display other campaign details */}
          <Link to={`/campaigns/${campaign.id}/edit`}>Edit Campaign</Link>
        </>
      ) : (
        <p>Loading...</p>
      )}
    </div>
  );
}

export default CampaignDetail;
