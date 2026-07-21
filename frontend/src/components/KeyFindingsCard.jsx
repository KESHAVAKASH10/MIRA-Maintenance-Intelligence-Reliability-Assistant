function KeyFindingsCard({
    workOrders,
    incidents,
    inspections,
    regulations,
}) {
    return (
        <div className="bg-white rounded-xl shadow p-6">

            <h2 className="text-xl font-semibold mb-5">
                📊 Key Findings
            </h2>

            <div className="grid grid-cols-2 gap-5">

                <div className="border rounded-lg p-4">
                    <p className="text-3xl font-bold text-blue-600">
                        {workOrders.length}
                    </p>
                    <p className="text-slate-600">
                        Work Orders
                    </p>
                </div>

                <div className="border rounded-lg p-4">
                    <p className="text-3xl font-bold text-red-600">
                        {incidents.length}
                    </p>
                    <p className="text-slate-600">
                        Incidents
                    </p>
                </div>

                <div className="border rounded-lg p-4">
                    <p className="text-3xl font-bold text-green-600">
                        {inspections.length}
                    </p>
                    <p className="text-slate-600">
                        Inspections
                    </p>
                </div>

                <div className="border rounded-lg p-4">
                    <p className="text-3xl font-bold text-purple-600">
                        {regulations.length}
                    </p>
                    <p className="text-slate-600">
                        Regulations
                    </p>
                </div>

            </div>

        </div>
    );
}

export default KeyFindingsCard;