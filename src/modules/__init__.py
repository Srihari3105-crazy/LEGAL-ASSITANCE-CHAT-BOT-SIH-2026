"""
SahkarSetu Modules Package

Production-grade modules for cooperative governance operations.

Modules:
    - PMFBYAssistant: Crop insurance calculator and claims guidance
    - FinancialLiteracyEngine: Cooperative banking, EMI, KCC, savings tools
    - Summarizer: Extract structured scheme summaries
    - NoticeDrafter: Generate official cooperative notices & circulars
    - GrievanceRouter: AI-powered cooperative grievance routing
    - SahkarVaani: Voice-native cross-lingual governance
"""

# Cooperative Module 1: PMFBY Assistant
from .pmfby_assistant import (
    PMFBYAssistant,
    PremiumCalculation,
    ClaimGuidance,
    Season,
    CropCategory,
)

# Cooperative Module 2: Financial Literacy Engine
from .financial_literacy import (
    FinancialLiteracyEngine,
    EMIResult,
    SavingsComparison,
)

# Module 3: Summarizer
try:
    from .summarizer import (
        SchemeSummarizer,
        SchemeSummary,
        SummarizerError,
        SchemeNotFoundError,
        LowConfidenceError,
        LLMUnavailableError,
        ValidationError as SummarizerValidationError,
    )
except ImportError:
    pass

# Module 4: Notice Drafter
try:
    from .notice_drafter import (
        NoticeDrafter,
        GovernmentNotice,
        NoticeDrafterError,
        SchemeNotFoundError as NoticeDrafterSchemeNotFoundError,
        LLMUnavailableError as NoticeDrafterLLMUnavailableError,
        ValidationError as NoticeDrafterValidationError,
    )
except ImportError:
    pass

# Module 5: Grievance Router
try:
    from .grievance_router import (
        GrievanceRouter,
        GrievanceRoute,
        GrievanceRouterError,
        InvalidGrievanceError,
        DepartmentUnavailableError,
        LowConfidenceError as RouterLowConfidenceError,
        LLMUnavailableError as RouterLLMUnavailableError,
        ValidationError as RouterValidationError,
        Department,
        Priority,
        Category,
    )
except ImportError:
    pass

__all__ = [
    # PMFBY Assistant
    "PMFBYAssistant",
    "PremiumCalculation",
    "ClaimGuidance",
    "Season",
    "CropCategory",
    # Financial Literacy
    "FinancialLiteracyEngine",
    "EMIResult",
    "SavingsComparison",
]

__version__ = "1.0.0"
