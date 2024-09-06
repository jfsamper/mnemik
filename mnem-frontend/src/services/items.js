import { axiosInstance } from "./auth";

const baseUrl = "http://localhost:5000/api";

export const getItems = async () => {
  try {
    const response = await axiosInstance.get(`${baseUrl}/items`);
    return response.data;
  } catch (error) {
    console.error(error);
  }
};

export const getItem = async (id) => {
    const response = await axiosInstance.get(`${baseUrl}/items/${id}`);
    return response.data;
}

export const createItem = async (itemData) => {
  
  const response = await axiosInstance.post(`${baseUrl}/items/create/`, {
    params: {
      item_id: itemData.item_id,
      name: itemData.name,
      weight: itemData.weight,
      price: itemData.price,
    },
    
  })

  return response.json();
};

export const deleteItem = async (id) => {
    const response = await axiosInstance.delete(`${baseUrl}/items/${id}`);
    return response.data;
}

export const updateItem = async (id, item) => {
    const response = await axiosInstance.put(`${baseUrl}/items/${id}`, item);
    return response.data;
}
