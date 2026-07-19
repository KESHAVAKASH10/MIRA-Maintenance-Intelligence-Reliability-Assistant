import { useEffect, useState } from "react";

import PageHeader from "../components/PageHeader";
import PlantStatusBanner from "../components/PlantStatusBanner";
import StatusCard from "../components/StatusCard";
import CriticalAssetCard from "../components/CriticalAssetCard";
import InsightCard from "../components/InsightCard";
import QuickActionCard from "../components/QuickActionCard";

import { dashboardData } from "../data/dashboardData";
import { getDashboardStats } from "../services/dashboardService";

function Dashboard() {

    const [stats, setStats] = useState(null);

    useEffect(() => {

        async function loadStats() {
            try {
                const data = await getDashboardStats();
                setStats(data);
            } catch (err) {
                console.error(err);
            }
        }

        loadStats();

    }, []);

    const summary = [
        {
            title: "Documents Indexed",
            value: stats ? stats.total_documents : "...",
            color: "text-blue-600",
        },
        {
            title: "Knowledge Chunks",
            value: stats ? stats.total_chunks : "...",
            color: "text-purple-600",
        },
        {
            title: "Critical Assets",
            value: dashboardData.summary[1].value,
            color: "text-red-600",
        },
        {
            title: "System Status",
            value: stats
                ? ((stats.backend || "Unknown").charAt(0).toUpperCase() +
                    (stats.backend || "Unknown").slice(1))
                : "...",
            color: "text-green-600",
        },
    ];

    return (
        <>
            <PageHeader
                title="Industrial Operations Dashboard"
                subtitle="Maintenance Intelligence & Reliability Assistant"
            />

            <PlantStatusBanner plant={dashboardData.plant} />

            <div className="grid grid-cols-4 gap-6 mb-8">
                {summary.map((card) => (
                    <StatusCard
                        key={card.title}
                        title={card.title}
                        value={card.value}
                        color={card.color}
                    />
                ))}
            </div>

            <h2 className="text-2xl font-semibold mb-4">
                Critical Assets
            </h2>

            <div className="grid grid-cols-2 gap-6 mb-8">
                {dashboardData.criticalAssets.map((asset) => (
                    <CriticalAssetCard
                        key={asset.id}
                        asset={asset}
                    />
                ))}
            </div>

            <h2 className="text-2xl font-semibold mb-4">
                AI Insights
            </h2>

            <div className="space-y-4 mb-8">
                {dashboardData.insights.map((insight, index) => (
                    <InsightCard
                        key={index}
                        insight={insight}
                    />
                ))}
            </div>

            <h2 className="text-2xl font-semibold mb-4">
                Quick Actions
            </h2>

            <div className="grid grid-cols-2 gap-6">
                {dashboardData.quickActions.map((action) => (
                    <QuickActionCard
                        key={action.title}
                        action={action}
                    />
                ))}
            </div>
        </>
    );
}

export default Dashboard;