import { useEffect, useState } from "react";
import PageHeader from "../components/PageHeader";

function Compliance() {

    const [selectedEquipment, setSelectedEquipment] = useState("PUMP-P103");

    const [data, setData] = useState(null);

    const [loading, setLoading] = useState(true);

    useEffect(() => {

        setLoading(true);

        fetch(`http://127.0.0.1:8000/compliance/${selectedEquipment}`)
            .then((res) => res.json())
            .then((json) => {

                setData(json);

                setLoading(false);

            });

    }, [selectedEquipment]);

    if (loading) {

        return (

            <>

                <PageHeader
                    title="Compliance Intelligence"
                    subtitle="Loading Industrial Compliance..."
                />

                <div className="bg-white rounded-xl shadow p-8">
                    Loading...
                </div>

            </>

        );

    }

    return (

        <>

            <PageHeader
                title="Compliance Intelligence"
                subtitle="AI Regulatory Assessment"
            />

            <div className="mb-6">

                <label className="block text-sm font-semibold mb-2">
                    Select Equipment
                </label>

                <select
                    value={selectedEquipment}
                    onChange={(e) => setSelectedEquipment(e.target.value)}
                    className="border rounded-lg px-4 py-2 w-64 bg-white"
                >

                    <option value="PUMP-P101">PUMP-P101</option>

                    <option value="PUMP-P102">PUMP-P102</option>

                    <option value="PUMP-P103">PUMP-P103</option>

                    <option value="COMP-A201">COMP-A201</option>

                </select>

            </div>

            <div className="grid grid-cols-3 gap-6 mb-6">

                <div className="bg-white rounded-xl shadow p-6">

                    <p className="text-slate-500">
                        Compliance Score
                    </p>

                    <h1 className="text-5xl font-bold text-green-600 mt-3">
                        {data.compliance_score}%
                    </h1>

                </div>

                <div className="bg-white rounded-xl shadow p-6">

                    <p className="text-slate-500">
                        Equipment
                    </p>

                    <h2 className="text-3xl font-bold mt-3">
                        {data.equipment}
                    </h2>

                </div>

                <div className="bg-white rounded-xl shadow p-6">

                    <p className="text-slate-500">
                        Status
                    </p>

                    <h2
                        className={`text-3xl font-bold mt-3 ${data.status === "Compliant"
                            ? "text-green-600"
                            : "text-red-600"
                            }`}
                    >
                        {data.status}
                    </h2>

                </div>

            </div>

            <div className="grid grid-cols-2 gap-6">

                <div className="bg-white rounded-xl shadow p-6">

                    <h2 className="text-xl font-bold mb-4">
                        Applicable Regulations
                    </h2>

                    {

                        data.regulations.length === 0 ?

                            <p className="text-slate-500">
                                No regulations detected.
                            </p>

                            :

                            data.regulations.map((item, index) => (

                                <div
                                    key={index}
                                    className="border rounded-lg p-3 mb-3"
                                >

                                    📚 {item}

                                </div>

                            ))

                    }

                </div>

                <div className="bg-white rounded-xl shadow p-6">

                    <h2 className="text-xl font-bold mb-4">
                        Audit Findings
                    </h2>

                    {

                        data.findings.length === 0 ?

                            <p className="text-slate-500">
                                No findings available.
                            </p>

                            :

                            data.findings.map((item, index) => (

                                <div
                                    key={index}
                                    className="border rounded-lg p-3 mb-3"
                                >

                                    ✅ {item}

                                </div>

                            ))

                    }

                </div>

            </div>
            <div className="grid grid-cols-4 gap-6 mb-6">

                <div className="bg-white rounded-xl shadow p-5">

                    <p className="text-3xl font-bold text-blue-600">
                        {data.statistics.audits}
                    </p>

                    <p>Audits</p>

                </div>

                <div className="bg-white rounded-xl shadow p-5">

                    <p className="text-3xl font-bold text-green-600">
                        {data.statistics.inspections}
                    </p>

                    <p>Inspections</p>

                </div>

                <div className="bg-white rounded-xl shadow p-5">

                    <p className="text-3xl font-bold text-red-600">
                        {data.statistics.incidents}
                    </p>

                    <p>Incidents</p>

                </div>

                <div className="bg-white rounded-xl shadow p-5">

                    <p className="text-3xl font-bold text-yellow-600">
                        {data.statistics.work_orders}
                    </p>

                    <p>Work Orders</p>

                </div>

            </div>

        </>

    );

}

export default Compliance;