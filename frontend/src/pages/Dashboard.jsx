import PageHeader from "../components/PageHeader";
import PlantStatusBanner from "../components/PlantStatusBanner";
import StatusCard from "../components/StatusCard";
import CriticalAssetCard from "../components/CriticalAssetCard";
import InsightCard from "../components/InsightCard";
import QuickActionCard from "../components/QuickActionCard";

import { dashboardData } from "../data/dashboardData";

function Dashboard() {
    return (
        <>
            <PageHeader
                title="Industrial Operations Dashboard"
                subtitle="Maintenance Intelligence & Reliability Assistant"
            />

            <PlantStatusBanner plant={dashboardData.plant} />

            <div className="grid grid-cols-4 gap-6 mb-8">
                {dashboardData.summary.map((card) => (
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