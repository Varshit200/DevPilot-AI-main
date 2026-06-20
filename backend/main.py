import os
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from agents.manager_agent import manager_agent

app = FastAPI(
    title="DevPilot AI"
)

# Enable CORS for local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class AgentRequest(BaseModel):
    task: str
    agent: str = "auto"

@app.post("/agent")
def run_agent(request: AgentRequest):
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise HTTPException(
            status_code=400,
            detail="GEMINI_API_KEY is not set in the workspace environment. Please create a '.env' file in the project root directory and set GEMINI_API_KEY=your_api_key."
        )
    
    try:
        task_text = request.task
        # If a specific agent is selected, prepend it to the prompt so the manager agent prioritizes it.
        if request.agent and request.agent != "auto":
            task_text = f"[Directive: Use {request.agent}] {task_text}"
        
        result = manager_agent(task_text)
        return {
            "Manager Agent": "Completed",
            "AI Output": result
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred while running the agent: {str(e)}"
        )

@app.get("/", response_class=HTMLResponse)
def home():
    html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>DevPilot AI - Dashboard</title>
    <!-- Fonts & Icons -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=Fira+Code:wght@400;500&display=swap" rel="stylesheet">
    <!-- Highlight.js for Code Highlighting -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.8.0/styles/tokyo-night-dark.min.css">
    <script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.8.0/highlight.min.js"></script>
    <!-- Marked.js for Markdown Parsing -->
    <script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
    
    <style>
        :root {
            --bg-color: #08060f;
            --bg-grid: rgba(123, 44, 191, 0.03);
            --panel-bg: rgba(15, 12, 28, 0.7);
            --panel-border: rgba(255, 255, 255, 0.06);
            --text-primary: #f4f3f7;
            --text-secondary: #9f9baa;
            --primary-color: #8a2be2;
            --primary-glow: rgba(138, 43, 226, 0.4);
            --accent-green: #00f5d4;
            --accent-blue: #3a86ff;
            --accent-pink: #ff007f;
            --card-hover: rgba(255, 255, 255, 0.02);
            --card-active: rgba(138, 43, 226, 0.15);
            --card-active-border: #8a2be2;
        }

        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            font-family: 'Plus Jakarta Sans', sans-serif;
            -webkit-font-smoothing: antialiased;
        }

        body {
            background-color: var(--bg-color);
            background-image: 
                radial-gradient(circle at 10% 20%, rgba(90, 24, 154, 0.15) 0%, transparent 40%),
                radial-gradient(circle at 90% 80%, rgba(0, 245, 212, 0.08) 0%, transparent 40%),
                linear-gradient(var(--bg-grid) 1px, transparent 1px),
                linear-gradient(90deg, var(--bg-grid) 1px, transparent 1px);
            background-size: 100% 100%, 100% 100%, 30px 30px, 30px 30px;
            color: var(--text-primary);
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            overflow-x: hidden;
        }

        /* Custom Scrollbar */
        ::-webkit-scrollbar {
            width: 8px;
            height: 8px;
        }
        ::-webkit-scrollbar-track {
            background: rgba(15, 12, 28, 0.5);
        }
        ::-webkit-scrollbar-thumb {
            background: rgba(138, 43, 226, 0.3);
            border-radius: 4px;
        }
        ::-webkit-scrollbar-thumb:hover {
            background: rgba(138, 43, 226, 0.5);
        }

        header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 20px 40px;
            background: rgba(8, 6, 15, 0.6);
            backdrop-filter: blur(12px);
            border-bottom: 1px solid var(--panel-border);
            position: sticky;
            top: 0;
            z-index: 100;
        }

        .logo-container {
            display: flex;
            align-items: center;
            gap: 12px;
        }

        .logo-icon {
            font-size: 24px;
            background: linear-gradient(135deg, var(--primary-color), var(--accent-green));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-weight: 800;
            display: flex;
            align-items: center;
            justify-content: center;
            width: 40px;
            height: 40px;
            border-radius: 12px;
            border: 2px solid var(--primary-color);
            box-shadow: 0 0 15px var(--primary-glow);
        }

        .logo-text {
            font-size: 20px;
            font-weight: 700;
            letter-spacing: 0.5px;
            background: linear-gradient(to right, #ffffff, #dcd7ec);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .status-pill {
            display: flex;
            align-items: center;
            gap: 8px;
            background: rgba(0, 245, 212, 0.08);
            border: 1px solid rgba(0, 245, 212, 0.2);
            padding: 6px 16px;
            border-radius: 20px;
            font-size: 13px;
            font-weight: 600;
            color: var(--accent-green);
        }

        .status-dot {
            width: 8px;
            height: 8px;
            background-color: var(--accent-green);
            border-radius: 50%;
            box-shadow: 0 0 10px var(--accent-green);
            animation: pulse 2s infinite;
        }

        @keyframes pulse {
            0% { transform: scale(0.9); opacity: 0.6; }
            50% { transform: scale(1.2); opacity: 1; box-shadow: 0 0 15px var(--accent-green); }
            100% { transform: scale(0.9); opacity: 0.6; }
        }

        main {
            flex: 1;
            display: grid;
            grid-template-columns: 450px 1fr;
            gap: 30px;
            padding: 30px 40px;
            max-width: 1600px;
            margin: 0 auto;
            width: 100%;
        }

        .left-col {
            display: flex;
            flex-direction: column;
            gap: 25px;
        }

        .right-col {
            display: flex;
            flex-direction: column;
        }

        .card {
            background: var(--panel-bg);
            border: 1px solid var(--panel-border);
            border-radius: 16px;
            padding: 24px;
            backdrop-filter: blur(16px);
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
            transition: border-color 0.3s, box-shadow 0.3s;
        }

        .card:hover {
            border-color: rgba(138, 43, 226, 0.2);
        }

        .card-title {
            font-size: 16px;
            font-weight: 700;
            margin-bottom: 16px;
            display: flex;
            align-items: center;
            gap: 8px;
            color: #ffffff;
            letter-spacing: 0.3px;
        }

        .card-title svg {
            color: var(--primary-color);
        }

        /* Agent Selection Styles */
        .agent-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 12px;
            margin-bottom: 10px;
        }

        .agent-card {
            background: rgba(255, 255, 255, 0.015);
            border: 1px solid var(--panel-border);
            border-radius: 12px;
            padding: 14px;
            cursor: pointer;
            transition: all 0.2s ease-in-out;
            display: flex;
            flex-direction: column;
            gap: 8px;
        }

        .agent-card:hover {
            background: var(--card-hover);
            border-color: rgba(255, 255, 255, 0.15);
            transform: translateY(-2px);
        }

        .agent-card.active {
            background: var(--card-active);
            border-color: var(--card-active-border);
            box-shadow: 0 0 15px rgba(138, 43, 226, 0.2);
        }

        .agent-icon {
            font-size: 18px;
            margin-bottom: 2px;
        }

        .agent-name {
            font-size: 13px;
            font-weight: 600;
            color: #ffffff;
        }

        .agent-desc {
            font-size: 11px;
            color: var(--text-secondary);
            line-height: 1.4;
        }

        .agent-card.full-width {
            grid-column: span 2;
            flex-direction: row;
            align-items: center;
            gap: 14px;
        }

        /* Share with Agent Section */
        .input-group {
            display: flex;
            flex-direction: column;
            gap: 10px;
            margin-top: 15px;
        }

        label {
            font-size: 12px;
            font-weight: 600;
            color: var(--text-secondary);
            text-transform: uppercase;
            letter-spacing: 0.8px;
        }

        textarea {
            background: rgba(5, 3, 10, 0.5);
            border: 1px solid var(--panel-border);
            border-radius: 12px;
            padding: 16px;
            color: var(--text-primary);
            font-size: 14px;
            min-height: 180px;
            resize: vertical;
            outline: none;
            transition: border-color 0.3s, box-shadow 0.3s;
            line-height: 1.5;
        }

        textarea:focus {
            border-color: var(--primary-color);
            box-shadow: 0 0 10px var(--primary-glow);
        }

        .btn-submit {
            background: linear-gradient(135deg, var(--primary-color) 0%, #6f2dbd 100%);
            border: none;
            border-radius: 12px;
            color: #ffffff;
            font-size: 14px;
            font-weight: 700;
            padding: 14px;
            cursor: pointer;
            transition: all 0.3s;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 8px;
            box-shadow: 0 4px 20px rgba(138, 43, 226, 0.3);
            margin-top: 10px;
        }

        .btn-submit:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 25px rgba(138, 43, 226, 0.5);
            background: linear-gradient(135deg, #9d4edd 0%, var(--primary-color) 100%);
        }

        .btn-submit:active {
            transform: translateY(1px);
        }

        .btn-submit:disabled {
            background: #252230;
            color: var(--text-secondary);
            cursor: not-allowed;
            box-shadow: none;
            transform: none;
        }

        /* Workspace & Output Section */
        .workspace-card {
            height: 100%;
            display: flex;
            flex-direction: column;
            min-height: calc(100vh - 120px);
        }

        .workspace-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 1px solid var(--panel-border);
            padding-bottom: 16px;
            margin-bottom: 20px;
        }

        .workspace-title {
            font-size: 18px;
            font-weight: 700;
            color: #ffffff;
        }

        .output-container {
            flex: 1;
            display: flex;
            flex-direction: column;
            overflow-y: auto;
            border-radius: 8px;
            position: relative;
        }

        .empty-state {
            margin: auto;
            text-align: center;
            max-width: 400px;
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 16px;
            color: var(--text-secondary);
            padding: 40px 20px;
        }

        .empty-icon {
            font-size: 48px;
            animation: float 4s ease-in-out infinite;
        }

        @keyframes float {
            0% { transform: translateY(0px); }
            50% { transform: translateY(-10px); }
            100% { transform: translateY(0px); }
        }

        .loading-state {
            margin: auto;
            text-align: center;
            display: none;
            flex-direction: column;
            align-items: center;
            gap: 20px;
        }

        .spinner {
            width: 50px;
            height: 50px;
            border: 3px solid rgba(138, 43, 226, 0.1);
            border-top: 3px solid var(--primary-color);
            border-right: 3px solid var(--accent-green);
            border-radius: 50%;
            animation: spin 1s linear infinite;
        }

        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }

        .loading-text {
            font-size: 14px;
            color: var(--text-secondary);
            font-weight: 500;
        }

        .logs-stream {
            width: 100%;
            background: rgba(5, 3, 10, 0.4);
            border: 1px solid var(--panel-border);
            border-radius: 8px;
            padding: 12px;
            font-family: 'Fira Code', monospace;
            font-size: 11px;
            color: var(--accent-blue);
            text-align: left;
            margin-top: 15px;
            max-height: 120px;
            overflow-y: auto;
            display: none;
        }

        .log-item {
            margin-bottom: 4px;
        }

        .log-item.success {
            color: var(--accent-green);
        }

        /* Markdown Output Styles */
        .markdown-body {
            display: none;
            color: var(--text-primary);
            line-height: 1.6;
            font-size: 15px;
            padding-right: 10px;
        }

        .markdown-body h1, .markdown-body h2, .markdown-body h3 {
            color: #ffffff;
            margin-top: 24px;
            margin-bottom: 12px;
            font-weight: 700;
        }

        .markdown-body h1 { font-size: 22px; border-bottom: 1px solid var(--panel-border); padding-bottom: 8px; }
        .markdown-body h2 { font-size: 18px; }
        .markdown-body h3 { font-size: 15px; }

        .markdown-body p {
            margin-bottom: 16px;
        }

        .markdown-body ul, .markdown-body ol {
            margin-bottom: 16px;
            padding-left: 20px;
        }

        .markdown-body li {
            margin-bottom: 6px;
        }

        .markdown-body code {
            font-family: 'Fira Code', monospace;
            background: rgba(138, 43, 226, 0.1);
            color: #e0aaff;
            padding: 3px 6px;
            border-radius: 4px;
            font-size: 13px;
        }

        .markdown-body pre {
            position: relative;
            background: #0f0b1a;
            border: 1px solid var(--panel-border);
            border-radius: 8px;
            padding: 16px;
            margin-bottom: 20px;
            overflow-x: auto;
        }

        .markdown-body pre code {
            background: transparent;
            color: inherit;
            padding: 0;
            border-radius: 0;
            font-size: 13px;
        }

        /* Copy Button for code blocks */
        .copy-btn {
            position: absolute;
            top: 8px;
            right: 8px;
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid var(--panel-border);
            border-radius: 4px;
            color: var(--text-secondary);
            font-size: 11px;
            padding: 4px 8px;
            cursor: pointer;
            transition: all 0.2s;
            backdrop-filter: blur(4px);
        }

        .copy-btn:hover {
            background: var(--primary-color);
            color: #ffffff;
            border-color: var(--primary-color);
        }

        /* Utility classes */
        .highlight-text {
            color: var(--primary-color);
            font-weight: 600;
        }
    </style>
