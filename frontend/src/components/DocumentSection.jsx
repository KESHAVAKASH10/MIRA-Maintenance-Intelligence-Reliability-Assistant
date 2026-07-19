function DocumentSection({ title, icon, documents }) {

    return (
        <div className="bg-white rounded-xl shadow p-6">

            <h3 className="text-xl font-semibold mb-4">
                {icon} {title}
            </h3>

            {documents.length === 0 ? (
                <p className="text-slate-500">
                    No records found.
                </p>
            ) : (
                <div className="space-y-4">

                    {documents.map((doc, index) => (

                        <div
                            key={index}
                            className="border rounded-lg p-4 hover:bg-slate-50 transition"
                        >

                            <h4 className="font-semibold">
                                {doc.filename}
                            </h4>

                            <p className="text-sm text-slate-500 mb-2">
                                Page {doc.page}
                            </p>

                            <p className="text-slate-700">
                                {doc.preview}
                            </p>

                        </div>

                    ))}

                </div>
            )}

        </div>
    );
}

export default DocumentSection;