import api from "./api";

export async function getEquipment(tag) {
    const { data } = await api.get(`/equipment/${tag}`);
    return data;
}