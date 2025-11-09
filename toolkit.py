from typing import List, Optional
import os
from pydantic import BaseModel, Field
from superagi.tools.base_tool import BaseTool
from superagi.tools.base_toolkit import BaseToolkit

# ---------- TOOL: minimal, returns a short string ----------
class FinancialBriefingArgs(BaseModel):
    send_email: bool = Field(default=False, description="Email the briefing after generating.")
    keywords: Optional[str] = Field(default=None, description="Comma-separated keywords to filter news.")

class FinancialIntelligenceBriefingTool(BaseTool):
    name = "financial_intelligence_briefing"
    description = "Generates a financial briefing (indexes, news, weather)."

    args_schema = FinancialBriefingArgs

    def _execute(self, send_email: bool = False, keywords: Optional[str] = None) -> str:
        """
        Keep heavy logic elsewhere. For now we just return a success message.
        Later you can:
          - call your API (requests.post(...))
          - import your own lib inside this method
        """
        # Example of reading env vars safely (SuperAGI will prompt for these):
        gmail_user = os.getenv("GMAIL_USER", "")
        weather_key = os.getenv("OPENWEATHER_API_KEY", "")

        # TODO: Replace this block with your real call (HTTP or library)
        # Example:
        #   import requests
        #   resp = requests.post("http://backend:8000/run-briefing",
        #                        json={"send_email": send_email, "keywords": keywords})
        #   resp.raise_for_status()
        #   return resp.json().get("message", "Briefing generated.")

        return f"Briefing generated. send_email={send_email}, keywords={keywords or ''}"

# ---------- TOOLKIT: exposes the tool above ----------
class FinancialBriefingToolkit(BaseToolkit):
    name = "Financial Briefing Toolkit"
    description = "Toolkit exposing a single financial briefing tool."

    def get_tools(self) -> List[BaseTool]:
        return [FinancialIntelligenceBriefingTool()]

    def get_env_keys(self) -> List[str]:
        # List env vars your tool needs; SuperAGI will ask the user for them.
        return ["GMAIL_USER", "GMAIL_APP_PASSWORD", "OPENWEATHER_API_KEY"]
