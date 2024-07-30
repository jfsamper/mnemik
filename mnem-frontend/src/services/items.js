import axios from "axios";

const baseUrl = "http://localhost:5000/api";

export const getItems = async () => {
    const response = await axios.get(`${baseUrl}/items/list`);
    return response.data;
}

export const getItem = async (id) => {
    const response = await axios.get(`${baseUrl}/items/${id}`);
    return response.data;
}

export const createItem = async (item) => {
    const response = await axios.post(`${baseUrl}/items`, item, {
        headers: {
            "Content-Type": "application/json",
        },
    });
    return response.data;
}

export const deleteItem = async (id) => {
    const response = await axios.delete(`${baseUrl}/items/${id}`);
    return response.data;
}

export const updateItem = async (id, item) => {
    const response = await axios.put(`${baseUrl}/items/${id}`, item);
    return response.data;
}
