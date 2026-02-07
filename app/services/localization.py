from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class LocalizationPack:
    lang: str
    direction: str
    labels: dict[str, Any]


_EN_LABELS: dict[str, Any] = {
    "app_name": "Homebase",
    "tagline": "AI-assisted property operations for Dubai/UAE",
    "nav": {
        "dashboard": "Dashboard",
        "maintenance": "Maintenance",
        "renewals": "Renewals",
        "properties": "Properties",
        "vendors": "Vendors",
        "analytics": "Analytics",
        "settings": "Settings",
    },
    "lang_switch": "EN / AR",
    "ai_assisted": "AI-assisted, manager approved",
    "ai_status": "AI Agent Status",
    "active": "Active",
    "processing": "Processing",
    "idle": "Idle",
    "freshness": "Updated 2 minutes ago",
    "response": "Agent response: 8 seconds",
    "rera_badge": "🇦🇪 RERA Compliant",
    "saved_time": "Saved 4 hours of manual work",
    "human_gate": "Manager approval required",
    "approve": "Approve",
    "modify": "Modify Terms",
    "send": "Send to Tenant",
    "process_all": "Process all renewals",
    "notices": "Send 90-day notices",
    "demo_mode": "Hackathon demo data",
}

_AR_LABELS: dict[str, Any] = {
    "app_name": "هومبيس",
    "tagline": "عمليات عقارية مدعومة بالذكاء الاصطناعي في دبي والإمارات",
    "nav": {
        "dashboard": "لوحة التحكم",
        "maintenance": "الصيانة",
        "renewals": "التجديدات",
        "properties": "العقارات",
        "vendors": "المورّدون",
        "analytics": "التحليلات",
        "settings": "الإعدادات",
    },
    "lang_switch": "ع / EN",
    "ai_assisted": "مساعد بالذكاء الاصطناعي مع اعتماد المدير",
    "ai_status": "حالة وكيل الذكاء الاصطناعي",
    "active": "نشط",
    "processing": "قيد المعالجة",
    "idle": "خامل",
    "freshness": "تم التحديث قبل دقيقتين",
    "response": "استجابة الوكيل: 8 ثوانٍ",
    "rera_badge": "🇦🇪 متوافق مع ريرا",
    "saved_time": "تم توفير 4 ساعات من العمل اليدوي",
    "human_gate": "مطلوب اعتماد المدير",
    "approve": "اعتماد",
    "modify": "تعديل الشروط",
    "send": "إرسال إلى المستأجر",
    "process_all": "معالجة جميع التجديدات",
    "notices": "إرسال إشعارات 90 يوم",
    "demo_mode": "بيانات عرض الهاكاثون",
}


def normalize_lang(value: str | None) -> str:
    if value and value.lower().startswith("ar"):
        return "ar"
    return "en"


def get_pack(lang: str) -> LocalizationPack:
    normalized = normalize_lang(lang)
    if normalized == "ar":
        return LocalizationPack(lang="ar", direction="rtl", labels=_AR_LABELS)
    return LocalizationPack(lang="en", direction="ltr", labels=_EN_LABELS)


def choose_lang(query_value: str | None, cookie_value: str | None) -> str:
    return normalize_lang(query_value or cookie_value)
