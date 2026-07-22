function DocumentCard({ document }) {

    return (

        <div className="bg-white rounded-xl shadow-md border p-5 hover:shadow-lg transition">

            <h2 className="text-xl font-semibold">

                {document.filename}

            </h2>

            <div className="mt-3 space-y-1 text-gray-700">

                <p>

                    <span className="font-semibold">

                        Type:

                    </span>

                    {" "}

                    {document.doc_type}

                </p>

                <p>

                    <span className="font-semibold">

                        Equipment:

                    </span>

                    {" "}

                    {document.equipment_tag}

                </p>

                <p>

                    <span className="font-semibold">

                        Pages:

                    </span>

                    {" "}

                    {document.pages}

                </p>

                <p>

                    <span className="font-semibold">

                        Chunks:

                    </span>

                    {" "}

                    {document.chunks}

                </p>

            </div>

        </div>

    );

}

export default DocumentCard;