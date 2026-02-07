from __future__ import annotations

from datetime import datetime

from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from app.services.localization import choose_lang, get_pack
from app.services.mock_store import store


templates = Jinja2Templates(directory="app/templates")
router = APIRouter()


NAV_CONFIG = [
    ("dashboard", "/dashboard"),
    ("maintenance", "/maintenance/vendors"),
    ("renewals", "/renewals/pipeline"),
    ("properties", "/properties/control-panel"),
    ("vendors", "/vendors/compliance"),
    ("analytics", "/analytics"),
    ("settings", "/settings"),
]


def nav_items(lang: str, labels: dict) -> list[dict[str, str]]:
    return [
        {"key": key, "title": labels["nav"][key], "href": f"{path}?lang={lang}"}
        for key, path in NAV_CONFIG
    ]


def base_context(request: Request, title: str, nav_active: str) -> dict:
    lang = choose_lang(request.query_params.get("lang"), request.cookies.get("lang"))
    pack = get_pack(lang)
    return {
        "request": request,
        "title": title,
        "lang": lang,
        "dir": pack.direction,
        "labels": pack.labels,
        "nav_items": nav_items(lang, pack.labels),
        "nav_active": nav_active,
        "agent_state": store.get_agent_state(),
        "today": datetime.now().strftime("%d/%m/%Y"),
    }


@router.get("/")
async def root(request: Request):
    lang = choose_lang(request.query_params.get("lang"), request.cookies.get("lang"))
    return RedirectResponse(url=f"/dashboard?lang={lang}")


@router.get("/dashboard")
async def dashboard(request: Request):
    context = base_context(request, "AI Agent Dashboard", "dashboard")
    context.update(
        {
            "activity_items": store.get_activity_slice(limit=3),
            "active_tickets": len(store.tickets),
            "pending_renewals": 8,
            "renewal_countdown_days": 62,
            "actions_today": 47,
            "response_time": 8,
            "maintenance_pipeline": [
                "Reported",
                "Assigned",
                "En Route",
                "In Progress",
                "Resolved",
            ],
            "renewal_pipeline": [
                "RERA Check",
                "Offer Draft",
                "Manager Approval",
                "Tenant Sent",
                "Ejari Ready",
            ],
        }
    )
    return templates.TemplateResponse("pages/dashboard.html", context)


@router.get("/maintenance/reasoning")
async def maintenance_reasoning(request: Request):
    context = base_context(request, "Maintenance Agent Reasoning", "maintenance")
    context.update(
        {
            "steps": [
                ("🧠", "14:31", "Analyzed message -> Detected: Maintenance (HVAC)"),
                ("📜", "14:31", "Checked tenant history -> No previous AC issues"),
                ("🔎", "14:32", "Searched 5 vendors -> Filtered by <2hr response, Al Barsha"),
                ("✅", "14:32", "Selected vendor: Ahmad HVAC (4.8★, available now)"),
                ("💬", "14:32", "Notified tenant (Arabic) + vendor (WhatsApp)"),
                ("🎫", "14:32", "Created ticket #M-1247"),
            ]
        }
    )
    return templates.TemplateResponse("pages/maintenance_reasoning.html", context)


@router.get("/maintenance/vendors")
async def maintenance_vendors(request: Request):
    context = base_context(request, "Vendor Assignment", "maintenance")
    context.update(
        {
            "vendors": store.get_vendors(),
            "ticket": store.get_ticket("M-1247"),
        }
    )
    return templates.TemplateResponse("pages/maintenance_vendors.html", context)


@router.get("/maintenance/ticket/{ticket_id}")
async def maintenance_ticket(request: Request, ticket_id: str):
    context = base_context(request, f"Ticket {ticket_id}", "maintenance")
    context.update({"ticket": store.get_ticket(ticket_id)})
    return templates.TemplateResponse("pages/maintenance_ticket.html", context)


