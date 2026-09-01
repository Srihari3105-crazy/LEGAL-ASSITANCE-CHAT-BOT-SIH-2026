"""
PMFBY Assistant Module — Crop Insurance Calculator & Claims Guidance

Provides PMFBY premium calculation, eligibility checking, claim filing guidance,
and risk coverage information for cooperative members.

Author: SahkarSetu Team
Version: 1.0.0
"""

import logging
from dataclasses import dataclass, field
from typing import Optional, Dict, List, Any
from enum import Enum

logger = logging.getLogger(__name__)


class Season(str, Enum):
    KHARIF = "kharif"
    RABI = "rabi"
    COMMERCIAL = "commercial"


class CropCategory(str, Enum):
    FOOD_GRAIN = "food_grain"
    OILSEED = "oilseed"
    PULSE = "pulse"
    COMMERCIAL = "commercial"
    HORTICULTURAL = "horticultural"


# Premium rates as per PMFBY guidelines
PREMIUM_RATES = {
    Season.KHARIF: 0.02,       # 2% of sum insured
    Season.RABI: 0.015,        # 1.5% of sum insured
    Season.COMMERCIAL: 0.05,   # 5% of sum insured
}

# Scale of Finance (typical sum insured per hectare in ₹) — representative values
SCALE_OF_FINANCE = {
    "paddy": {"kharif": 45000, "rabi": 50000},
    "wheat": {"kharif": 0, "rabi": 55000},
    "maize": {"kharif": 30000, "rabi": 35000},
    "cotton": {"kharif": 50000, "rabi": 0},
    "sugarcane": {"kharif": 120000, "rabi": 120000},
    "mustard": {"kharif": 0, "rabi": 40000},
    "groundnut": {"kharif": 45000, "rabi": 0},
    "soybean": {"kharif": 40000, "rabi": 0},
    "potato": {"kharif": 0, "rabi": 60000},
    "onion": {"kharif": 80000, "rabi": 80000},
    "tomato": {"kharif": 70000, "rabi": 70000},
    "chana": {"kharif": 0, "rabi": 35000},
    "bajra": {"kharif": 25000, "rabi": 0},
    "jowar": {"kharif": 25000, "rabi": 28000},
    "tur_dal": {"kharif": 35000, "rabi": 0},
    "urad_dal": {"kharif": 30000, "rabi": 0},
    "moong_dal": {"kharif": 30000, "rabi": 0},
}


@dataclass
class PremiumCalculation:
    """Result of PMFBY premium calculation."""
    crop_name: str
    season: str
    area_hectares: float
    sum_insured: float
    premium_rate: float
    farmer_premium: float
    government_subsidy: float
    actual_premium_estimate: float
    is_eligible: bool = True
    notes: List[str] = field(default_factory=list)


@dataclass
class ClaimGuidance:
    """Structured claim filing guidance."""
    steps: List[str]
    documents_required: List[str]
    contact_channels: List[str]
    important_deadlines: Dict[str, str]
    tips: List[str]


