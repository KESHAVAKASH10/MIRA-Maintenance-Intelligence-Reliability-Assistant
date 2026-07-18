import { useState, useRef, useEffect } from "react";
import PageHeader from "../components/PageHeader";
import AIResponseCard from "../components/AIResponseCard";
import { askMira } from "../services/chatService";

function Chat() {
    const [question, setQuestion] = useState("");
    const [messages, setMessages] = useState([]);
    const [loading, setLoading] = useState(false);

    const bottomRef = useRef(null);

    useEffect(() => {
        bottomRef.current?.scrollIntoView({
            behavior: "smooth",
        });
    }, [messages, loading]);

    const handleAsk = async () => {

        if (!question.trim() || loading) return;

        const userQuestion = question;

        setMessages((prev) => [
            ...prev,
            {
                role: "user",
                text: userQuestion,
            },
        ]);

        setQuestion("");
        setLoading(true);

        try {

            const result = await askMira(userQuestion);

            setMessages((prev) => [
                ...prev,
                {
                    role: "assistant",
                    answer: result.answer,
                    confidence: result.confidence,
                    confidenceLabel: result.confidence_label,
                    sources: result.sources || [],
                },
            ]);

        } catch (error) {

            setMessages((prev) => [
                ...prev,
                {
                    role: "assistant",
                    answer: error.message,
                    confidence: null,
                    confidenceLabel: "",
                    sources: [],
                },
            ]);

        } finally {

            setLoading(false);

        }

    };

    return (
        <>

            <PageHeader
                title="Industrial AI Copilot"
                subtitle="Powered by MIRA RAG Engine"
            />

            <div className="bg-white rounded-xl shadow h-[70vh] flex flex-col">

                <div className="flex-1 overflow-y-auto p-6 space-y-6">

                    {messages.length === 0 && (

                        <div className="text-center text-slate-500 mt-20">

                            <h2 className="text-2xl font-semibold mb-3">
                                Welcome to MIRA
                            </h2>

                            <p>
                                Ask about maintenance procedures,
                                SOPs, equipment manuals,
                                troubleshooting or regulations.
                            </p>

                        </div>

                    )}

                    {messages.map((msg, index) => (

                        <div key={index}>

                            {msg.role === "user" ? (

                                <div className="flex justify-end">

                                    <div className="bg-blue-600 text-white rounded-xl px-4 py-3 max-w-2xl">

                                        {msg.text}

                                    </div>

                                </div>

                            ) : (

                                <AIResponseCard message={msg} />

                            )}

                        </div>

                    ))}

                    {loading && (

                        <div className="bg-slate-100 rounded-xl p-4 italic text-slate-500">

                            🤖 MIRA is analyzing industrial documents...

                        </div>

                    )}

                    <div ref={bottomRef} />

                </div>

                <div className="border-t p-5 flex gap-4">

                    <input
                        type="text"
                        value={question}
                        disabled={loading}
                        placeholder="Ask MIRA anything..."
                        onChange={(e) => setQuestion(e.target.value)}
                        onKeyDown={(e) => {
                            if (e.key === "Enter") {
                                handleAsk();
                            }
                        }}
                        className="flex-1 border rounded-lg px-4 py-3 outline-none"
                    />

                    <button
                        onClick={handleAsk}
                        disabled={loading}
                        className="bg-blue-600 hover:bg-blue-700 text-white px-8 rounded-lg disabled:opacity-60"
                    >
                        {loading ? "Thinking..." : "Send"}
                    </button>

                </div>

            </div>

        </>
    );
}

export default Chat;