export const dashboardData = {
    plant: {
        name: "Axis Manufacturing Plant",
        status: "Operational",
        lastUpdated: "2 mins ago",
        criticalAlerts: 3,
        workOrders: 12,
    },

    summary: [
        {
            title: "Assets Monitored",
            value: "148",
            color: "text-blue-600",
        },
        {
            title: "Critical Assets",
            value: "3",
            color: "text-red-600",
        },
        {
            title: "Open Work Orders",
            value: "12",
            color: "text-orange-600",
        },
        {
            title: "Compliance Score",
            value: "96%",
            color: "text-green-600",
        },
    ],

    criticalAssets: [
        {
            id: "PUMP-P103",
            issue: "Bearing temperature high",
            confidence: 94,
            severity: "High",
        },
        {
            id: "COMP-A201",
            issue: "Lubrication overdue",
            confidence: 90,
            severity: "Medium",
        },
    ],

    insights: [
        "Bearing failures increased by 23% this month.",
        "Similar failure detected in Area B.",
        "Lubrication overdue on 3 pumps.",
    ],

    quickActions: [
        {
            title: "Open Asset 360",
            description: "View complete asset history and health.",
        },
        {
            title: "Ask Industrial Copilot",
            description: "Get AI-powered maintenance assistance.",
        },
        {
            title: "Browse Documents",
            description: "Search manuals, SOPs and standards.",
        },
        {
            title: "Compliance Dashboard",
            description: "Review audit readiness and compliance.",
        },
    ],
};