class PMFBYAssistant:
    """PMFBY crop insurance calculator and guidance engine."""

    def calculate_premium(
        self,
        crop_name: str,
        season: str,
        area_hectares: float,
        state: str = "general"
    ) -> PremiumCalculation:
        """Calculate PMFBY premium for given crop, season, and area."""
        crop_key = crop_name.lower().strip().replace(" ", "_")
        season_key = season.lower().strip()

        # Determine season enum
        if season_key in ("kharif", "monsoon"):
            season_enum = Season.KHARIF
        elif season_key in ("rabi", "winter"):
            season_enum = Season.RABI
        else:
            season_enum = Season.COMMERCIAL

        # Get premium rate
        premium_rate = PREMIUM_RATES[season_enum]

        # Get sum insured per hectare
        notes = []
        if crop_key in SCALE_OF_FINANCE:
            sof = SCALE_OF_FINANCE[crop_key]
            si_per_ha = sof.get(season_key, 0)
            if si_per_ha == 0:
                # Crop not typically grown in this season
                si_per_ha = max(sof.values())  # Use available season
                notes.append(
                    f"Note: {crop_name} is not typically grown in {season} season. "
                    f"Using alternate season's sum insured."
                )
        else:
            # Default average sum insured
            si_per_ha = 40000
            notes.append(
                f"Note: Using average sum insured of ₹40,000/hectare for {crop_name}. "
                f"Actual amount depends on your state's Scale of Finance notification."
            )

        # Calculate
        total_sum_insured = si_per_ha * area_hectares
        farmer_premium = total_sum_insured * premium_rate
        # Actual premium is typically 4-5x the farmer's share
        actual_premium_estimate = total_sum_insured * premium_rate * 4
        government_subsidy = actual_premium_estimate - farmer_premium

        notes.append(
            "Final premium and sum insured depend on your state's notification. "
            "Contact your bank, PACS, or CSC for exact amounts."
        )

        return PremiumCalculation(
            crop_name=crop_name,
            season=season,
            area_hectares=area_hectares,
            sum_insured=total_sum_insured,
            premium_rate=premium_rate,
            farmer_premium=round(farmer_premium, 2),
            government_subsidy=round(government_subsidy, 2),
            actual_premium_estimate=round(actual_premium_estimate, 2),
            notes=notes,
        )

    def get_claim_guidance(self, language: str = "en") -> ClaimGuidance:
        """Get step-by-step claim filing guidance."""
        if language == "hi":
            return ClaimGuidance(
                steps=[
                    "फसल नुकसान होने के 72 घंटे के अंदर सूचना दें",
                    "Crop Insurance App, टोल-फ्री नंबर 14447, बैंक शाखा, या PACS में रिपोर्ट करें",
                    "किसान का नाम, पॉलिसी नंबर, फसल का नाम, नुकसान की तारीख और प्रकार बताएं",
                    "बीमा कंपनी 48 घंटे में सर्वेयर भेजेगी",
                    "फसल कटाई प्रयोग (CCE) के आधार पर दावा राशि तय होगी",
                    "दावा राशि 2 महीने में बैंक खाते में जमा होगी",
                ],
                documents_required=[
                    "आधार कार्ड",
                    "बैंक पासबुक",
                    "भूमि रिकॉर्ड (खसरा/खतौनी/7-12)",
                    "बुवाई प्रमाण पत्र",
                    "फसल नुकसान की फोटो",
                ],
                contact_channels=[
                    "Crop Insurance App (Android/iOS)",
                    "टोल-फ्री नंबर: 14447",
                    "बैंक शाखा",
                    "PACS कार्यालय",
                    "CSC (Common Service Centre)",
                ],
                important_deadlines={
                    "नुकसान सूचना": "72 घंटे के अंदर",
                    "दावा निपटान": "फसल कटाई डेटा प्राप्ति के 2 महीने अंदर",
                    "शिकायत": "दावा अस्वीकृति के 30 दिन अंदर",
                },
                tips=[
                    "फसल नुकसान की फोटो और वीडियो तुरंत लें",
                    "GPS location के साथ फोटो लें (फोन की लोकेशन ON रखें)",
                    "बीमा कंपनी का नाम और पॉलिसी नंबर संभाल कर रखें",
                    "PACS से मदद लें — वे दावा प्रक्रिया में सहायता करते हैं",
                ],
            )
        else:
            return ClaimGuidance(
                steps=[
                    "Report crop loss within 72 hours of the calamity",
                    "Report through: Crop Insurance App, toll-free 14447, bank branch, PACS, or CSC",
                    "Provide: farmer name, policy number, crop name, date and nature of loss",
                    "Insurance company sends surveyor within 48 hours",
                    "Claim amount determined by Crop Cutting Experiments (CCE)",
                    "Claim credited to bank account within 2 months of harvest data submission",
                ],
                documents_required=[
                    "Aadhaar Card",
                    "Bank Passbook",
                    "Land Records (Khasra/Khatauni/7-12 extract)",
                    "Sowing Certificate from Patwari/Lekhpal",
                    "Photographs of crop damage",
                ],
                contact_channels=[
                    "Crop Insurance App (Android/iOS)",
                    "Toll-free Number: 14447",
                    "Bank Branch",
                    "PACS Office",
                    "CSC (Common Service Centre)",
                ],
                important_deadlines={
                    "Loss Intimation": "Within 72 hours",
                    "Claim Settlement": "Within 2 months of harvest data",
                    "Grievance Filing": "Within 30 days of claim rejection",
                },
                tips=[
                    "Take photos and videos of crop damage immediately",
                    "Capture photos with GPS location enabled on phone",
                    "Keep insurance company name and policy number safe",
                    "Take help from PACS — they assist with claim process",
                ],
            )

    def get_risks_covered(self) -> Dict[str, List[str]]:
        """Get PMFBY risk coverage information."""
        return {
            "covered": [
                "Prevented Sowing/Planting (25% of sum insured)",
                "Standing Crop: drought, flood, pest/disease, fire, storm, hailstorm, cyclone",
                "Post-Harvest Losses: coverage up to 14 days for cut-and-spread crops",
                "Localized Calamities: hailstorm, landslide, inundation affecting individual farms",
                "Mid-season adversity add-on coverage",
            ],
            "not_covered": [
                "War and nuclear risks",
                "Riot and civil disturbance",
                "Theft and malicious damage",
                "Damage by domestic or wild animals",
                "Losses due to use of unapproved seeds",
            ],
        }

    def check_eligibility(
        self, is_farmer: bool, has_land: bool, crop_notified: bool
    ) -> Dict[str, Any]:
        """Check basic PMFBY eligibility."""
        eligible = is_farmer and crop_notified
        reasons = []
        if not is_farmer:
            reasons.append("Must be a farmer (landowner, sharecropper, or tenant)")
        if not crop_notified:
            reasons.append("Crop must be notified in your area for the current season")

        return {
            "eligible": eligible,
            "enrollment_type": "voluntary" if not has_land else "voluntary",
            "reasons": reasons if not eligible else [],
            "note": (
                "Both loanee and non-loanee farmers are eligible. "
                "Enrollment is voluntary since Kharif 2020."
            ),
        }
