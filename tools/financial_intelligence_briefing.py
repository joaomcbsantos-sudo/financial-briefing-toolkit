from superagi.tools.base_tool import BaseTool
from pydantic import BaseModel, Field
from typing import Optional, List
import json
from RAVAbriefing import FinancialBriefingTool as Core

class FinancialBriefingArgs(BaseModel):
    send_email: bool = Field(default=True)
    preview_html: bool = Field(default=False)
    keywords: Optional[List[str]] = None
    extra_tickers: Optional[List[str]] = None

class SuperAGIFinancialBriefingTool(BaseTool):
    name: str = "financial_intelligence_briefing"
    description: str = "Generates and emails a financial briefing."
    args_schema: type = FinancialBriefingArgs

    def _execute(self, send_email=True, preview_html=False,
                 keywords=None, extra_tickers=None) -> str:
        try:
            tool = Core()

            if keywords:
                tool.config["keywords"] = keywords
            if extra_tickers:
                for t in extra_tickers:
                    if not t.endswith(".SA"):
                        t += ".SA"
                    if t not in tool.config["portfolio"]:
                        tool.config["portfolio"].append(t)

            indexes = tool.get_market_indexes()
            portfolio = tool.get_portfolio_data()
            macro = tool.get_macro_data()
            commodities = tool.get_commodities_data()

            all_headlines = []
            for source in tool.config["news_sources"]:
                all_headlines.extend(tool.scrape_headlines(source["url"], source["name"]))
            news = tool.filter_headlines_by_keywords(all_headlines)
            weather = tool.get_weather()

            data = {"indexes": indexes, "portfolio": portfolio, "macro": macro,
                    "commodities": commodities, "news": news, "weather": weather}

            html = tool.generate_html_email(data)

            if send_email:
                tool.send_email(html)

            result = {"sent_email": send_email,
                      "avg_change": round(portfolio.get("avg_change", 0), 2),
                      "news_count": len(news)}
            if preview_html:
                result["html_preview"] = html[:500] + "..."

            return json.dumps(result)
        except Exception as e:
            return json.dumps({"error": str(e)})
