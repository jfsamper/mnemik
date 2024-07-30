import axios from 'axios';

const baseUrl = 'http://localhost:5000/api';

export const getCampaigns = async () => {
  const response = await axios.get(`${baseUrl}/campaigns/list`);
  return response.data;
};

export const getCampaign = async (id) => {
  const response = await axios.get(`${baseUrl}/campaigns/${id}`);
  return response.data;
};

export const createCampaign = async (campaign) => {
  const response = await axios.post(`${baseUrl}/campaigns`, campaign, {
    headers: {
      'Content-Type': 'application/json',
    },
  });
  return response.data;
};

export const updateCampaign = async (id, campaign) => {
  const response = await axios.put(`${baseUrl}/campaigns/${id}`, campaign);
  return response.data;
};

export const deleteCampaign = async (id) => {
  const response = await axios.delete(`${baseUrl}/campaigns/${id}`);
  return response.data;
};
