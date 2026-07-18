import api from "./api";

export async function askMira(question, equipmentTag = "") {
    try {
        const response = await api.post("/ask", {
            question,
            equipment_tag: equipmentTag,
        });

        return response.data;
    } catch (error) {
        console.error(error);

        throw new Error(
            error.response?.data?.detail ||
            "Unable to contact MIRA backend."
        );
    }
}