import axios from "axios";

const API = "http://127.0.0.1:8000";

export const getDocuments = async () => {
    const response = await axios.get(`${API}/documents`);
    return response.data;
};

export const searchDocuments = async (query) => {
    const response = await axios.get(`${API}/documents/search/${query}`);
    return response.data;
};

export const getDocument = async (filename) => {
    const response = await axios.get(`${API}/documents/${filename}`);
    return response.data;
};