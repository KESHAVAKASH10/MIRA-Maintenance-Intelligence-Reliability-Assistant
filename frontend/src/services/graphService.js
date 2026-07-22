import axios from "axios";

const API = "http://127.0.0.1:8000";

export const getEquipmentGraph = async (equipment) => {

    const response = await axios.get(

        `${API}/graph/equipment/${equipment}`

    );

    return response.data;

};

export const getGraphStats = async () => {

    const response = await axios.get(

        `${API}/graph/stats`

    );

    return response.data;

};