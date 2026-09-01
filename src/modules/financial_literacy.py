"""
Financial Literacy Module — Cooperative Financial Education Tools

Provides EMI calculators, savings comparisons, cooperative banking guidance,
and KCC information for rural cooperative members.

Author: SahkarSetu Team
Version: 1.0.0
"""

import logging
import math
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional

logger = logging.getLogger(__name__)


@dataclass
class EMIResult:
    """Loan EMI calculation result."""
    principal: float
    annual_rate: float
    tenure_months: int
    monthly_emi: float
    total_payment: float
    total_interest: float
    effective_rate: float  # After interest subvention
    subvention_savings: float


@dataclass
class SavingsComparison:
    """Comparison of savings options."""
    options: List[Dict[str, Any]]
    recommended: str
    recommendation_reason: str


class FinancialLiteracyEngine:
    """Financial literacy tools for cooperative members."""

    # Current interest rates (representative)
    CROP_LOAN_RATE = 7.0          # 7% p.a.
    SUBVENTION_RATE = 3.0          # 3% subvention for timely repayment
    EFFECTIVE_CROP_RATE = 4.0      # Effective rate = 7% - 3% = 4%
    KCC_LIMIT_PER_HA = 300000     # ₹3 lakh per hectare (typical KCC limit)
    COOPERATIVE_FD_RATE = 7.5      # Cooperative bank FD rate
    COMMERCIAL_FD_RATE = 6.5       # Commercial bank FD rate
    POST_OFFICE_RD_RATE = 6.7      # Post office RD rate

    def calculate_emi(
        self,
        principal: float,
        annual_rate: float = None,
        tenure_months: int = 12,
        is_crop_loan: bool = True,
    ) -> EMIResult:
        """Calculate EMI for cooperative/PACS loan.

        For crop loans through PACS, applies government interest subvention.
        """
        if annual_rate is None:
            annual_rate = self.CROP_LOAN_RATE if is_crop_loan else 10.0

        # Effective rate with subvention
        effective_rate = annual_rate
        subvention = 0.0
        if is_crop_loan and annual_rate == self.CROP_LOAN_RATE:
            effective_rate = self.EFFECTIVE_CROP_RATE
            subvention = principal * (self.SUBVENTION_RATE / 100) * (tenure_months / 12)

        monthly_rate = effective_rate / 100 / 12

        if monthly_rate == 0:
            monthly_emi = principal / tenure_months
        else:
            monthly_emi = principal * monthly_rate * (1 + monthly_rate) ** tenure_months / (
                (1 + monthly_rate) ** tenure_months - 1
            )

        total_payment = monthly_emi * tenure_months
        total_interest = total_payment - principal

        return EMIResult(
            principal=principal,
            annual_rate=annual_rate,
            tenure_months=tenure_months,
            monthly_emi=round(monthly_emi, 2),
            total_payment=round(total_payment, 2),
            total_interest=round(total_interest, 2),
            effective_rate=effective_rate,
            subvention_savings=round(subvention, 2),
        )

    def calculate_kcc_limit(
        self, land_area_hectares: float, crop_name: str = "general"
    ) -> Dict[str, Any]:
        """Estimate KCC credit limit based on land area and crop."""
        # KCC limit = Scale of Finance × Land Area × 1.1 (10% post-harvest + consumption)
        from .pmfby_assistant import SCALE_OF_FINANCE

        crop_key = crop_name.lower().strip().replace(" ", "_")
        if crop_key in SCALE_OF_FINANCE:
            sof_values = SCALE_OF_FINANCE[crop_key]
            sof = max(sof_values.values())
        else:
            sof = 40000  # Default

        base_limit = sof * land_area_hectares
        # Add 10% for post-harvest + consumption needs
        kcc_limit = base_limit * 1.1
        # Add 20% for farm maintenance
        total_limit = kcc_limit * 1.2

        return {
            "crop": crop_name,
            "land_area_hectares": land_area_hectares,
            "scale_of_finance_per_ha": sof,
            "base_crop_loan": round(base_limit, 2),
            "with_post_harvest": round(kcc_limit, 2),
            "total_kcc_limit": round(min(total_limit, 300000), 2),  # Cap at ₹3 lakh for subvention
            "interest_rate": f"{self.CROP_LOAN_RATE}% (effective {self.EFFECTIVE_CROP_RATE}% with subvention)",
            "notes": [
                "KCC limit up to ₹3 lakh eligible for interest subvention (effective 4% p.a.)",
                "Limit reviewed and enhanced by 10% annually",
                "Includes crop loan + post-harvest needs + consumption",
                "Apply at your nearest PACS or bank branch",
            ],
        }

    def compare_savings(self, amount: float, years: int = 5) -> SavingsComparison:
        """Compare savings/investment options for cooperative members."""
        options = []

        # 1. Cooperative Bank FD
        coop_fd = amount * (1 + self.COOPERATIVE_FD_RATE / 100) ** years
        options.append({
            "name": "Cooperative Bank Fixed Deposit",
            "rate": f"{self.COOPERATIVE_FD_RATE}% p.a.",
            "maturity_value": round(coop_fd, 2),
            "interest_earned": round(coop_fd - amount, 2),
            "risk": "Low",
            "liquidity": "Premature withdrawal with penalty",
            "tax": "TDS applicable above ₹40,000/year interest",
        })

        # 2. Commercial Bank FD
        comm_fd = amount * (1 + self.COMMERCIAL_FD_RATE / 100) ** years
        options.append({
            "name": "Commercial Bank Fixed Deposit",
            "rate": f"{self.COMMERCIAL_FD_RATE}% p.a.",
            "maturity_value": round(comm_fd, 2),
            "interest_earned": round(comm_fd - amount, 2),
            "risk": "Low",
            "liquidity": "Premature withdrawal with penalty",
            "tax": "TDS applicable above ₹40,000/year interest",
        })

        # 3. Post Office RD (monthly)
        monthly = amount / (years * 12)
        rd_rate_monthly = self.POST_OFFICE_RD_RATE / 100 / 4  # Quarterly compounding
        # Approximate RD maturity
        n = years * 12
        rd_maturity = monthly * n + (monthly * n * (n + 1) * rd_rate_monthly / 24)
        options.append({
            "name": "Post Office Recurring Deposit",
            "rate": f"{self.POST_OFFICE_RD_RATE}% p.a. (quarterly compounding)",
            "monthly_deposit": round(monthly, 2),
            "maturity_value": round(rd_maturity, 2),
            "interest_earned": round(rd_maturity - amount, 2),
            "risk": "Very Low (Government backed)",
            "liquidity": "After 1 year",
            "tax": "Taxable as per income tax slab",
        })

        # 4. PM Jeevan Jyoti Bima Yojana
        options.append({
            "name": "PM Jeevan Jyoti Bima Yojana (Life Insurance)",
            "premium": "₹436/year",
            "coverage": "₹2,00,000 life cover",
            "risk": "No investment risk (pure insurance)",
            "eligibility": "Age 18-55 years, savings bank account",
            "note": "Can be enrolled through PACS banking correspondent",
        })

        # 5. Cooperative Share Deposit
        options.append({
            "name": "Cooperative Society Share Capital",
            "rate": "Dividend based (typically 10-15%)",
            "benefits": "Voting rights in cooperative + dividend income",
            "risk": "Medium (depends on cooperative performance)",
            "liquidity": "Withdrawal on leaving membership",
            "note": "Required for cooperative membership and loan eligibility",
        })

        return SavingsComparison(
            options=options,
            recommended="Cooperative Bank Fixed Deposit",
            recommendation_reason=(
                "Cooperative bank FDs typically offer higher rates than commercial banks "
                f"({self.COOPERATIVE_FD_RATE}% vs {self.COMMERCIAL_FD_RATE}%). "
                "Combined with cooperative share deposits for dividend income "
                "and PM Jeevan Jyoti for life cover, this provides a balanced approach."
            ),
        )

    def get_financial_tips(self, language: str = "en") -> List[str]:
        """Get financial literacy tips for cooperative members."""
        if language == "hi":
            return [
                "हमेशा बैंक/PACS से ही लोन लें — महाजन से कभी न लें",
                "समय पर लोन चुकाएं — 3% ब्याज छूट मिलेगी (7% → 4%)",
                "KCC (किसान क्रेडिट कार्ड) बनवाएं — एक ही कार्ड से सब लोन",
                "PMFBY से फसल बीमा जरूर कराएं — प्रीमियम बहुत कम है",
                "बचत खाता आधार से लिंक रखें — DBT लाभ सीधे मिलेगा",
                "SHG (स्वयं सहायता समूह) से जुड़ें — छोटे लोन और बचत में मदद",
                "लोन लेने से पहले ब्याज दर समझें — सिंपल vs कंपाउंड",
                "फसल लोन को गैर-कृषि कार्य में न लगाएं",
                "अगर लोन नहीं चुका पा रहे तो बैंक से बात करें — डिफॉल्ट न करें",
                "पोस्ट ऑफिस, सुकन्या, PPF — सुरक्षित बचत के विकल्प हैं",
            ]
        else:
            return [
                "Always borrow from banks/PACS — never from moneylenders",
                "Repay loans on time — get 3% interest subvention (7% → effective 4%)",
                "Get KCC (Kisan Credit Card) — one card for all agricultural credit needs",
                "Always take PMFBY crop insurance — premiums are very low",
                "Keep savings account linked with Aadhaar — for DBT benefits",
                "Join SHG (Self Help Group) — helps with small loans and savings habit",
                "Understand interest rates before taking loan — simple vs compound",
                "Don't use crop loan for non-agricultural purposes",
                "If unable to repay, talk to bank immediately — don't default",
                "Post Office, Sukanya Samriddhi, PPF — safe savings options available",
            ]
