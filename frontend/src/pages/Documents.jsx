import { useEffect, useState } from "react";

import DocumentCard from "../components/DocumentCard";

import {

    getDocuments,

    searchDocuments

}

    from "../services/documentService";

function Documents() {

    const [documents, setDocuments] = useState([]);

    const [loading, setLoading] = useState(true);

    const [query, setQuery] = useState("");

    useEffect(() => {

        loadDocuments();

    }, []);

    async function loadDocuments() {

        try {

            const data = await getDocuments();

            setDocuments(data);

        }

        catch (error) {

            console.log(error);

        }

        finally {

            setLoading(false);

        }

    }

    async function handleSearch(e) {

        const value = e.target.value;

        setQuery(value);

        if (value === "") {

            loadDocuments();

            return;

        }

        const data = await searchDocuments(value);

        setDocuments(data);

    }

    return (

        <div className="p-8">

            <h1 className="text-4xl font-bold mb-6">

                Industrial Documents

            </h1>

            <input

                value={query}

                onChange={handleSearch}

                placeholder="Search by filename, equipment or type..."

                className="border rounded-lg p-3 w-full mb-8"

            />

            {

                loading ?

                    (

                        <h2>

                            Loading...

                        </h2>

                    )

                    :

                    (

                        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">

                            {

                                documents.map((doc, index) => (

                                    <DocumentCard

                                        key={index}

                                        document={doc}

                                    />

                                ))

                            }

                        </div>

                    )

            }

        </div>

    );

}

export default Documents;