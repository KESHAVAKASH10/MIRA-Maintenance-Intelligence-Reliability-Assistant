function EquipmentHealthCard({ status, summary }) {
    const color =
        status === "Healthy"
            ? "bg-green-100 text-green-700"
            : status === "Warning"
                ? "bg-yellow-100 text-yellow-700"
                : "bg-red-100 text-red-700";

    return (
        <div className="bg-white rounded-xl shadow p-6">

            <div className="flex justify-between items-center mb-4">

                <h2 className="text-xl font-semibold">
                    🧠 AI Health Summary
                </h2>

                <span className={`px-4 py-1 rounded-full font-semibold ${color}`}>
                    {status}
                </span>

            </div>

            <p className="text-slate-700 leading-7 whitespace-pre-wrap">
                {summary}
            </p>

        </div>
    );
}

export default EquipmentHealthCard;