import os
from pathlib import Path
from dotenv import load_dotenv
import google.generativeai as genai

# Find the project root dynamically and load .env
current_dir = Path(__file__).resolve().parent
project_root = current_dir.parent
env_path = project_root / '.env'
load_dotenv(dotenv_path=env_path)

# Configure API Key if present
api_key = os.getenv("GEMINI_API_KEY")
if api_key:
    genai.configure(api_key=api_key)


model = genai.GenerativeModel(
    "gemini-flash-latest"
)




def manager_agent(user_task):

    prompt = f"""

You are DevPilot AI Manager Agent.

You have these agents:

1. Code Understanding Agent
2. Bug Detection Agent
3. Security Agent
4. Testing Agent
5. Documentation Agent


Analyze user request:

{user_task}


Decide required agent.

Generate professional software engineering output.

"""


    response = model.generate_content(prompt)


    return response.text