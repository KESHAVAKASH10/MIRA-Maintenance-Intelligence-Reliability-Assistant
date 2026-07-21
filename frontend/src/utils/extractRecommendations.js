export default function extractRecommendations(text) {

    const match = text.match(
        /Recommended Actions:\s*([\s\S]*?)(Relevant Regulations:|$)/i
    );

    if (!match) {
        return [];
    }

    return match[1]
        .split("\n")
        .map(line => line.replace(/^[-•*\d.]+\s*/, "").trim())
        .filter(Boolean);

}