@router.get("/renewals/pipeline")
async def renewals_pipeline(request: Request):
    context = base_context(request, "Renewal Pipeline", "renewals")
    context.update({"buckets": store.get_renewals_by_stage()})
    return templates.TemplateResponse("pages/renewals_pipeline.html", context)


@router.get("/renewals/rera/{unit_id}")
async def renewals_rera(request: Request, unit_id: str):
    context = base_context(request, "RERA Compliance Engine", "renewals")
    renewal = store.get_renewal(unit_id)
    analysis = store.calculate_rera(unit_id, proposed_rent_aed=87000)
    context.update({"renewal": renewal, "analysis": analysis, "unit_id": unit_id, "proposed_rent": 87000})
    return templates.TemplateResponse("pages/renewals_rera.html", context)


@router.get("/renewals/offer/{unit_id}")
async def renewals_offer(request: Request, unit_id: str):
    context = base_context(request, "AI Renewal Offer", "renewals")
    context.update(
        {
            "renewal": store.get_renewal(unit_id),
            "contract": store.get_contract(unit_id),
        }
    )
    return templates.TemplateResponse("pages/renewals_offer.html", context)


@router.get("/renewals/communication/{tenant_id}")
async def renewals_communication(request: Request, tenant_id: str):
    context = base_context(request, "Tenant Renewal Communication", "renewals")
    context.update({"tenant_id": tenant_id})
    return templates.TemplateResponse("pages/renewals_communication.html", context)


@router.get("/ai/multi-issue")
async def multi_issue(request: Request):
    context = base_context(request, "Multi-Issue Agent Intelligence", "dashboard")
    return templates.TemplateResponse("pages/multi_issue.html", context)


@router.get("/properties/control-panel")
async def properties_control_panel(request: Request):
    context = base_context(request, "Property Manager Control Panel", "properties")
    units = [
        {
            "unit": f"U-{100 + i}",
            "building": ["Al Barsha Heights", "JBR Residence", "Marina View"][i % 3],
            "status": ["Occupied", "Pending Renewal", "Maintenance"][i % 3],
            "renewal_timeline": ["90+", "60-90", "30-60", "<30"][i % 4],
        }
        for i in range(1, 51)
    ]
    context.update({"units": units})
    return templates.TemplateResponse("pages/properties_control_panel.html", context)


@router.get("/vendors/compliance")
async def vendors_compliance(request: Request):
    context = base_context(request, "Vendor Compliance Tracking", "vendors")
    context.update({"vendors": store.get_vendors(), "compliance": store.compliance})
    return templates.TemplateResponse("pages/vendors_compliance.html", context)


@router.get("/foundations")
async def foundations(request: Request):
    context = base_context(request, "Style Guide & Architecture", "settings")
    return templates.TemplateResponse("pages/foundations.html", context)


@router.get("/mobile/whatsapp")
async def mobile_whatsapp(request: Request):
    context = base_context(request, "Mobile WhatsApp Intake", "maintenance")
    return templates.TemplateResponse("pages/mobile_whatsapp.html", context)


@router.get("/mobile/dashboard")
async def mobile_dashboard(request: Request):
    context = base_context(request, "Mobile Manager Dashboard", "dashboard")
    return templates.TemplateResponse("pages/mobile_dashboard.html", context)


@router.get("/mobile/ticket/{ticket_id}")
async def mobile_ticket(request: Request, ticket_id: str):
    context = base_context(request, "Mobile Ticket Status", "maintenance")
    context.update({"ticket": store.get_ticket(ticket_id)})
    return templates.TemplateResponse("pages/mobile_ticket.html", context)


@router.get("/analytics")
async def analytics(request: Request):
    context = base_context(request, "Analytics", "analytics")
    return templates.TemplateResponse("pages/analytics_placeholder.html", context)


@router.get("/settings")
async def settings(request: Request):
    context = base_context(request, "Settings", "settings")
    return templates.TemplateResponse("pages/settings_placeholder.html", context)
