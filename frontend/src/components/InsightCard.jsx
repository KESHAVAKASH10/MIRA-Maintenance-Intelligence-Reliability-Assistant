function InsightCard({ insight }) {
    return (
        <div className="bg-white rounded-xl border p-4 shadow-sm">
            <p className="text-slate-700">
                {insight}
            </p>
        </div>
    );
}

export default InsightCard;