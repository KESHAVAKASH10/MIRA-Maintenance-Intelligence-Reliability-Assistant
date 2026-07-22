function KnowledgeGraphCard({ graph }) {
    if (!graph) {
        return null;
    }

    const documents = graph.documents || [];

    const workOrders = documents.filter(
        (doc) =>
            doc.filename?.toLowerCase().includes("wo") ||
            doc.filename?.toLowerCase().includes("work_order")
    );

    const incidents = documents.filter(
        (doc) =>
            doc.filename?.toLowerCase().includes("incident") ||
            doc.filename?.toLowerCase().includes("near") ||
            doc.filename?.toLowerCase().includes("rca")
    );

    const inspections = documents.filter(
        (doc) =>
            doc.filename?.toLowerCase().includes("inspection") ||
            doc.filename?.toLowerCase().includes("checklist") ||
            doc.filename?.toLowerCase().includes("handover")
    );

    const regulations = documents.filter(
        (doc) =>
            doc.filename?.toLowerCase().includes("oisd") ||
            doc.filename?.toLowerCase().includes("factories") ||
            doc.filename?.toLowerCase().includes("audit")
    );

    return (
        <div className="bg-white rounded-xl shadow-lg border p-6 mt-6">
            <h2 className="text-2xl font-bold mb-6">
                Knowledge Graph
            </h2>

            <div className="bg-slate-50 rounded-lg p-5 border">
                <div className="flex items-center gap-3">
                    <div className="w-12 h-12 rounded-full bg-blue-600 text-white flex items-center justify-center font-bold">
                        ⚙
                    </div>

                    <div>
                        <h3 className="font-bold text-lg">
                            {graph.equipment?.equipment_tag ||
                                graph.equipment?.tag ||
                                graph.equipment?.id ||
                                "Equipment"}
                        </h3>

                        <p className="text-slate-500">
                            Industrial Asset
                        </p>
                    </div>
                </div>
            </div>

            <div className="grid grid-cols-2 gap-5 mt-6">
                <div className="border rounded-lg p-4">
                    <h3 className="font-semibold mb-3">
                        📄 Work Orders
                    </h3>

                    {workOrders.length === 0 ? (
                        <p className="text-slate-400">
                            None
                        </p>
                    ) : (
                        workOrders.map((doc, i) => (
                            <div
                                key={i}
                                className="text-sm py-1"
                            >
                                • {doc.filename || doc.label}
                            </div>
                        ))
                    )}
                </div>

                <div className="border rounded-lg p-4">
                    <h3 className="font-semibold mb-3">
                        ⚠ Incidents
                    </h3>

                    {incidents.length === 0 ? (
                        <p className="text-slate-400">
                            None
                        </p>
                    ) : (
                        incidents.map((doc, i) => (
                            <div
                                key={i}
                                className="text-sm py-1"
                            >
                                • {doc.filename || doc.label}
                            </div>
                        ))
                    )}
                </div>

                <div className="border rounded-lg p-4">
                    <h3 className="font-semibold mb-3">
                        🔍 Inspections
                    </h3>

                    {inspections.length === 0 ? (
                        <p className="text-slate-400">
                            None
                        </p>
                    ) : (
                        inspections.map((doc, i) => (
                            <div
                                key={i}
                                className="text-sm py-1"
                            >
                                • {doc.filename || doc.label}
                            </div>
                        ))
                    )}
                </div>

                <div className="border rounded-lg p-4">
                    <h3 className="font-semibold mb-3">
                        📚 Regulations
                    </h3>

                    {regulations.length === 0 ? (
                        <p className="text-slate-400">
                            None
                        </p>
                    ) : (
                        regulations.map((doc, i) => (
                            <div
                                key={i}
                                className="text-sm py-1"
                            >
                                • {doc.filename || doc.label}
                            </div>
                        ))
                    )}
                </div>
            </div>

            <div className="mt-6">
                <h3 className="font-semibold mb-3">
                    Connected Documents
                </h3>

                <div className="space-y-2">
                    {documents.map((doc, index) => (
                        <div
                            key={index}
                            className="flex items-center justify-between border rounded-lg p-3"
                        >
                            <span>
                                📄 {doc.filename || doc.label}
                            </span>

                            <span className="text-xs bg-blue-100 text-blue-700 px-2 py-1 rounded">
                                {doc.doc_type || doc.type || "Document"}
                            </span>
                        </div>
                    ))}
                </div>
            </div>
        </div>
    );
}

export default KnowledgeGraphCard;
