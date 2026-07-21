function RecommendationsCard({ recommendations }) {

    if (!recommendations || recommendations.length === 0) {
        return null;
    }

    return (

        <div className="bg-white rounded-xl shadow p-6">

            <h2 className="text-xl font-semibold mb-5">
                🛠 AI Recommendations
            </h2>

            <div className="space-y-3">

                {recommendations.map((item, index) => (

                    <div
                        key={index}
                        className="flex gap-3 border rounded-lg p-3"
                    >

                        <span className="text-green-600 font-bold">
                            ✓
                        </span>

                        <p className="text-slate-700">
                            {item}
                        </p>

                    </div>

                ))}

            </div>

        </div>

    );
}

export default RecommendationsCard;