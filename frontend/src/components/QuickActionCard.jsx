function QuickActionCard({ action }) {
    return (
        <button className="bg-white border rounded-xl p-5 text-left shadow-sm hover:shadow-md transition">
            <h3 className="font-semibold text-slate-900">
                {action.title}
            </h3>

            <p className="mt-2 text-sm text-slate-500">
                {action.description}
            </p>
        </button>
    );
}

export default QuickActionCard;