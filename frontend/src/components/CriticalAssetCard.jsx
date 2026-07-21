function CriticalAssetCard({ asset }) {
    return (
        <div className="bg-white rounded-xl border p-5 shadow-sm">
            <div className="flex justify-between items-center">
                <h3 className="font-semibold text-slate-900">
                    {asset.id}
                </h3>

                <span className="text-red-600 font-semibold">
                    {asset.severity}
                </span>
            </div>

            <p className="mt-3 text-slate-600">
                {asset.issue}
            </p>

            <p className="mt-4 text-sm text-slate-500">
                Confidence: {asset.confidence}%
            </p>

            <button className="mt-5 text-blue-600 font-medium hover:underline">
                Open Asset →
            </button>
        </div>
    );
}

export default CriticalAssetCard;