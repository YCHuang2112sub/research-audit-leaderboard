
import fs from 'fs';
import path from 'path';

// Paths
const clientOutput = path.join(process.cwd(), 'output', 'results.json');
const debugOutput = path.join(process.cwd(), 'debug_output', 'green_audit_result.json');
const resultDir = path.join(process.cwd(), 'results');

if (!fs.existsSync(resultDir)) {
    fs.mkdirSync(resultDir, { recursive: true });
}

// 1. Read Participant ID
let participantId = "";
try {
    const clientData = JSON.parse(fs.readFileSync(clientOutput, 'utf-8'));
    participantId = clientData.participants?.agent || "unknown-agent-id";
    console.log(`Found Participant ID: ${participantId}`);
} catch (e) {
    console.warn("Could not read client output. Using placeholder ID.");
    participantId = "placeholder-agent-id";
}

// 2. Read Audit Scores
let auditScores = [];
try {
    const debugData = JSON.parse(fs.readFileSync(debugOutput, 'utf-8'));
    const textPart = debugData.parts?.[0]?.text;
    if (textPart) {
        auditScores = JSON.parse(textPart); // array of score objects
        console.log(`Found ${auditScores.length} audit results.`);
    }
} catch (e) {
    console.error("Failed to read debug output:", e);
    process.exit(1);
}

// 3. Construct Payload
const finalJson = {
    participants: {
        agent: participantId
    },
    results: auditScores
};

// 4. Get Target Filename from Args
const targetFileName = process.argv[2] || 'result_unknown.json';
const targetPath = path.join(resultDir, targetFileName);

// 5. Write File
fs.writeFileSync(targetPath, JSON.stringify(finalJson, null, 2));

console.log(`Successfully generated results/${targetFileName} from current debug output.`);
