import { useEffect, useState } from "react";

import KnowledgeGraphCard from "../components/KnowledgeGraphCard";

import { getEquipmentGraph } from "../services/graphService";

function Equipment() {

    const [graph, setGraph] = useState(null);

    const [equipment, setEquipment] = useState("PUMP-P103");

    const [loading, setLoading] = useState(true);

    useEffect(() => {

        loadGraph();

    }, []);

    async function loadGraph() {

        try {

            const data = await getEquipmentGraph(

                equipment

            );

            setGraph(data);

        }

        catch (error) {

            console.log(error);

        }

        finally {

            setLoading(false);

        }

    }

    return (

        <div className="p-8">

            <div className="flex justify-between items-center mb-8">

                <h1 className="text-4xl font-bold">

                    Equipment Knowledge Graph

                </h1>

                <select

                    value={equipment}

                    onChange={(e) => {

                        setEquipment(e.target.value);

                        getEquipmentGraph(

                            e.target.value

                        ).then(setGraph);

                    }}

                    className="border rounded-lg p-2"

                >

                    <option>PUMP-P101</option>

                    <option>PUMP-P102</option>

                    <option>PUMP-P103</option>

                    <option>COMP-A201</option>

                </select>

            </div>

            {

                loading ?

                    (

                        <h2>

                            Loading Knowledge Graph...

                        </h2>

                    )

                    :

                    (

                        <KnowledgeGraphCard

                            graph={graph}

                        />

                    )

            }

        </div>

    );

}

export default Equipment;