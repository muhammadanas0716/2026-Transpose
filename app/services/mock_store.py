from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Literal


StatusType = Literal["Active", "Processing", "Idle"]


@dataclass
class AgentState:
    status: StatusType
    actions_today: int
    response_time_seconds: int


@dataclass
class ActivityItem:
    text: str
    timestamp: str


@dataclass
class Ticket:
    ticket_id: str
    title: str
    unit: str
    area: str
    statuses: list[str]
    status_index: int
    sla_minutes_remaining: int
    tenant_name: str
    vendor_name: str
    priority: str
    notes: str


@dataclass
class Vendor:
    vendor_id: str
    name: str
    specialty: str
    area: str
    availability: Literal["available", "busy"]
    response_minutes: int
    rating: float
    jobs_completed: int
    ai_recommended: bool
    latitude: float
    longitude: float
    license_days_left: int
    insurance_valid: bool
    emirates_id_verified: bool
    trade_license_verified: bool


@dataclass
class RenewalCase:
    unit: str
    tenant_name: str
    current_rent_aed: int
    expiry_date: str
    days_out: int
    stage: str
    ai_status: str
    area: str
    bedrooms: str
    market_average_aed: int
    max_allowed_increase_pct: float


@dataclass
class ReraAnalysis:
    current_rent_aed: int
    market_average_aed: int
    your_vs_market_pct: float
    max_allowed_increase_pct: float
    recommended_rent_aed: int
    compliant: bool
    updated_at: str
    source: str


@dataclass
class ContractDraft:
    contract_id: str
    tenant_name: str
    unit: str
    start_date: str
    end_date: str
    rent_aed: int
    generated_seconds: int


@dataclass
class ComplianceRecord:
    vendor_name: str
    emirates_id: bool
    trade_license: bool
    insurance: bool
    ai_score: int
    alert: str


@dataclass
class ChequeSchedule:
    unit: str
    cheque_dates: list[str]
    cheque_amounts_aed: list[int]


