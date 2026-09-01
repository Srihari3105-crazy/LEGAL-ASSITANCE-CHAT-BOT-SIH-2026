"""
PMFBY & Financial Literacy API Routes

REST API endpoints for PMFBY premium calculation, claim guidance,
financial literacy tools, and KCC information.

Author: SahkarSetu Team
Version: 1.0.0
"""

import logging
from typing import Optional

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field

from src.modules.pmfby_assistant import PMFBYAssistant
from src.modules.financial_literacy import FinancialLiteracyEngine

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1", tags=["PACS Services", "Financial Literacy"])

# Initialize modules
pmfby = PMFBYAssistant()
fin_engine = FinancialLiteracyEngine()


# ============================================================================
# PMFBY ROUTES
# ============================================================================

class PremiumRequest(BaseModel):
    crop_name: str = Field(..., description="Name of the crop", examples=["paddy"])
    season: str = Field(..., description="Kharif, Rabi, or Commercial", examples=["kharif"])
    area_hectares: float = Field(..., gt=0, description="Land area in hectares", examples=[2.0])
    state: str = Field(default="general", description="State name (optional)")


class EligibilityRequest(BaseModel):
    is_farmer: bool = Field(..., description="Is the applicant a farmer")
    has_land: bool = Field(default=True, description="Has cultivable land")
    crop_notified: bool = Field(default=True, description="Is crop notified in the area")


@router.post("/pmfby/calculate-premium", tags=["PACS Services"])
async def calculate_premium(req: PremiumRequest):
    """Calculate PMFBY premium for a given crop, season, and area.

    Returns the farmer's share of premium, government subsidy,
    and total sum insured. Uses official Scale of Finance data.
    """
    try:
        result = pmfby.calculate_premium(
            crop_name=req.crop_name,
            season=req.season,
            area_hectares=req.area_hectares,
            state=req.state,
        )
        return {
            "success": True,
            "data": {
                "crop": result.crop_name,
                "season": result.season,
                "area_hectares": result.area_hectares,
                "sum_insured": f"₹{result.sum_insured:,.2f}",
                "premium_rate": f"{result.premium_rate * 100:.1f}%",
                "farmer_premium": f"₹{result.farmer_premium:,.2f}",
                "government_subsidy": f"₹{result.government_subsidy:,.2f}",
                "is_eligible": result.is_eligible,
                "notes": result.notes,
            },
        }
    except Exception as e:
        logger.error(f"Premium calculation failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/pmfby/claim-guidance", tags=["PACS Services"])
async def get_claim_guidance(language: str = Query(default="en", regex="^(en|hi)$")):
    """Get step-by-step PMFBY claim filing guidance.

    Available in Hindi and English. Includes required documents,
    contact channels, and important deadlines.
    """
    guidance = pmfby.get_claim_guidance(language=language)
    return {
        "success": True,
        "data": {
            "steps": guidance.steps,
            "documents_required": guidance.documents_required,
            "contact_channels": guidance.contact_channels,
            "important_deadlines": guidance.important_deadlines,
            "tips": guidance.tips,
        },
    }


@router.get("/pmfby/risks-covered", tags=["PACS Services"])
async def get_risks_covered():
    """Get PMFBY risk coverage information — what's covered and what's not."""
    return {"success": True, "data": pmfby.get_risks_covered()}


@router.post("/pmfby/check-eligibility", tags=["PACS Services"])
async def check_eligibility(req: EligibilityRequest):
    """Check basic PMFBY eligibility for a farmer."""
    result = pmfby.check_eligibility(
        is_farmer=req.is_farmer,
        has_land=req.has_land,
        crop_notified=req.crop_notified,
    )
    return {"success": True, "data": result}


# ============================================================================
# FINANCIAL LITERACY ROUTES
# ============================================================================

class EMIRequest(BaseModel):
    principal: float = Field(..., gt=0, description="Loan amount in ₹", examples=[50000])
    annual_rate: Optional[float] = Field(
        default=None, description="Annual interest rate (%). Uses PACS rate if None."
    )
    tenure_months: int = Field(default=12, gt=0, le=360, description="Loan tenure in months")
    is_crop_loan: bool = Field(default=True, description="Is this a crop loan through PACS")


class KCCRequest(BaseModel):
    land_area_hectares: float = Field(..., gt=0, description="Total cultivable land in hectares")
    crop_name: str = Field(default="general", description="Primary crop name")


class SavingsRequest(BaseModel):
    amount: float = Field(..., gt=0, description="Total savings amount in ₹")
    years: int = Field(default=5, gt=0, le=30, description="Investment period in years")


@router.post("/financial/calculate-emi", tags=["Financial Literacy"])
async def calculate_emi(req: EMIRequest):
    """Calculate EMI for cooperative/PACS loan.

    For crop loans, automatically applies government interest subvention
    (7% → effective 4% for timely repayment).
    """
    try:
        result = fin_engine.calculate_emi(
            principal=req.principal,
            annual_rate=req.annual_rate,
            tenure_months=req.tenure_months,
            is_crop_loan=req.is_crop_loan,
        )
        return {
            "success": True,
            "data": {
                "principal": f"₹{result.principal:,.2f}",
                "annual_rate": f"{result.annual_rate}%",
                "effective_rate": f"{result.effective_rate}%",
                "tenure_months": result.tenure_months,
                "monthly_emi": f"₹{result.monthly_emi:,.2f}",
                "total_payment": f"₹{result.total_payment:,.2f}",
                "total_interest": f"₹{result.total_interest:,.2f}",
                "subvention_savings": f"₹{result.subvention_savings:,.2f}",
                "note": (
                    "Interest subvention of 3% available for timely repayment of crop loans "
                    "up to ₹3 lakh through PACS/banks."
                    if req.is_crop_loan
                    else ""
                ),
            },
        }
    except Exception as e:
        logger.error(f"EMI calculation failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/financial/kcc-limit", tags=["Financial Literacy"])
async def estimate_kcc_limit(req: KCCRequest):
    """Estimate Kisan Credit Card (KCC) credit limit based on land area and crop."""
    try:
        result = fin_engine.calculate_kcc_limit(
            land_area_hectares=req.land_area_hectares,
            crop_name=req.crop_name,
        )
        return {"success": True, "data": result}
    except Exception as e:
        logger.error(f"KCC limit calculation failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/financial/compare-savings", tags=["Financial Literacy"])
async def compare_savings(req: SavingsRequest):
    """Compare savings and investment options for cooperative members.

    Compares cooperative bank FD, commercial bank FD, post office RD,
    insurance schemes, and cooperative share deposits.
    """
    try:
        result = fin_engine.compare_savings(amount=req.amount, years=req.years)
        return {
            "success": True,
            "data": {
                "options": result.options,
                "recommended": result.recommended,
                "recommendation_reason": result.recommendation_reason,
            },
        }
    except Exception as e:
        logger.error(f"Savings comparison failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/financial/tips", tags=["Financial Literacy"])
async def get_financial_tips(language: str = Query(default="en", regex="^(en|hi)$")):
    """Get financial literacy tips for cooperative members in Hindi or English."""
    tips = fin_engine.get_financial_tips(language=language)
    return {"success": True, "data": {"language": language, "tips": tips}}
