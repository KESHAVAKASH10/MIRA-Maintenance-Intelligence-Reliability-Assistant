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

function Equipment360() {

    const { tag } = useParams();

    const [equipment, setEquipment] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState("");

    useEffect(() => {
        fetchEquipment();
    }, [tag]);

    const fetchEquipment = async () => {

        try {

            const data = await getEquipment(tag);

            setEquipment(data);

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
                    workOrders={equipment.work_orders}
                    incidents={equipment.incidents}
                    inspections={equipment.inspections}
                    regulations={equipment.regulations}
                />

            </div>

            <RecommendationsCard
                recommendations={recommendations}
            />

            <div className="space-y-6 mt-6">

                <DocumentSection
                    title="Work Orders"
                    icon="📄"
                    documents={equipment.work_orders}
                />

                <DocumentSection
                    title="Incident Reports"
                    icon="⚠"
                    documents={equipment.incidents}
                />

                <DocumentSection
                    title="Inspection Records"
                    icon="🔍"
                    documents={equipment.inspections}
                />

                <DocumentSection
                    title="Standards & Regulations"
                    icon="📚"
                    documents={equipment.regulations}
                />

            </div>

        </>

    );

}

export default Equipment360;