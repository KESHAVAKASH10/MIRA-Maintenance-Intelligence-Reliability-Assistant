import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";

import PageHeader from "../components/PageHeader";
import EquipmentHeader from "../components/EquipmentHeader";
import EquipmentHealthCard from "../components/EquipmentHealthCard";
import KeyFindingsCard from "../components/KeyFindingsCard";
import RecommendationsCard from "../components/RecommendationsCard";
import DocumentSection from "../components/DocumentSection";

import extractRecommendations from "../utils/extractRecommendations";
import { getEquipment } from "../services/assetService";
import KnowledgeGraphCard from "../components/KnowledgeGraphCard";
import { getEquipmentGraph } from "../services/graphService";

function Equipment360() {
    const { tag } = useParams();

    const [equipment, setEquipment] = useState(null);
    const [graph, setGraph] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState("");

    useEffect(() => {
        fetchEquipment();
    }, [tag]);

    const fetchEquipment = async () => {
        try {
            const data = await getEquipment(tag);
            setEquipment(data);

            const graphData = await getEquipmentGraph(tag);
            setGraph(graphData);
        } catch (err) {
            setError("Unable to load equipment intelligence.");
        } finally {
            setLoading(false);
        }
    };

    if (loading) {
        return (
            <>
                <PageHeader
                    title="Equipment 360"
                    subtitle="Loading Equipment Intelligence..."
                />

                <div className="bg-white rounded-xl shadow p-10 text-center">
                    Loading equipment data...
                </div>
            </>
        );
    }

    if (error) {
        return (
            <>
                <PageHeader
                    title="Equipment 360"
                    subtitle="Industrial Intelligence"
                />

                <div className="bg-red-50 border border-red-200 rounded-xl p-6 text-red-600">
                    {error}
                </div>
            </>
        );
    }

    const recommendations = extractRecommendations(
        equipment.intelligence_summary
    );

    // Documents from Knowledge Graph
    const docs = graph?.documents || [];

    const workOrders = docs.filter((d) =>
        (d.label || "").includes("WO_")
    );

    const incidents = docs.filter(
        (d) =>
            (d.label || "").includes("INC_") ||
            (d.label || "").includes("Near_Miss") ||
            (d.label || "").includes("RCA_")
    );

    const inspections = docs.filter(
        (d) =>
            (d.label || "").includes("Inspection") ||
            (d.label || "").includes("Shift")
    );

    const regulations = docs.filter(
        (d) =>
            (d.label || "").includes("OISD") ||
            (d.label || "").includes("Compliance") ||
            (d.label || "").includes("Factories")
    );

    return (
        <>
            <PageHeader
                title="Equipment 360"
                subtitle="Complete Industrial Asset Intelligence"
            />

            <EquipmentHeader
                equipmentTag={equipment.equipment_tag}
                totalDocuments={equipment.total_documents_found}
            />

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
                <EquipmentHealthCard
                    status="Warning"
                    summary={equipment.intelligence_summary}
                />

                <KeyFindingsCard
                    workOrders={workOrders}
                    incidents={incidents}
                    inspections={inspections}
                    regulations={regulations}
                />
            </div>

            <RecommendationsCard
                recommendations={recommendations}
            />

            <div className="mt-6">
                <KnowledgeGraphCard
                    graph={graph}
                />
            </div>

            <div className="space-y-6 mt-6">
                <DocumentSection
                    title="Work Orders"
                    icon="📄"
                    documents={workOrders}
                />

                <DocumentSection
                    title="Incident Reports"
                    icon="⚠"
                    documents={incidents}
                />

                <DocumentSection
                    title="Inspection Records"
                    icon="🔍"
                    documents={inspections}
                />

                <DocumentSection
                    title="Standards & Regulations"
                    icon="📚"
                    documents={regulations}
                />
            </div>
        </>
    );
}

export default Equipment360;