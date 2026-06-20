# DevPilot AI: Multi-Agent Software Engineering Assistant
## Submission Writeup & Project Description

### 1. Project Overview & Inspiration
Software development requires wearing many hats: writing clean logic, detecting obscure bugs, validating security compliance, writing tests, and maintaining documentation. Transitioning between these domains can break developer focus. 

**DevPilot AI** is an autonomous, multi-agent developer workspace designed to streamline these engineering tasks. Utilizing Google's Gemini models, it features a manager agent that orchestrates a team of specialized AI sub-agents. 

To bridge the gap between backend capabilities and developer experience, we transformed a basic, static JSON FastAPI endpoint into a stunning, interactive Single Page Application (SPA) dashboard. Developers can now select dedicated agents, stream execution logs, write prompts, and view rendered outputs with premium code styling directly in their browser.

---

### 2. How It Works (The Multi-Agent Architecture)
DevPilot AI employs a hierarchical agent pattern:
*   **Manager Agent (Auto Decider)**: Analyzes the user's software engineering task and routes it to the most qualified agent.
*   **Code Explainer (Code Understanding Agent)**: Analyzes logical structures, explaining code paths and project hierarchies.
*   **Bug Detector (Bug Detection Agent)**: Scans snippets for race conditions, syntax faults, and logical edge cases.
*   **Security Guard (Security Agent)**: Highlights security vulnerabilities, credential leaks, and compliance issues.
*   **Test Engineer (Testing Agent)**: Generates high-quality unit tests, mock configurations, and integration plans.
*   **Docs Writer (Documentation Agent)**: Generates clear docstrings, inline comments, and project READMEs.

---

### 3. Key Dashboard Features & UI/UX
*   **Rich Developer Aesthetics**: High-end dark mode interface featuring radial purple/teal background gradients, interactive glassmorphism cards, and smooth hover animations.
*   **Interactive Agent Selector**: Visual cards that allow developers to explicitly target a specific agent role or let the Manager Agent auto-delegate.
*   **"Share with Agent" Console**: A dedicated workspace text area built for writing prompts and sharing large code segments.
*   **Live Work Logs**: Real-time status console displaying routing logs (e.g., *"[Info] Routing task to: Bug Detector"*) so developers can track the agentic workflow.
*   **Premium Output Rendering**: Full Markdown output parsed dynamically via `marked.js` and highlighted using the `tokyo-night-dark` theme via `highlight.js`, complete with single-click "Copy Code" overlays.

---

### 4. Technical Stack
*   **Backend Framework**: FastAPI (Python 3.13)
*   **AI Engine**: Google GenAI SDK (configured with dynamic `.env` resolution, utilizing the stable `gemini-flash-latest` model)
*   **Frontend**: Vanilla HTML5, CSS3 Custom Properties & Animations, Modern ES6 Javascript
*   **Third-party UI Libraries**: Highlight.js (Tokyo Night style), Marked.js, Plus Jakarta Sans & Fira Code Google Fonts
