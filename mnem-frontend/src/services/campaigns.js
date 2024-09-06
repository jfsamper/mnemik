import { axiosInstance, generateToken } from './auth';

const baseUrl = 'http://localhost:5000/api';

export const getCampaigns = async () => {
  try {
    const response = await axiosInstance.get(`${baseUrl}/campaigns/list`);
    return response.data;
  } catch (error) {
    console.error(error);
    throw error;
  }
};

export const getCampaign = async (id) => {
  const response = await axiosInstance.get(`${baseUrl}/campaigns/${id}`);
  return response.data;
};

export const createCampaign = async (campaignData) => {
  try {
    const token = localStorage.getItem('token');
    axiosInstance.defaults.headers.common['Authorization'] = `Bearer ${token}`;
    const response = await axiosInstance.post(`${baseUrl}/campaigns/create`, campaignData);
    return response;
  } catch (error) {
    console.error(error);
    throw error;
    }
};


export const updateCampaign = async (id, campaign) => {
  try {
    const token = localStorage.getItem('token');
    axiosInstance.defaults.headers.Authorization = `Bearer ${token}`;
    const response = await axiosInstance.put(`${baseUrl}/campaigns/${id}`, campaign);
    return response.data;
  } catch (error) {
    console.error(error);
    throw error;
  }
};

export const deleteCampaign = async (id) => {
  try {
    const token = localStorage.getItem('token');
    axiosInstance.defaults.headers.Authorization = `Bearer ${token}`;
    const response = await axiosInstance.delete(`${baseUrl}/campaigns/${id}`);
    return response.data;
  } catch (error) {
    console.error(error);
    throw error;
  }
};
