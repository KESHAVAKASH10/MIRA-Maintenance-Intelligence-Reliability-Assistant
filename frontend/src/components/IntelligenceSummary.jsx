import ReactMarkdown from "react-markdown";

function IntelligenceSummary({ summary }) {
    return (
        <div className="bg-white rounded-xl shadow p-6">

            <h3 className="text-xl font-semibold mb-4">
                🧠 AI Intelligence Summary
            </h3>

            <div className="prose max-w-none">
                <ReactMarkdown>
                    {summary}
                </ReactMarkdown>
            </div>

        </div>
    );
}

export default IntelligenceSummary;