</head>
<body>

    <header>
        <div class="logo-container">
            <div class="logo-icon">DP</div>
            <div class="logo-text">DevPilot AI</div>
        </div>
        <div class="status-pill">
            <div class="status-dot"></div>
            <span>Agentic Workspace Connected</span>
        </div>
    </header>

    <main>
        <div class="left-col">
            <!-- Agent Role Config -->
            <div class="card">
                <div class="card-title">
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2a10 10 0 1 0 10 10H12V2z"/><path d="M12 2a10 10 0 0 1 10 10h-10V2z"/><path d="M12 12L2.5 12"/><path d="M12 12l9.5 0"/></svg>
                    Select Workspace Agent
                </div>
                <div class="agent-grid">
                    <div class="agent-card active" data-agent="auto">
                        <span class="agent-icon">🔮</span>
                        <span class="agent-name">Auto Decider</span>
                        <span class="agent-desc">Manager agent delegates to the best team member.</span>
                    </div>
                    <div class="agent-card" data-agent="Code Understanding Agent">
                        <span class="agent-icon">📁</span>
                        <span class="agent-name">Code Explainer</span>
                        <span class="agent-desc">Explains logic, architecture & file structures.</span>
                    </div>
                    <div class="agent-card" data-agent="Bug Detection Agent">
                        <span class="agent-icon">🐛</span>
                        <span class="agent-name">Bug Detector</span>
                        <span class="agent-desc">Scans code snippets for logic errors & race conditions.</span>
                    </div>
                    <div class="agent-card" data-agent="Security Agent">
                        <span class="agent-icon">🛡️</span>
                        <span class="agent-name">Security Guard</span>
                        <span class="agent-desc">Identifies vulnerabilities & compliance risks.</span>
                    </div>
                    <div class="agent-card" data-agent="Testing Agent">
                        <span class="agent-icon">🧪</span>
                        <span class="agent-name">Test Engineer</span>
                        <span class="agent-desc">Writes unit tests, integration plans & mocks.</span>
                    </div>
                    <div class="agent-card" data-agent="Documentation Agent">
                        <span class="agent-icon">✍️</span>
                        <span class="agent-name">Docs Writer</span>
                        <span class="agent-desc">Generates professional docstrings & READMEs.</span>
                    </div>
                </div>
            </div>

            <!-- Task Input -->
            <div class="card" style="flex: 1;">
                <div class="card-title">
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg>
                    Share with Agent
                </div>
                <div class="input-group">
                    <label for="task-input">Prompt or Task Details</label>
                    <textarea id="task-input" placeholder="Explain what you need help with. E.g., 'Find bugs in this function' or 'Write unit tests for a fast api route'"></textarea>
                    
                    <button class="btn-submit" id="btn-submit">
                        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><line x1="22" y1="2" x2="11" y2="13"/><polygon points="22 2 15 22 11 13 2 9 22 2"/></svg>
                        <span>Submit to Agent</span>
                    </button>
                </div>
            </div>
        </div>

        <div class="right-col">
            <!-- Output Console -->
            <div class="card workspace-card">
                <div class="workspace-header">
                    <span class="workspace-title">Workspace Output Log</span>
                </div>
                
                <div class="output-container" id="output-container">
                    <!-- Empty State -->
                    <div class="empty-state" id="empty-state">
                        <span class="empty-icon">🤖</span>
                        <h3>No Active Request</h3>
                        <p>Configure your workspace agent on the left, input a prompt, and click "Submit to Agent" to begin.</p>
                    </div>

                    <!-- Loading State -->
                    <div class="loading-state" id="loading-state">
                        <div class="spinner"></div>
                        <h3 style="color: #ffffff;">Consulting DevPilot AI Agents...</h3>
                        <p class="loading-text">Analyzing request & formatting agent response</p>
                        <div class="logs-stream" id="logs-stream">
                            <div class="log-item">[Info] Connection established.</div>
                            <div class="log-item" id="log-routing">[Info] Routing task to selected agent...</div>
                            <div class="log-item" id="log-running">[Info] Invoking LLM processing...</div>
                        </div>
                    </div>

                    <!-- Output Content -->
                    <div class="markdown-body" id="output-content"></div>
                </div>
            </div>
        </div>
    </main>

    <script>
        // State
        let selectedAgent = "auto";

        // DOM elements
        const agentCards = document.querySelectorAll('.agent-card');
        const taskInput = document.getElementById('task-input');
        const submitBtn = document.getElementById('btn-submit');
        const emptyState = document.getElementById('empty-state');
        const loadingState = document.getElementById('loading-state');
        const outputContent = document.getElementById('output-content');
        const logsStream = document.getElementById('logs-stream');
        const logRouting = document.getElementById('log-routing');
        const logRunning = document.getElementById('log-running');

        // Agent selection handler
        agentCards.forEach(card => {
            card.addEventListener('click', () => {
                agentCards.forEach(c => c.classList.remove('active'));
                card.classList.add('active');
                selectedAgent = card.getAttribute('data-agent');
            });
        });

        // Submit task handler
        submitBtn.addEventListener('click', async () => {
            const task = taskInput.value.trim();
            if (!task) return;

            // UI state management
            emptyState.style.display = 'none';
            outputContent.style.display = 'none';
            loadingState.style.display = 'flex';
            logsStream.style.display = 'block';
            submitBtn.disabled = true;

            logRouting.innerHTML = `[Info] Routing task to: <span style="color: var(--accent-green);">${selectedAgent === 'auto' ? 'Manager Agent (Auto)' : selectedAgent}</span>`;
            logRunning.innerHTML = `[Info] Processing prompt...`;

            try {
                const response = await fetch('/agent', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        task: task,
                        agent: selectedAgent
                    })
                });

                if (!response.ok) {
                    let errorMessage = `Server returned status: ${response.status}`;
                    try {
                        const errorData = await response.json();
                        if (errorData && errorData.detail) {
                            errorMessage = errorData.detail;
                        }
                    } catch (e) {}
                    throw new Error(errorMessage);
                }

                const data = await response.json();
                const rawOutput = data["AI Output"];

                // Render Markdown output
                outputContent.innerHTML = marked.parse(rawOutput);
                
                // Highlight code blocks
                document.querySelectorAll('pre code').forEach((block) => {
                    hljs.highlightElement(block);
                });

                // Add copy buttons to code blocks
                addCopyButtons();

                // Transition UI
                loadingState.style.display = 'none';
                outputContent.style.display = 'block';
            } catch (err) {
                console.error(err);
                outputContent.innerHTML = `
                    <div style="color: var(--accent-pink); padding: 20px; border: 1px solid rgba(255, 0, 127, 0.2); background: rgba(255, 0, 127, 0.05); border-radius: 8px;">
                        <h3>⚠️ Error Encountered</h3>
                        <p style="margin-top: 10px;">${err.message || 'An unknown error occurred while contacting the agent backend.'}</p>
                        <p style="margin-top: 10px; font-size: 13px; color: var(--text-secondary);">Please verify that the FastAPI backend server is running and accessible.</p>
                    </div>
                `;
                loadingState.style.display = 'none';
                outputContent.style.display = 'block';
            } finally {
                submitBtn.disabled = false;
            }
        });

        // Helper to add Copy button to code pre elements
        function addCopyButtons() {
            const preElements = document.querySelectorAll('pre');
            preElements.forEach((pre) => {
                // Prevent duplicate buttons
                if (pre.querySelector('.copy-btn')) return;

                const button = document.createElement('button');
                button.className = 'copy-btn';
                button.innerText = 'Copy';
                
                button.addEventListener('click', async () => {
                    const code = pre.querySelector('code').innerText;
                    try {
                        await navigator.clipboard.writeText(code);
                        button.innerText = 'Copied!';
                        setTimeout(() => {
                            button.innerText = 'Copy';
                        }, 2000);
                    } catch (err) {
                        button.innerText = 'Failed';
                    }
                });

                pre.appendChild(button);
            });
        }
    </script>
</body>
</html>
    """
    return HTMLResponse(content=html_content, status_code=200)