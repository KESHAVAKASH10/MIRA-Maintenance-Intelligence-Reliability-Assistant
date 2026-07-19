function EquipmentHeader({ equipmentTag, totalDocuments }) {
    return (
        <div className="bg-white rounded-xl shadow p-6 mb-6">

            <div className="flex justify-between items-center">

                <div>

                    <h2 className="text-3xl font-bold">
                        {equipmentTag}
                    </h2>

                    <p className="text-slate-500 mt-2">
                        AI Generated Equipment Intelligence
                    </p>

                </div>

                <div className="text-right">

                    <div className="inline-block bg-yellow-100 text-yellow-700 px-4 py-2 rounded-full font-semibold">
                        Warning
                    </div>

                    <p className="text-slate-500 mt-3">
                        {totalDocuments} Related Documents
                    </p>

                </div>

            </div>

        </div>
    );
}

export default EquipmentHeader;