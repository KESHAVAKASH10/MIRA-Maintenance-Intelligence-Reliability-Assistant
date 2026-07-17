function AssetSummaryCard({ asset }) {
    return (
        <div className="bg-white border rounded-xl shadow-sm p-5 hover:shadow-md transition">
            <div className="flex justify-between items-center">
                <div>
                    <h3 className="text-lg font-semibold text-slate-900">
                        {asset.id}
                    </h3>

                    <p className="text-sm text-slate-500 mt-1">
                        {asset.location}
                    </p>
                </div>

                <span
                    className={`font-semibold ${asset.status === "Healthy"
                            ? "text-green-600"
                            : asset.status === "Needs Attention"
                                ? "text-yellow-600"
                                : "text-red-600"
                        }`}
                >
                    {asset.status}
                </span>
            </div>

            <div className="mt-4">
                <p className="text-slate-600">
                    {asset.description}
                </p>
            </div>

            <button className="mt-5 text-blue-600 font-medium hover:underline">
                View Asset →
            </button>
        </div>
    );
}

export default AssetSummaryCard;