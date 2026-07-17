function StatusCard({ title, value, color }) {
    return (
        <div className="rounded-xl bg-white p-5 shadow-sm border">
            <p className="text-sm text-slate-500">
                {title}
            </p>

            <h2 className={`mt-3 text-3xl font-bold ${color}`}>
                {value}
            </h2>
        </div>
    );
}

export default StatusCard;