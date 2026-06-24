from datetime import datetime, timezone
from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI(
    title="Egyptian Legal Agent Cloud",
    version="0.1.0",
    description="منصة قانونية مصرية متعددة الوكلاء - نواة سحابية أولية",
)

class LegalTask(BaseModel):
    question: str = Field(..., min_length=3)
    context: Optional[str] = None
    mode: str = "safe"

AGENTS = [
    {
        "id": "orchestrator",
        "name": "وكيل التنسيق الرئيسي",
        "role": "يوزع المهمة ويرتب مراحل العمل بين الوكلاء.",
    },
    {
        "id": "legislation_research",
        "name": "وكيل التشريعات",
        "role": "يبحث لاحقًا في القوانين واللوائح والقرارات الرسمية.",
    },
    {
        "id": "legal_analysis",
        "name": "وكيل التحليل القانوني",
        "role": "يفكك الوقائع والطلبات والأسانيد القانونية.",
    },
    {
        "id": "reverse_opponent",
        "name": "وكيل الخصم العكسي",
        "role": "يتوقع دفوع الطرف المقابل والثغرات المحتملة.",
    },
    {
        "id": "drafting",
        "name": "وكيل الصياغة",
        "role": "يعد مسودات المذكرات والتظلمات والشكاوى.",
    },
    {
        "id": "quality_closure",
        "name": "وكيل المراجعة والإغلاق",
        "role": "يفحص التناقضات والنواقص قبل اعتماد المخرج.",
    },
]

@app.get("/")
def home():
    return {
        "name": "Egyptian Legal Agent Cloud",
        "status": "running",
        "message": "المنصة السحابية متعددة الوكلاء تعمل كنواة أولية.",
        "docs": "/docs",
    }

@app.get("/health")
def health():
    return {
        "status": "ok",
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }

@app.get("/api/agents")
def list_agents():
    return {
        "count": len(AGENTS),
        "agents": AGENTS,
    }

@app.post("/api/analyze")
def analyze(task: LegalTask):
    mode_to_route = {
        "safe": [
            "وكيل التنسيق الرئيسي",
            "وكيل التحليل القانوني",
            "وكيل المراجعة والإغلاق",
        ],
        "research": [
            "وكيل التشريعات",
            "وكيل التحليل القانوني",
            "وكيل المراجعة والإغلاق",
        ],
        "reverse": [
            "وكيل التحليل القانوني",
            "وكيل الخصم العكسي",
            "وكيل المراجعة والإغلاق",
        ],
        "drafting": [
            "وكيل التحليل القانوني",
            "وكيل الصياغة",
            "وكيل المراجعة والإغلاق",
        ],
        "closure": [
            "وكيل الخصم العكسي",
            "وكيل الصياغة",
            "وكيل المراجعة والإغلاق",
        ],
    }

    route = mode_to_route.get(task.mode, mode_to_route["safe"])

    return {
        "status": "accepted",
        "mode": task.mode,
        "question": task.question,
        "context_received": bool(task.context),
        "agent_route": route,
        "message": "تم استقبال المهمة وتحديد مسار الوكلاء.",
    }