@dataclass
class MockStore:
    agent_status_cycle: list[StatusType] = field(default_factory=lambda: ["Active", "Processing", "Idle"])
    status_cursor: int = 0
    activity_cursor: int = 0
    activity_log: list[ActivityItem] = field(default_factory=list)
    tickets: dict[str, Ticket] = field(default_factory=dict)
    vendors: dict[str, Vendor] = field(default_factory=dict)
    renewals: dict[str, RenewalCase] = field(default_factory=dict)
    contracts: dict[str, ContractDraft] = field(default_factory=dict)
    compliance: list[ComplianceRecord] = field(default_factory=list)
    cheque_schedules: list[ChequeSchedule] = field(default_factory=list)

    def seed(self) -> None:
        self.activity_log = [
            ActivityItem("Checking RERA rental index for Unit 402...", "14:32"),
            ActivityItem("Assigning plumber to Al Barsha South...", "14:33"),
            ActivityItem("Generating renewal contract for Tenant Sara Ahmad...", "14:34"),
            ActivityItem("Syncing Ejari registration data for Marina Tower A-809...", "14:35"),
            ActivityItem("Escalating electrical ticket #M-1289 to senior vendor...", "14:36"),
            ActivityItem("Preparing 90-day renewal notices for JBR portfolio...", "14:37"),
        ]

        self.tickets = {
            "M-1247": Ticket(
                ticket_id="M-1247",
                title="AC Repair",
                unit="Unit 402",
                area="Al Barsha",
                statuses=["Reported", "Assigned", "En Route", "In Progress", "Resolved"],
                status_index=2,
                sla_minutes_remaining=83,
                tenant_name="Sara Ahmad",
                vendor_name="Ahmad HVAC",
                priority="Medium",
                notes="Priority: Medium. Tenant comfort issue. No safety risk.",
            ),
            "M-1289": Ticket(
                ticket_id="M-1289",
                title="Plumbing Leak",
                unit="Unit 809",
                area="Dubai Marina",
                statuses=["Reported", "Assigned", "En Route", "In Progress", "Resolved"],
                status_index=1,
                sla_minutes_remaining=57,
                tenant_name="Rashid Khan",
                vendor_name="Marina Plumbers",
                priority="High",
                notes="Potential water damage risk. Escalated for immediate attendance.",
            ),
        }

        self.vendors = {
            "V-HVAC-01": Vendor(
                vendor_id="V-HVAC-01",
                name="Ahmad HVAC",
                specialty="HVAC",
                area="Al Barsha",
                availability="available",
                response_minutes=38,
                rating=4.8,
                jobs_completed=231,
                ai_recommended=True,
                latitude=25.103,
                longitude=55.193,
                license_days_left=186,
                insurance_valid=True,
                emirates_id_verified=True,
                trade_license_verified=True,
            ),
            "V-PLB-11": Vendor(
                vendor_id="V-PLB-11",
                name="Marina Plumbers",
                specialty="Plumbing",
                area="Dubai Marina",
                availability="busy",
                response_minutes=55,
                rating=4.6,
                jobs_completed=198,
                ai_recommended=False,
                latitude=25.081,
                longitude=55.141,
                license_days_left=15,
                insurance_valid=True,
                emirates_id_verified=True,
                trade_license_verified=True,
            ),
            "V-ELC-02": Vendor(
                vendor_id="V-ELC-02",
                name="JBR Electric",
                specialty="Electrical",
                area="JBR",
                availability="available",
                response_minutes=42,
                rating=4.7,
                jobs_completed=164,
                ai_recommended=False,
                latitude=25.079,
                longitude=55.136,
                license_days_left=244,
                insurance_valid=False,
                emirates_id_verified=True,
                trade_license_verified=True,
            ),
            "V-GEN-05": Vendor(
                vendor_id="V-GEN-05",
                name="Emirates Facility Team",
                specialty="General",
                area="Al Barsha",
                availability="available",
                response_minutes=61,
                rating=4.5,
                jobs_completed=422,
                ai_recommended=False,
                latitude=25.111,
                longitude=55.207,
                license_days_left=92,
                insurance_valid=True,
                emirates_id_verified=True,
                trade_license_verified=True,
            ),
        }

        self.renewals = {
            "U-402": RenewalCase(
                unit="Unit 402",
                tenant_name="Sara Ahmad",
                current_rent_aed=85000,
                expiry_date="15/04/2026",
                days_out=62,
                stage="60-90 Days",
                ai_status="RERA check pending",
                area="Al Barsha South",
                bedrooms="2BR apartment",
                market_average_aed=82000,
                max_allowed_increase_pct=4.2,
            ),
            "U-809": RenewalCase(
                unit="Unit 809",
                tenant_name="Ahmed Farooq",
                current_rent_aed=120000,
                expiry_date="29/03/2026",
                days_out=45,
                stage="30-60 Days",
                ai_status="Offer ready",
                area="Dubai Marina",
                bedrooms="2BR apartment",
                market_average_aed=118000,
                max_allowed_increase_pct=5.0,
            ),
            "U-111": RenewalCase(
                unit="Unit 111",
                tenant_name="Nadia Omar",
                current_rent_aed=98000,
                expiry_date="21/02/2026",
                days_out=14,
                stage="<30 Days",
                ai_status="Sent to tenant",
                area="JBR",
                bedrooms="1BR apartment",
                market_average_aed=101000,
                max_allowed_increase_pct=3.5,
            ),
            "U-210": RenewalCase(
                unit="Unit 210",
                tenant_name="Zaid Malik",
                current_rent_aed=77000,
                expiry_date="28/07/2026",
                days_out=166,
                stage="90+ Days Out",
                ai_status="RERA check pending",
                area="Al Barsha",
                bedrooms="1BR apartment",
                market_average_aed=79000,
                max_allowed_increase_pct=4.0,
            ),
        }

        self.contracts = {
            "U-402": ContractDraft(
                contract_id="R-402-2026",
                tenant_name="Sara Ahmad",
                unit="Unit 402",
                start_date="16/04/2026",
                end_date="15/04/2027",
                rent_aed=87000,
                generated_seconds=12,
            )
        }

        self.compliance = [
            ComplianceRecord(
                vendor_name="Ahmad HVAC",
                emirates_id=True,
                trade_license=True,
                insurance=True,
                ai_score=93,
                alert="None",
            ),
            ComplianceRecord(
                vendor_name="Marina Plumbers",
                emirates_id=True,
                trade_license=True,
                insurance=True,
                ai_score=89,
                alert="Trade license expires in 15 days",
            ),
            ComplianceRecord(
                vendor_name="JBR Electric",
                emirates_id=True,
                trade_license=True,
                insurance=False,
                ai_score=77,
                alert="Insurance renewal required",
            ),
        ]

        self.cheque_schedules = [
            ChequeSchedule(
                unit="Unit 402",
                cheque_dates=["16/04/2026", "16/07/2026", "16/10/2026", "16/01/2027"],
                cheque_amounts_aed=[21750, 21750, 21750, 21750],
            )
        ]

    def get_agent_state(self) -> AgentState:
        self.status_cursor = (self.status_cursor + 1) % len(self.agent_status_cycle)
        status = self.agent_status_cycle[self.status_cursor]
        return AgentState(status=status, actions_today=47 + self.status_cursor, response_time_seconds=8)

    def get_activity_slice(self, limit: int = 3) -> list[ActivityItem]:
        items: list[ActivityItem] = []
        for offset in range(limit):
            idx = (self.activity_cursor + offset) % len(self.activity_log)
            items.append(self.activity_log[idx])
        self.activity_cursor = (self.activity_cursor + 1) % len(self.activity_log)
        return items

    def get_ticket(self, ticket_id: str) -> Ticket:
        return self.tickets[ticket_id]

    def get_vendors(self) -> list[Vendor]:
        return list(self.vendors.values())

    def assign_vendor(self, ticket_id: str, vendor_id: str) -> tuple[Ticket, Vendor]:
        ticket = self.tickets[ticket_id]
        vendor = self.vendors[vendor_id]
        ticket.vendor_name = vendor.name
        if ticket.status_index < 1:
            ticket.status_index = 1
        vendor.availability = "busy"
        for existing in self.vendors.values():
            existing.ai_recommended = existing.vendor_id == vendor_id
        self.activity_log.insert(
            0,
            ActivityItem(
                text=f"AI-assisted assignment: {vendor.name} -> {ticket.ticket_id} ({ticket.unit})",
                timestamp=datetime.now().strftime("%H:%M"),
            ),
        )
        return ticket, vendor

    def advance_ticket(self, ticket_id: str) -> Ticket:
        ticket = self.tickets[ticket_id]
        if ticket.status_index < len(ticket.statuses) - 1:
            ticket.status_index += 1
        if ticket.sla_minutes_remaining > 0:
            ticket.sla_minutes_remaining -= 2
        return ticket

    def get_renewals_by_stage(self) -> dict[str, list[RenewalCase]]:
        buckets: dict[str, list[RenewalCase]] = {
            "90+ Days Out": [],
            "60-90 Days": [],
            "30-60 Days": [],
            "<30 Days": [],
        }
        for renewal in self.renewals.values():
            buckets.setdefault(renewal.stage, []).append(renewal)
        return buckets

    def get_renewal(self, unit_id: str) -> RenewalCase:
        return self.renewals[unit_id]

    def calculate_rera(self, unit_id: str, proposed_rent_aed: int) -> ReraAnalysis:
        renewal = self.get_renewal(unit_id)
        market_avg = renewal.market_average_aed
        vs_market = ((proposed_rent_aed - market_avg) / market_avg) * 100
        max_allowed_rent = int(round(renewal.current_rent_aed * (1 + renewal.max_allowed_increase_pct / 100)))
        recommended = min(max_allowed_rent, int(round(market_avg * 1.06)))
        return ReraAnalysis(
            current_rent_aed=renewal.current_rent_aed,
            market_average_aed=market_avg,
            your_vs_market_pct=round(vs_market, 1),
            max_allowed_increase_pct=renewal.max_allowed_increase_pct,
            recommended_rent_aed=recommended,
            compliant=proposed_rent_aed <= max_allowed_rent,
            updated_at="Feb 7, 2026, 2:34 PM",
            source="Dubai Land Department - Rental Index 2026",
        )

    def get_contract(self, unit_id: str) -> ContractDraft:
        return self.contracts[unit_id]

    def bulk_process_renewals(self) -> str:
        ready = 0
        for renewal in self.renewals.values():
            if renewal.ai_status == "RERA check pending":
                renewal.ai_status = "Offer ready"
                ready += 1
        return f"Processed {ready} renewal cases. Manager review queue updated."

    def send_notices(self) -> str:
        count = sum(1 for renewal in self.renewals.values() if renewal.days_out >= 90)
        return f"Sent {count} automated 90-day notices. Awaiting manager sign-off logs."


store = MockStore()
store.seed()
