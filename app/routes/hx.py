from __future__ import annotations

from urllib.parse import parse_qsl, urlencode, urlparse, urlunparse

from fastapi import APIRouter, Form, Request
from fastapi.responses import HTMLResponse, Response
from fastapi.templating import Jinja2Templates

from app.services.localization import choose_lang, get_pack, normalize_lang
from app.services.mock_store import store


templates = Jinja2Templates(directory="app/templates")
router = APIRouter(prefix="/hx", tags=["htmx"])


def _lang_from_request(request: Request) -> str:
    return choose_lang(request.query_params.get("lang"), request.cookies.get("lang"))


@router.get("/agent/status")
async def agent_status(request: Request):
    lang = _lang_from_request(request)
    labels = get_pack(lang).labels
    return templates.TemplateResponse(
        "partials/agent_status_chip.html",
        {
            "request": request,
            "agent_state": store.get_agent_state(),
            "labels": labels,
            "lang": lang,
        },
    )


@router.get("/agent/activity-feed")
async def activity_feed(request: Request):
    lang = _lang_from_request(request)
    return templates.TemplateResponse(
        "partials/activity_feed.html",
        {
            "request": request,
            "items": store.get_activity_slice(limit=3),
            "lang": lang,
        },
    )


@router.post("/vendors/assign")
async def assign_vendor(
    request: Request,
    ticket_id: str = Form(...),
    vendor_id: str = Form(...),
    lang: str = Form("en"),
):
    ticket, vendor = store.assign_vendor(ticket_id=ticket_id, vendor_id=vendor_id)
    return templates.TemplateResponse(
        "partials/vendor_assignment_result.html",
        {
            "request": request,
            "ticket": ticket,
            "vendor": vendor,
            "lang": normalize_lang(lang),
        },
    )


@router.get("/tickets/{ticket_id}/timeline")
async def ticket_timeline(request: Request, ticket_id: str):
    lang = _lang_from_request(request)
    ticket = store.advance_ticket(ticket_id)
    return templates.TemplateResponse(
        "partials/ticket_timeline.html",
        {
            "request": request,
            "ticket": ticket,
            "lang": lang,
        },
    )


@router.post("/rera/calculate")
async def rera_calculate(
    request: Request,
    unit_id: str = Form(...),
    proposed_rent: int = Form(...),
    lang: str = Form("en"),
):
    analysis = store.calculate_rera(unit_id=unit_id, proposed_rent_aed=proposed_rent)
    return templates.TemplateResponse(
        "partials/rera_result.html",
        {
            "request": request,
            "analysis": analysis,
            "proposed_rent": proposed_rent,
            "lang": normalize_lang(lang),
        },
    )


@router.post("/renewals/bulk-process")
async def bulk_process(request: Request):
    lang = _lang_from_request(request)
    return templates.TemplateResponse(
        "partials/bulk_result_toast.html",
        {
            "request": request,
            "message": store.bulk_process_renewals(),
            "kind": "success",
            "lang": lang,
        },
    )


@router.post("/renewals/send-notices")
async def send_notices(request: Request):
    lang = _lang_from_request(request)
    return templates.TemplateResponse(
        "partials/bulk_result_toast.html",
        {
            "request": request,
            "message": store.send_notices(),
            "kind": "info",
            "lang": lang,
        },
    )


@router.post("/lang/toggle")
async def lang_toggle(request: Request, lang: str = Form(...)):
    normalized = normalize_lang(lang)
    referer = request.headers.get("referer", "/dashboard")
    parsed = urlparse(referer)
    query = dict(parse_qsl(parsed.query))
    query["lang"] = normalized
    new_query = urlencode(query)
    redirect_url = urlunparse(("", "", parsed.path or "/dashboard", "", new_query, ""))

    response = Response(content="", media_type="text/plain")
    response.headers["HX-Redirect"] = redirect_url
    response.set_cookie("lang", normalized, max_age=60 * 60 * 24 * 30)
    return response


@router.get("/mobile/nav/{tab}")
async def mobile_nav(request: Request, tab: str):
    lang = _lang_from_request(request)
    tab = tab.lower()
    tabs = {
        "tickets": {
            "title": "Active Tickets",
            "lines": ["M-1247 AC Repair - In Progress", "M-1289 Plumbing Leak - Assigned"],
        },
        "renewals": {
            "title": "Renewal Queue",
            "lines": ["Unit 402 - 62 days - Offer pending", "Unit 111 - 14 days - Critical follow-up"],
        },
        "ai": {
            "title": "AI Actions",
            "lines": ["Checking RERA index", "Drafting bilingual renewal offer"],
        },
    }
    payload = tabs.get(tab, tabs["tickets"])
    return templates.TemplateResponse(
        "partials/mobile_nav_content.html",
        {
            "request": request,
            "payload": payload,
            "lang": lang,
        },
    )
