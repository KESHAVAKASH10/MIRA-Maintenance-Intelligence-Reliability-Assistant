import ReactMarkdown from "react-markdown";

function AIResponseCard({ message }) {

    const answer = message.answer || "";

    const extractSection = (start, end) => {

        const startIndex = answer.indexOf(start);

        if (startIndex === -1) return "";

        const from = startIndex + start.length;

        const endIndex = end
            ? answer.indexOf(end, from)
            : -1;

        return (
            endIndex === -1
                ? answer.substring(from)
                : answer.substring(from, endIndex)
        ).trim();

    };

    const directAnswer = extractSection(
        "Direct Answer:",
        "Supporting Evidence:"
    );

    const evidence = extractSection(
        "Supporting Evidence:",
        "Recommended Actions:"
    );

    const actions = extractSection(
        "Recommended Actions:",
        "Relevant Regulations:"
    );

    const regulations = extractSection(
        "Relevant Regulations:",
        null
    );

    const badgeColor = () => {

        if (message.confidenceLabel === "High")
            return "bg-green-100 text-green-700";

        if (message.confidenceLabel === "Medium")
            return "bg-yellow-100 text-yellow-700";

        return "bg-red-100 text-red-700";

    };

    const Section = ({ title, icon, content }) => {

        if (!content) return null;

        return (

            <div className="bg-white border rounded-xl p-4">

                <h4 className="font-semibold mb-3">
                    {icon} {title}
                </h4>

                <div className="prose prose-slate max-w-none text-sm">

                    <ReactMarkdown>
                        {content}
                    </ReactMarkdown>

                </div>

            </div>

        );

    };

    return (

        <div className="bg-slate-100 rounded-xl p-5 space-y-4">

            <h3 className="text-lg font-semibold">
                🤖 MIRA Response
            </h3>

            <Section
                title="Direct Answer"
                icon="💡"
                content={directAnswer}
            />

            <Section
                title="Supporting Evidence"
                icon="📖"
                content={evidence}
            />

            <Section
                title="Recommended Actions"
                icon="🛠"
                content={actions}
            />

            <Section
                title="Relevant Regulations"
                icon="⚖"
                content={regulations}
            />

            {message.confidence && (

                <div className="flex items-center justify-between">

                    <span
                        className={`px-3 py-1 rounded-full text-sm font-semibold ${badgeColor()}`}
                    >
                        {message.confidence}% • {message.confidenceLabel}
                    </span>

                </div>

            )}

            {message.sources?.length > 0 && (

                <div>

                    <h4 className="font-semibold mb-3">
                        📄 Supporting Documents
                    </h4>

                    <div className="space-y-2">

                        {message.sources.map((source, index) => (

                            <div
                                key={index}
                                className="bg-white border rounded-lg px-3 py-2 text-sm"
                            >
                                {source}
                            </div>

                        ))}

                    </div>

                </div>

            )}

        </div>

    );

}

export default AIResponseCard;