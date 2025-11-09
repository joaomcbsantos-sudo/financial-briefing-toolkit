# Financial Briefing Toolkit

A SuperAGI toolkit exposing one tool: `financial_intelligence_briefing`.

It calls a local script `RAVAbriefing.py` already present in your backend container and returns a preview or emails the HTML briefing.

Requires env vars: `GMAIL_USER`, `GMAIL_APP_PASSWORD`, `OPENWEATHER_API_KEY`.
