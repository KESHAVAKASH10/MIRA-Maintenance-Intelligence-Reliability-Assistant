function PlantStatusBanner({ plant }) {
    return (
        <div className="bg-white rounded-xl border shadow-sm p-6 mb-8">
            <div className="flex justify-between items-center">
                <div>
                    <h1 className="text-2xl font-bold text-slate-900">
                        {plant.name}
                    </h1>

                    <p className="text-green-600 font-semibold mt-2">
                        ● {plant.status}
                    </p>
                </div>

                <div className="text-right">
                    <p className="text-red-600 font-semibold">
                        {plant.criticalAlerts} Critical Alerts
                    </p>

                    <p className="text-orange-500 font-semibold mt-1">
                        {plant.workOrders} Open Work Orders
                    </p>

                    <p className="text-sm text-slate-500 mt-3">
                        Last Updated
                    </p>

                    <p className="font-medium">
                        {plant.lastUpdated}
                    </p>
                </div>
            </div>
        </div>
    );
}

export default PlantStatusBanner;