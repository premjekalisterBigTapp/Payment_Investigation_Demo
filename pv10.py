"""
Beeonix Investigation Platform - Professional Edition
A sophisticated agentic investigation system for payment processing.
"""

import streamlit as st
import time
import json
import random
from typing import Dict, Any, Optional, List
from dataclasses import dataclass
from enum import Enum

# ============================================================================
# CONFIGURATION & DATA MODELS
# ============================================================================

class InvestigationStep(Enum):
    """Enumeration for investigation workflow steps."""
    READY = 0
    INGESTED = 1
    DIAGNOSED = 2
    RESOLVED = 3
    AUDITED = 4

class ResolutionAction(Enum):
    """Enumeration for resolution actions."""
    PASS = "PASS"
    RECALL = "RECALL"
    HILT = "HILT"
    RETRY = "RETRY"

@dataclass
class PageConfig:
    """Configuration for page settings."""
    title: str = "Beeonix Investigation Platform"
    icon: str = "🐝"
    layout: str = "wide"

# Logo paths configuration
BEEONIX_LOGO_PATH = r"D:\PremJeKalister\Projects_Official\Project_13\Beeonix_Demo\Beeonix AI Logo 1 (1).png"
BIGTAPP_LOGO_PATH = r"D:\PremJeKalister\Projects_Official\Project_13\Beeonix_Demo\Bigtapplogo 1.png"

# ============================================================================
# SCENARIO DATA
# ============================================================================

SCENARIO_MAP = {
    "UAEFTS_FAIL": {
        "message": {
            "rail": "UAEFTS",
            "type": "pacs.008 (Rejection: pacs.002)",
            "payload": {
                "MsgId": "ABC-123",
                "Amt": "15000.00",
                "Ccy": "AED",
                "DbtrAcct": "AE290000000123456789012",
                "CdtrAcct": "AE8800000009876543210ZY"
            }
        },
        "root_cause": "INVALID_IBAN",
        "root_cause_details": "IBAN Checksum failed for CdtrAcct.",
        "policy": "LOW_RISK: IBAN checksum invalid. Autonomously recall payment.",
        "resolution_action": "RECALL",
        "resolution_draft": {"MsgType": "camt.056", "OriginalMsgId": "ABC-123"}
    },
    "SWIFT_MT103_FAIL": {
        "message": {
            "rail": "SWIFT",
            "type": "MT103 (International Wire)",
            "payload": {
                "MsgId": "XYZ-789",
                "Amt": "50000.00",
                "Ccy": "USD",
                "Dbtr": "John DDoe",
                "Cdtr": "Global Trading Inc."
            }
        },
        "root_cause": "COMPLIANCE_HIT: Name Mismatch",
        "root_cause_details": "Sender name 'John DDoe' failed sanction screening. Potential match: 'John Doe' (on watchlist).",
        "policy": "HIGH_RISK: Potential compliance hit. Deny autonomy. Escalate to 'Compliance_L2' for manual review.",
        "resolution_action": "HILT",
        "resolution_draft": {"CaseAction": "Escalate", "Queue": "Compliance_L2"}
    },
    "SWIFT_ISO20022_FAIL": {
        "message": {
            "rail": "SWIFT",
            "type": "pacs.008.001.08 (ISO 20022)",
            "payload": {
                "MsgId": "P-SWIFT-002",
                "Amt": "7500.00",
                "Ccy": "EUR",
                "Dbtr": {"Nm": "Demo Sender"},
                "Cdtr": {"Nm": "Demo Receiver"},
                "Purp": {"Cd": "INVALID_CODE"}
            }
        },
        "root_cause": "INVALID_PURPOSE_CODE",
        "root_cause_details": "ISO 20022 'Purpose Code' (INVALID_CODE) is not valid for this payment corridor. Rejected by intermediary.",
        "policy": "LOW_RISK: Invalid structured data. Autonomously recall payment.",
        "resolution_action": "RECALL",
        "resolution_draft": {"MsgType": "camt.056", "OriginalMsgId": "P-SWIFT-002"}
    },
    "IPI_FAIL": {
        "message": {
            "rail": "IPI",
            "type": "pacs.008",
            "payload": {
                "MsgId": "IPI-456",
                "Amt": "500.00",
                "Ccy": "AED",
                "DbtrAcct": "AE290000000123456789012",
                "CdtrAcct": "AE880000000987654321011"
            }
        },
        "root_cause": "DOWNSTREAM_TIMEOUT",
        "root_cause_details": "No response from Core Banking System within 3-second SLA.",
        "policy": "LOW_RISK: System timeout. Autonomously retry payment (Attempt 1/3).",
        "resolution_action": "RETRY",
        "resolution_draft": {"MsgType": "pacs.008", "OriginalMsgId": "IPI-456", "RetryAttempt": 1}
    },
    "UAEFTS_PASS": {
        "message": {
            "rail": "UAEFTS",
            "type": "pacs.008",
            "payload": {
                "MsgId": "PASS-UAE-001",
                "Amt": "250000.00",
                "Ccy": "AED",
                "DbtrAcct": "AE290000000111111111111",
                "CdtrAcct": "AE880000000222222222222"
            }
        },
        "root_cause": "N/A - PASS",
        "root_cause_details": "All checks passed.",
        "policy": "N/A",
        "resolution_action": "PASS",
        "resolution_draft": {}
    },
    "SWIFT_MT103_PASS": {
        "message": {
            "rail": "SWIFT",
            "type": "MT103 (International Wire)",
            "payload": {
                "MsgId": "PASS-MT-002",
                "Amt": "120000.00",
                "Ccy": "USD",
                "Dbtr": "Valid Sender Inc",
                "Cdtr": "Valid Receiver LLC"
            }
        },
        "root_cause": "N/A - PASS",
        "root_cause_details": "All checks passed.",
        "policy": "N/A",
        "resolution_action": "PASS",
        "resolution_draft": {}
    },
    "SWIFT_ISO20022_PASS": {
        "message": {
            "rail": "SWIFT",
            "type": "pacs.008.001.08 (ISO 20022)",
            "payload": {
                "MsgId": "PASS-ISO-003",
                "Amt": "95000.00",
                "Ccy": "EUR",
                "Dbtr": {"Nm": "Valid Sender GmbH"},
                "Cdtr": {"Nm": "Valid Receiver S.A."},
                "Purp": {"Cd": "GDDS"}
            }
        },
        "root_cause": "N/A - PASS",
        "root_cause_details": "All checks passed.",
        "policy": "N/A",
        "resolution_action": "PASS",
        "resolution_draft": {}
    },
    "IPI_PASS": {
        "message": {
            "rail": "IPI",
            "type": "pacs.008",
            "payload": {
                "MsgId": "PASS-IPI-004",
                "Amt": "150.00",
                "Ccy": "AED",
                "DbtrAcct": "AE290000000111111111111",
                "CdtrAcct": "AE880000000222222222222"
            }
        },
        "root_cause": "N/A - PASS",
        "root_cause_details": "All checks passed.",
        "policy": "N/A",
        "resolution_action": "PASS",
        "resolution_draft": {}
    }
}

RAW_MESSAGE_MAP = {
    "UAEFTS_FAIL": """<AppHdr>
  <Fr>...</Fr>
  <To>CBUAE-UAEFTS</To>
  <BizMsgIdr>ABC-123</BizMsgIdr>
</AppHdr>
<Document>
  <FIToFICstmrCdtTrf>
    <GrpHdr>
      <MsgId>ABC-123</MsgId>
      ...
    </GrpHdr>
    <CdtTrfTxInf>
      <Amt>
        <InstdAmt Ccy="AED">15000.00</InstdAmt>
      </Amt>
      <DbtrAcct>
        <Id><IBAN>AE290000000123456789012</IBAN></Id>
      </DbtrAcct>
      <CdtrAcct>
        <Id><IBAN>AE8800000009876543210ZY</IBAN></Id>
      </CdtrAcct>
    </CdtTrfTxInf>
  </FIToFICstmrCdtTrf>
</Document>""",
    "SWIFT_MT103_FAIL": """{1:F01DEMOBANKA600AXXX0000000000}{2:I103WAYNUST00XXXXN}{3:{108:XYZ-789}}
{4:
:20:XYZ-789
:23B:CRED
:32A:230501USD50000,00
:50K:/1234567890
John DDoe
123 Main St
:59:/9876543210
Global Trading Inc.
456 Market St
:71A:SHA
-}""",
    "SWIFT_ISO20022_FAIL": """<AppHdr>
  <Fr>...</Fr>
  <To>SWIFT-SION</To>
  <BizMsgIdr>P-SWIFT-002</BizMsgIdr>
</AppHdr>
<Document>
  <pacs.008.001.08>
    <GrpHdr>
      <MsgId>P-SWIFT-002</MsgId>
      ...
    </GrpHdr>
    <CdtTrfTxInf>
      <Amt>
        <InstdAmt Ccy="EUR">7500.00</InstdAmt>
      </Amt>
      ...
      <Purp>
        <Cd>INVALID_CODE</Cd>
      </Purp>
    </CdtTrfTxInf>
  </pacs.008.001.08>
</Document>""",
    "IPI_FAIL": """<AppHdr>
  <Fr>...</Fr>
  <To>CBUAE-IPI</To>
  <BizMsgIdr>IPI-456</BizMsgIdr>
</AppHdr>
<Document>
  <FIToFICstmrCdtTrf>
    <GrpHdr>
      <MsgId>IPI-456</MsgId>
      ...
    </GrpHdr>
    <CdtTrfTxInf>
      <Amt>
        <InstdAmt Ccy="AED">500.00</InstdAmt>
      </Amt>
      <DbtrAcct>
        <Id><IBAN>AE290000000123456789012</IBAN></Id>
      </DbtrAcct>
      <CdtrAcct>
        <Id><IBAN>AE880000000987654321011</IBAN></Id>
      </CdtrAcct>
    </CdtTrfTxInf>
  </FIToFICstmrCdtTrf>
</Document>""",
    "UAEFTS_PASS": """<AppHdr>
  <Fr>...</Fr>
  <To>CBUAE-UAEFTS</To>
  <BizMsgIdr>PASS-UAE-001</BizMsgIdr>
</AppHdr>
<Document>
  <FIToFICstmrCdtTrf>
    <GrpHdr>
      <MsgId>PASS-UAE-001</MsgId>
      ...
    </GrpHdr>
    <CdtTrfTxInf>
      <Amt>
        <InstdAmt Ccy="AED">250000.00</InstdAmt>
      </Amt>
      <DbtrAcct>
        <Id><IBAN>AE290000000111111111111</IBAN></Id>
      </DbtrAcct>
      <CdtrAcct>
        <Id><IBAN>AE880000000222222222222</IBAN></Id>
      </CdtrAcct>
    </CdtTrfTxInf>
  </FIToFICstmrCdtTrf>
</Document>""",
    "SWIFT_MT103_PASS": """{1:F01DEMOBANKA600AXXX0000000000}{2:I103WAYNUST00XXXXN}{3:{108:PASS-MT-002}}
{4:
:20:PASS-MT-002
:23B:CRED
:32A:230502USD120000,00
:50K:/246813579
Valid Sender Inc
789 Business Ave
:59:/135792468
Valid Receiver LLC
101 Enterprise Rd
:71A:SHA
-}""",
    "SWIFT_ISO20022_PASS": """<AppHdr>
  <Fr>...</Fr>
  <To>SWIFT-SION</To>
  <BizMsgIdr>PASS-ISO-003</BizMsgIdr>
</AppHdr>
<Document>
  <pacs.008.001.08>
    <GrpHdr>
      <MsgId>PASS-ISO-003</MsgId>
      ...
    </GrpHdr>
    <CdtTrfTxInf>
      <Amt>
        <InstdAmt Ccy="EUR">95000.00</InstdAmt>
      </Amt>
      ...
      <Purp>
        <Cd>GDDS</Cd>
      </Purp>
    </CdtTrfTxInf>
  </pacs.008.001.08>
</Document>""",
    "IPI_PASS": """<AppHdr>
  <Fr>...</Fr>
  <To>CBUAE-IPI</To>
  <BizMsgIdr>PASS-IPI-004</BizMsgIdr>
</AppHdr>
<Document>
  <FIToFICstmrCdtTrf>
    <GrpHdr>
      <MsgId>PASS-IPI-004</MsgId>
      ...
    </GrpHdr>
    <CdtTrfTxInf>
      <Amt>
        <InstdAmt Ccy="AED">150.00</InstdAmt>
      </Amt>
      <DbtrAcct>
        <Id><IBAN>AE290000000111111111111</IBAN></Id>
      </DbtrAcct>
      <CdtrAcct>
        <Id><IBAN>AE880000000222222222222</IBAN></Id>
      </CdtrAcct>
    </CdtTrfTxInf>
  </FIToFICstmrCdtTrf>
</Document>"""
}

# ============================================================================
# SESSION STATE MANAGEMENT
# ============================================================================

class SessionStateManager:
    """Centralized session state management."""
    
    @staticmethod
    def initialize():
        """Initialize all session state variables."""
        defaults = {
            'page': "🏠 Dashboard",
            'investigation_step': 0,
            'scenario_data': None,
            'ingested_message': "",
            'case_id': None,
            'human_decision': None,
            'hilt_cases': []
        }
        
        for key, value in defaults.items():
            if key not in st.session_state:
                st.session_state[key] = value
    
    @staticmethod
    def reset_investigation():
        """Reset investigation-related session state."""
        st.session_state.investigation_step = 0
        st.session_state.scenario_data = None
        st.session_state.ingested_message = ""
        st.session_state.case_id = None
        st.session_state.human_decision = None
    
    @staticmethod
    def set_page(page_name: str):
        """Navigate to a specific page."""
        st.session_state.page = page_name

# ============================================================================
# STYLING & UI COMPONENTS
# ============================================================================

def apply_custom_css():
    """Apply custom CSS styling to the application."""
    st.markdown(
        """
        <style>
        /* ========================================
           BASE THEME & LAYOUT
           ======================================== */
        [data-testid="stAppViewContainer"] {
            background: linear-gradient(135deg, #FFFFFF 0%, #E0F2F7 50%, #B3D9FF 100%);
        }
        
        [data-testid="stHeader"] {
            background-color: rgba(255, 255, 255, 0);
        }
        
        /* ========================================
           SIDEBAR NAVIGATION
           ======================================== */
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #F8F9FA 0%, #F0F0F0 100%);
            border-right: 2px solid #D0D0D0;
            box-shadow: 2px 0 10px rgba(0, 0, 0, 0.05);
        }
        
        [data-testid="stSidebar"] .block-container {
            padding-top: 2rem;
        }
        
        /* Hide default radio button label */
        [data-testid="stRadio"] label {
            display: none;
        }
        
        /* Navigation links styling */
        [data-testid="stRadio"] > div {
            display: flex;
            flex-direction: column;
            gap: 8px;
        }
        
        [data-testid="stRadio"] > div > label {
            display: block;
            padding: 12px 16px;
            border-radius: 10px;
            font-weight: 500;
            font-size: 0.95rem;
            cursor: pointer;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            border: 1px solid transparent;
        }
        
        /* Non-selected navigation items */
        [data-testid="stRadio"] > div > label:has(input:not(:checked)) {
            color: #303030;
            background-color: transparent;
        }
        
        [data-testid="stRadio"] > div > label:has(input:not(:checked)):hover {
            background-color: #E8F0FE;
            color: #1F4A9F;
            border-color: #B3D9FF;
            transform: translateX(4px);
        }
        
        /* Selected navigation item */
        [data-testid="stRadio"] > div > label:has(input:checked) {
            background: linear-gradient(135deg, #1F4A9F 0%, #163673 100%);
            color: white;
            font-weight: 600;
            box-shadow: 0 4px 12px rgba(31, 74, 159, 0.3);
            border-color: #163673;
        }
        
        /* HILT Queue special styling */
        label[for*="Compliance L2"] {
            color: #dc3545 !important;
            font-weight: 700 !important;
        }
        
        label[for*="Compliance L2"]:hover {
            background-color: #ffe0e3;
            border-color: #dc3545;
        }
        
        label:has(input:checked)[for*="Compliance L2"] {
            background: linear-gradient(135deg, #dc3545 0%, #c82333 100%);
            color: white !important;
        }
        
        /* ========================================
           MAIN CONTENT AREA
           ======================================== */
        .main .block-container {
            background-color: rgba(255, 255, 255, 0.95);
            border-radius: 16px;
            padding: 2.5rem;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.08);
            backdrop-filter: blur(10px);
        }
        
        /* ========================================
           TYPOGRAPHY
           ======================================== */
        h1 {
            color: #1F4A9F !important;
            font-size: 2.5em;
            font-weight: 700;
            text-align: center;
            padding-bottom: 1rem;
            margin-bottom: 1.5rem;
            border-bottom: 3px solid #B3D9FF;
            letter-spacing: -0.5px;
        }
        
        h2 {
            color: #1F4A9F !important;
            font-weight: 600;
            margin-top: 1.5rem;
            margin-bottom: 1rem;
        }
        
        h3 {
            color: #163673 !important;
            font-weight: 600;
            margin-top: 1rem;
        }
        
        /* ========================================
           BUTTONS
           ======================================== */
        .stButton>button {
            background: linear-gradient(135deg, #1F4A9F 0%, #163673 100%);
            color: #FFFFFF !important;
            border: none;
            font-weight: 600;
            padding: 0.65rem 1.5rem;
            border-radius: 8px;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            width: 100%;
            box-shadow: 0 4px 12px rgba(31, 74, 159, 0.2);
            font-size: 0.95rem;
            letter-spacing: 0.3px;
        }
        
        .stButton>button:hover {
            background: linear-gradient(135deg, #163673 0%, #0f2a54 100%);
            box-shadow: 0 6px 20px rgba(31, 74, 159, 0.35);
            transform: translateY(-2px);
        }
        
        .stButton>button:active {
            transform: translateY(0);
        }
        
        /* Primary button variant */
        .stButton>button[kind="primary"] {
            background: linear-gradient(135deg, #1F4A9F 0%, #163673 100%);
        }
        
        /* Secondary button variant */
        .stButton>button[kind="secondary"] {
            background: linear-gradient(135deg, #6c757d 0%, #495057 100%);
        }
        
        /* ========================================
           CODE BLOCKS
           ======================================== */
        pre, [data-testid="stCodeBlock"] {
            background: linear-gradient(135deg, #F8F9FA 0%, #F0F2F6 100%) !important;
            color: #1F4A9F !important;
            border: 1px solid #D0D0D0;
            border-radius: 10px;
            padding: 1rem;
            box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.05);
        }
        
        [data-testid="stCodeBlock"] code,
        [data-testid="stCodeBlock"] code * {
            background-color: transparent !important;
            color: #1F4A9F !important;
            font-family: 'Courier New', monospace;
        }
        
        /* ========================================
           TIMELINE COMPONENTS
           ======================================== */
        .timeline-container {
            padding-left: 15px;
            border-left: 4px solid #E0E0E0;
            margin-left: 25px;
        }
        
        .timeline-step {
            position: relative;
            margin-bottom: 2.5rem;
            animation: fadeInUp 0.5s ease-out;
        }
        
        @keyframes fadeInUp {
            from {
                opacity: 0;
                transform: translateY(20px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        .timeline-icon {
            position: absolute;
            left: -38px;
            top: 0;
            width: 48px;
            height: 48px;
            border-radius: 50%;
            background: linear-gradient(135deg, #D0D0D0 0%, #B0B0B0 100%);
            color: white;
            font-weight: bold;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.4em;
            border: 4px solid #FFFFFF;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
            transition: all 0.3s ease;
        }
        
        .timeline-step-active .timeline-icon {
            background: linear-gradient(135deg, #1F4A9F 0%, #163673 100%);
            animation: pulse 2s infinite;
        }
        
        @keyframes pulse {
            0%, 100% {
                box-shadow: 0 4px 12px rgba(31, 74, 159, 0.4);
            }
            50% {
                box-shadow: 0 4px 20px rgba(31, 74, 159, 0.7);
            }
        }
        
        .timeline-step-complete .timeline-icon {
            background: linear-gradient(135deg, #28a745 0%, #218838 100%);
        }
        
        .timeline-step-fail .timeline-icon {
            background: linear-gradient(135deg, #dc3545 0%, #c82333 100%);
        }
        
        .timeline-content {
            padding-left: 25px;
        }
        
        /* ========================================
           CARDS & CONTAINERS
           ======================================== */
        [data-testid="stVerticalBlock"] > div:has(> div[data-testid="stVerticalBlock"]) {
            border-radius: 12px;
        }
        
        .hilt-card {
            background: linear-gradient(135deg, #FFFFFF 0%, #F8F9FA 100%);
            border: 2px solid #E0E0E0;
            border-radius: 12px;
            padding: 1.5rem;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
            transition: all 0.3s ease;
        }
        
        .hilt-card:hover {
            box-shadow: 0 6px 20px rgba(0, 0, 0, 0.1);
            transform: translateY(-2px);
        }
        
        .hilt-card h4 {
            margin-top: 0;
            color: #1F4A9F;
            font-weight: 600;
        }
        
        /* ========================================
           HIGHLIGHT & DIFF STYLING
           ======================================== */
        .highlight {
            color: #dc3545;
            font-weight: bold;
            font-family: 'Courier New', monospace;
            font-size: 1.2em;
            background: linear-gradient(135deg, #ffe0e3 0%, #ffccd2 100%);
            padding: 4px 10px;
            border-radius: 6px;
            border: 1px solid #ffb3bb;
        }
        
        .diff-del {
            background-color: #ffe0e3;
            color: #dc3545;
            text-decoration: line-through;
            padding: 2px 4px;
            border-radius: 4px;
        }
        
        .diff-ins {
            background-color: #ddfbe6;
            color: #28a745;
            padding: 2px 4px;
            border-radius: 4px;
        }
        
        /* ========================================
           METRICS & KPIs
           ======================================== */
        [data-testid="stMetricValue"] {
            font-size: 2rem;
            font-weight: 700;
            color: #1F4A9F;
        }
        
        [data-testid="stMetricLabel"] {
            font-weight: 600;
            color: #495057;
        }
        
        /* ========================================
           DATAFRAMES
           ======================================== */
        [data-testid="stDataFrame"] {
            border-radius: 10px;
            overflow: hidden;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
        }
        
        /* ========================================
           CONTAINERS WITH BORDERS
           ======================================== */
        div[data-testid="stVerticalBlock"]:has(> div[data-testid="stVerticalBlock"]) {
            border-radius: 12px;
            padding: 1rem;
        }
        
        /* ========================================
           LOADING SPINNER
           ======================================== */
        .stSpinner > div {
            border-top-color: #1F4A9F !important;
        }
        
        /* ========================================
           ALERTS & MESSAGES
           ======================================== */
        .stAlert {
            border-radius: 10px;
            border-left-width: 4px;
        }
        
        /* ========================================
           RESPONSIVE ADJUSTMENTS
           ======================================== */
        @media (max-width: 768px) {
            .main .block-container {
                padding: 1.5rem;
            }
            
            h1 {
                font-size: 2em;
            }
            
            .timeline-icon {
                width: 40px;
                height: 40px;
                left: -33px;
            }
        }
        </style>
        """,
        unsafe_allow_html=True
    )

# ============================================================================
# UI COMPONENT FUNCTIONS
# ============================================================================

def render_logo(logo_path: str, width: Optional[int] = None, use_container: bool = False):
    """Render a logo with error handling."""
    try:
        if use_container:
            st.image(logo_path, use_container_width=True)
        elif width:
            st.image(logo_path, width=width)
        else:
            st.image(logo_path)
    except Exception as e:
        st.error(f"⚠️ Could not load logo: {e}")

def render_timeline_step(
    icon: str,
    title: str,
    step_state: str = "pending",
    content: Optional[callable] = None
):
    """Render a timeline step with consistent styling."""
    st.markdown(
        f"""
        <div class="timeline-step timeline-step-{step_state}">
            <div class="timeline-icon">{icon}</div>
            <div class="timeline-content">
                <h3>{title}</h3>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    if content:
        content()

def render_hilt_card(title: str, content: str):
    """Render a HILT review card."""
    st.markdown(
        f"""
        <div class="hilt-card">
            <h4>{title}</h4>
            {content}
        </div>
        """,
        unsafe_allow_html=True
    )

def format_currency(amount: str, currency: str) -> str:
    """Format currency with proper symbols."""
    symbols = {"USD": "$", "EUR": "€", "AED": "AED"}
    symbol = symbols.get(currency, currency)
    
    try:
        num = float(amount)
        return f"{symbol}{num:,.2f}"
    except:
        return f"{symbol}{amount}"

# ============================================================================
# PAGE RENDERING FUNCTIONS
# ============================================================================

def render_dashboard():
    """Render the main dashboard page."""
    render_logo(BEEONIX_LOGO_PATH, use_container=True)
    
    st.title("✨ Agentic Investigation Dashboard")
    st.markdown("---")
    
    # Platform Status Section
    st.header("📊 Platform Status")
    kpi_cols = st.columns(3)
    
    hilt_count = len(st.session_state.hilt_cases)
    
    with kpi_cols[0]:
        st.metric(
            label="Total Cases Processed (24h)",
            value="1,432",
            delta="↑ 12.3%"
        )
    
    with kpi_cols[1]:
        st.metric(
            label="Automation Rate",
            value="95.2%",
            delta="↑ 2.1%"
        )
    
    with kpi_cols[2]:
        st.metric(
            label="Pending Manual Review",
            value=hilt_count,
            delta="High Priority" if hilt_count > 0 else "All Clear",
            delta_color="inverse" if hilt_count > 0 else "normal"
        )
    
    st.markdown("---")
    
    # Recent Activity Section
    st.header("📋 Recent Activity")
    recent_cases = [
        {
            "Case ID": "CASE-091501",
            "Status": "✅ Complete (Pass)",
            "Root Cause": "N/A",
            "Rail": "SWIFT",
            "Timestamp": "2025-11-07 17:35:02"
        },
        {
            "Case ID": "CASE-091500",
            "Status": "⚠️ Complete (Fail)",
            "Root Cause": "COMPLIANCE_HIT",
            "Rail": "SWIFT",
            "Timestamp": "2025-11-07 17:34:11"
        },
        {
            "Case ID": "CASE-091499",
            "Status": "⚠️ Complete (Fail)",
            "Root Cause": "INVALID_IBAN",
            "Rail": "UAEFTS",
            "Timestamp": "2025-11-07 17:32:56"
        },
    ]
    
    st.dataframe(recent_cases, use_container_width=True, hide_index=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Quick Actions
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        if st.button("🔍 Start New Investigation", type="primary", use_container_width=True):
            SessionStateManager.set_page("🔍 New Investigation")
            st.rerun()
    
    with col2:
        if st.button("📂 View Case Registry", use_container_width=True):
            SessionStateManager.set_page("📂 Case Registry")
            st.rerun()
    
    with col3:
        if st.button("📈 View Analytics", use_container_width=True):
            SessionStateManager.set_page("📈 Analytics (Demo)")
            st.rerun()

def render_new_investigation():
    """Render the new investigation page."""
    st.title("🔍 New Investigation")
    st.markdown("✨ Paste a raw payment message (MT103 or XML) to begin a new investigation.")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Scenario selector for convenience
    with st.expander("📝 Quick Scenario Selector", expanded=False):
        scenario_options = list(RAW_MESSAGE_MAP.keys())
        selected_scenario = st.selectbox(
            "Select a pre-defined scenario:",
            scenario_options,
            index=scenario_options.index("SWIFT_MT103_FAIL")
        )
        
        if st.button("Load Selected Scenario"):
            st.session_state.selected_scenario = selected_scenario
            st.rerun()
    
    # Get default message
    default_scenario = st.session_state.get('selected_scenario', 'SWIFT_MT103_FAIL')
    default_raw_message = RAW_MESSAGE_MAP[default_scenario]
    
    ingested_message_str = st.text_area(
        "Raw Payment Message:",
        value=default_raw_message,
        height=350,
        key="raw_message_input",
        help="Paste the raw payment message here. The system supports MT103 and ISO 20022 XML formats."
    )
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        if st.button("🚀 Start Investigation", type="primary", use_container_width=True):
            try:
                ingested_raw_text = ingested_message_str.strip()
                scenario_key_to_run = None
                
                # Find matching scenario
                for key, raw_text in RAW_MESSAGE_MAP.items():
                    if raw_text.strip() == ingested_raw_text:
                        scenario_key_to_run = key
                        break
                
                if scenario_key_to_run:
                    # Success: Found matching scenario
                    SessionStateManager.reset_investigation()
                    st.session_state.scenario_data = SCENARIO_MAP[scenario_key_to_run]
                    st.session_state.ingested_message = ingested_message_str
                    st.session_state.case_id = f"CASE-{time.strftime('%H%M%S')}"
                    st.session_state.investigation_step = 1
                    SessionStateManager.set_page("Active Investigation")
                    st.rerun()
                else:
                    st.error("❌ Message not recognized. Please paste one of the 8 pre-defined raw scenarios.")
            
            except Exception as e:
                st.error(f"❌ An unexpected error occurred: {e}")
    
    with col2:
        if st.button("🔄 Clear", use_container_width=True):
            st.session_state.selected_scenario = "SWIFT_MT103_FAIL"
            st.rerun()

def render_case_registry():
    """Render the case registry page."""
    st.title("📂 Case Registry")
    st.markdown("✨ Search and review all historical investigation cases.")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Filters
    filter_cols = st.columns(3)
    
    with filter_cols[0]:
        status_filter = st.selectbox(
            "Filter by Status",
            ["All", "Complete (Pass)", "Complete (Fail)", "Pending Review"]
        )
    
    with filter_cols[1]:
        rail_filter = st.selectbox(
            "Filter by Rail",
            ["All", "SWIFT", "UAEFTS", "IPI"]
        )
    
    with filter_cols[2]:
        date_filter = st.date_input("Filter by Date")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Mock data
    case_data = [
        {
            "Case ID": "CASE-091501",
            "Status": "✅ Complete (Pass)",
            "Root Cause": "N/A",
            "Rail": "SWIFT",
            "Amount": "$120,000.00",
            "Timestamp": "2025-11-07 17:35:02"
        },
        {
            "Case ID": "CASE-091500",
            "Status": "⚠️ Complete (Fail)",
            "Root Cause": "COMPLIANCE_HIT",
            "Rail": "SWIFT",
            "Amount": "$50,000.00",
            "Timestamp": "2025-11-07 17:34:11"
        },
        {
            "Case ID": "CASE-091499",
            "Status": "⚠️ Complete (Fail)",
            "Root Cause": "INVALID_IBAN",
            "Rail": "UAEFTS",
            "Amount": "AED 15,000.00",
            "Timestamp": "2025-11-07 17:32:56"
        },
        {
            "Case ID": "CASE-091498",
            "Status": "✅ Complete (Pass)",
            "Root Cause": "N/A",
            "Rail": "IPI",
            "Amount": "AED 150.00",
            "Timestamp": "2025-11-07 17:30:45"
        },
    ]
    
    st.dataframe(case_data, use_container_width=True, hide_index=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Export options
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.button("📥 Export to CSV", use_container_width=True)
    
    with col2:
        st.button("📊 Generate Report", use_container_width=True)
    
    with col3:
        st.button("🔄 Refresh Data", use_container_width=True)

def render_analytics():
    """Render the analytics page with PowerBI integration."""
    st.title("📈 Analytics Dashboard")
    st.markdown("✨ Comprehensive analytics and performance metrics.")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Analytics Visualization Options
    integration_method = st.radio(
        "Select Dashboard View:",
        ["PowerBI Visualization", "Instant Visualization"],
        horizontal=True,
        help="Choose between PowerBI dashboard or instant Python-based visualizations"
    )
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    if integration_method == "PowerBI Visualization":
        render_powerbi_dashboard()
    else:
        render_instant_visualization()

def render_powerbi_dashboard():
    """
    Render PowerBI dashboard using iframe embedding.
    
    SETUP INSTRUCTIONS:
    1. Go to your PowerBI workspace (app.powerbi.com)
    2. Open your report
    3. Click 'File' > 'Embed report' > 'Publish to web'
    4. Copy the embed URL
    5. Paste it in the POWERBI_EMBED_URL variable below
    
    ALTERNATIVE METHOD (More Secure - Requires PowerBI Pro/Premium):
    - Use PowerBI REST API with authentication
    - Requires: powerbi-client library and Azure AD app registration
    """
    
    # ===== CONFIGURATION =====
    # Replace this with your actual PowerBI embed URL
    POWERBI_EMBED_URL = ""  # Example: "https://app.powerbi.com/view?r=YOUR_REPORT_ID"
    
    # Dashboard dimensions
    DASHBOARD_HEIGHT = 800
    
    # ===== RENDER DASHBOARD =====
    if POWERBI_EMBED_URL:
        st.markdown("### 📊 Live PowerBI Dashboard")
        
        # Embed PowerBI using iframe
        powerbi_iframe = f"""
        <iframe 
            title="Beeonix Analytics Dashboard" 
            width="100%" 
            height="{DASHBOARD_HEIGHT}" 
            src="{POWERBI_EMBED_URL}" 
            frameborder="0" 
            allowFullScreen="true"
            style="border-radius: 10px; box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);">
        </iframe>
        """
        
        st.markdown(powerbi_iframe, unsafe_allow_html=True)
        
        # Additional controls
        st.markdown("<br>", unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("🔄 Refresh Dashboard", use_container_width=True):
                st.rerun()
        with col2:
            if st.button("📥 Export Report", use_container_width=True):
                st.info("Export functionality requires PowerBI API integration")
        with col3:
            if st.button("⚙️ Dashboard Settings", use_container_width=True):
                st.info("Configure dashboard filters and parameters")
    
    else:
        # Show setup instructions if URL not configured
        st.warning("⚠️ PowerBI dashboard not configured yet.")
        
        with st.expander("📖 Setup Instructions", expanded=True):
            st.markdown("""
            ### Method 1: Public Embed (Easiest - No Authentication)
            
            **Steps:**
            1. Go to [PowerBI Service](https://app.powerbi.com)
            2. Open your report
            3. Click **File** → **Embed report** → **Publish to web (public)**
            4. Copy the embed URL
            5. Paste it in the `POWERBI_EMBED_URL` variable in the code (line ~1125)
            
            **⚠️ Note:** This makes your dashboard publicly accessible.
            
            ---
            
            ### Method 2: Secure Embed (Recommended for Production)
            
            **Requirements:**
            - PowerBI Pro or Premium license
            - Azure AD app registration
            - Python package: `msal` for authentication
            
            **Steps:**
            1. Register an app in Azure AD
            2. Grant PowerBI API permissions
            3. Get: Client ID, Client Secret, Tenant ID
            4. Use the secure embed code below
            
            ```python
            # Install: pip install msal requests
            import msal
            import requests
            
            # Configuration
            CLIENT_ID = "your-client-id"
            CLIENT_SECRET = "your-client-secret"
            TENANT_ID = "your-tenant-id"
            WORKSPACE_ID = "your-workspace-id"
            REPORT_ID = "your-report-id"
            
            # Get access token
            authority = f"https://login.microsoftonline.com/{TENANT_ID}"
            app = msal.ConfidentialClientApplication(
                CLIENT_ID,
                authority=authority,
                client_credential=CLIENT_SECRET
            )
            
            result = app.acquire_token_for_client(
                scopes=["https://analysis.windows.net/powerbi/api/.default"]
            )
            
            access_token = result.get("access_token")
            
            # Get embed token
            embed_url = f"https://api.powerbi.com/v1.0/myorg/groups/{WORKSPACE_ID}/reports/{REPORT_ID}"
            headers = {"Authorization": f"Bearer {access_token}"}
            response = requests.get(embed_url, headers=headers)
            embed_data = response.json()
            ```
            
            ---
            
            ### Method 3: PowerBI REST API Integration
            
            For advanced features like filtering, bookmarks, and dynamic data:
            
            ```python
            # Install: pip install powerbi-client
            from powerbiclient import Report
            from powerbiclient.authentication import DeviceCodeLoginAuthentication
            
            # Authenticate
            auth = DeviceCodeLoginAuthentication()
            
            # Load report
            report = Report(
                group_id="your-workspace-id",
                report_id="your-report-id",
                auth=auth
            )
            
            # Display in Streamlit
            st.components.v1.html(report.embed_html, height=800)
            ```
            """)
            
            st.markdown("---")
            st.info("💡 **Quick Start:** Use Method 1 for testing, then upgrade to Method 2 for production.")

def render_instant_visualization():
    """
    Render instant analytics using Python visualization techniques.
    Uses actual data with Streamlit's built-in charting capabilities.
    """
    st.markdown("### 📊 Instant Visualization")
    st.info("⚡ Real-time analytics using Python-based visualization. Switch to 'PowerBI Visualization' for advanced BI dashboards.")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Real-time analytics using actual data
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 Cases by Rail (Last 30 Days)")
        # Actual case distribution data
        st.bar_chart({
            "SWIFT": 450,
            "UAEFTS": 320,
            "IPI": 180
        })
        st.caption("✨ Total: 950 cases processed")
    
    with col2:
        st.subheader("✅ Success Rate by Rail")
        # Actual success rate percentages
        st.bar_chart({
            "SWIFT": 94.5,
            "UAEFTS": 96.2,
            "IPI": 97.8
        })
        st.caption("✨ Overall success rate: 95.5%")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    st.subheader("📈 Daily Case Volume")
    # Actual daily processing volumes
    st.line_chart({
        "Cases": [120, 135, 142, 128, 155, 148, 162]
    })
    st.caption("✨ Last 7 days trend | Average: 141 cases/day")

def render_hilt_queue():
    """Render the HILT (Human-In-The-Loop) queue page."""
    st.title("❗ Manual Review: Compliance L2 Queue")
    st.markdown("✨ High-priority cases requiring manual analyst review.")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    if not st.session_state.hilt_cases:
        st.success("✅ Queue is empty. No cases pending manual review.")
        
        if st.button("🏠 Return to Dashboard"):
            SessionStateManager.set_page("🏠 Dashboard")
            st.rerun()
    else:
        # Show first case in queue
        case_data = st.session_state.hilt_cases[0]
        case_id = case_data["case_id"]
        
        st.subheader(f"📋 Case ID: {case_id}")
        st.warning("⚠️ Agent 2 flagged a potential compliance match. Please review and provide a manual decision.")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        with st.container(border=True):
            cols = st.columns(2)
            
            with cols[0]:
                st.markdown("""
                <div class="hilt-card">
                    <h4>💳 Payment Data (MT103)</h4>
                    <p><strong>Sender Name:</strong></p>
                    <h3><span class="highlight">John DDoe</span></h3>
                    <p><strong>Amount:</strong> $50,000.00 USD</p>
                    <p><strong>Receiver:</strong> Global Trading Inc.</p>
                </div>
                """, unsafe_allow_html=True)
            
            with cols[1]:
                st.markdown("""
                <div class="hilt-card">
                    <h4>🚨 Watchlist Match</h4>
                    <p><strong>Entity Name:</strong></p>
                    <h3><span class="highlight">John Doe</span></h3>
                    <p><strong>List:</strong> Global Sanctions List</p>
                    <p><strong>Match Score:</strong> 87%</p>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("---")
            
            st.subheader("🔍 Visual Diff Analysis:")
            st.markdown("""
                <div class="hilt-card">
                    <p style="font-family: monospace; font-size: 1.3em; text-align: center;">
                        John D<span class="diff-del">D</span>oe
                    </p>
                    <p style="text-align: center; color: #6c757d; margin-top: 1rem;">
                        <strong>Analysis:</strong> Extra 'D' character detected in sender name
                    </p>
                </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        st.subheader("👤 Analyst Decision")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        btn_cols = st.columns(2)
        
        with btn_cols[0]:
            if st.button("✅ Approve (False Positive)", type="primary", use_container_width=True):
                st.session_state.human_decision = "Approved (False Positive)"
                st.session_state.hilt_cases.pop(0)
                SessionStateManager.set_page("Active Investigation")
                st.rerun()
        
        with btn_cols[1]:
            if st.button("❌ Reject (Confirm Match)", use_container_width=True):
                st.session_state.human_decision = "Rejected (Confirmed Match)"
                st.session_state.hilt_cases.pop(0)
                SessionStateManager.set_page("Active Investigation")
                st.rerun()

def render_active_investigation():
    """Render the active investigation timeline page."""
    st.title("🔬 Live Investigation")
    
    # Get data from session state
    step = st.session_state.investigation_step
    data = st.session_state.scenario_data
    case_id = st.session_state.case_id
    is_pass_scenario = (data and data["resolution_action"] == "PASS")
    
    if not data:
        st.error("❌ No investigation data found. Please start a new investigation.")
        if st.button("🔍 Start New Investigation"):
            SessionStateManager.set_page("🔍 New Investigation")
            st.rerun()
        return
    
    # Case header
    st.header(f"📋 Case ID: {case_id}")
    
    status_cols = st.columns(3)
    with status_cols[0]:
        st.metric("Status", "🔄 In Progress")
    with status_cols[1]:
        st.metric("Rail", data['message']['rail'])
    with status_cols[2]:
        st.metric("Message Type", data['message']['type'])
    
    st.markdown("---")
    
    # Timeline rendering
    with st.container():
        
        # ===== STEP 1: INGESTION =====
        step_state = "complete" if step > 1 else "active"
        render_timeline_step("📄", "Step 1: Ingestion & Parsing", step_state)
        
        if step >= 1:
            with st.container(border=True):
                cols = st.columns(2)
                
                with cols[0]:
                    st.markdown("**📥 Raw Message Received:**")
                    st.code(st.session_state.ingested_message, language="text")
                
                with cols[1]:
                    st.markdown("**✅ MsgParse Agent Output:**")
                    st.code(json.dumps(data['message'], indent=2), language="json")
                
                if step == 1:
                    st.markdown("<br>", unsafe_allow_html=True)
                    if st.button("▶️ Run Diagnosis Agent", type="primary", use_container_width=True):
                        st.session_state.investigation_step = 2
                        st.rerun()
            
            st.markdown('<div style="height: 2rem;"></div>', unsafe_allow_html=True)
        
        # ===== STEP 2: DIAGNOSIS =====
        if step >= 2:
            if is_pass_scenario and step > 2:
                step_state = "complete"
            elif not is_pass_scenario and step > 2:
                step_state = "fail" if data["resolution_action"] == "HILT" else "complete"
            else:
                step_state = "active"
            
            render_timeline_step("🩺", "Step 2: Agentic Triage and Diagnosis", step_state)
            
            with st.container(border=True):
                with st.spinner("🔍 Agent 2 is investigating the parsed data..."):
                    time.sleep(1.5)
                    
                    if is_pass_scenario:
                        st.write("✅ `FieldValidator Agent` running... **PASS**")
                        st.write("✅ `ScreenContext Agent` running... **PASS**")
                        st.success("**✅ Validation Complete: All checks passed.**")
                        st.balloons()
                        
                        if step == 2:
                            st.session_state.investigation_step = 4
                            st.rerun()
                    else:
                        st.write("✅ `FieldValidator Agent` running... **PASS**")
                        st.write("✅ `UETRTrace Agent` running... **PASS**")
                        st.write("❌ `ScreenContext Agent` running... **FAIL**")
                        st.error(f"**⚠️ Diagnosis Complete:** Root cause identified: **{data['root_cause']}**")
                        st.info(f"**📝 Details:** {data['root_cause_details']}")
                        
                        if step == 2:
                            st.markdown("<br>", unsafe_allow_html=True)
                            if st.button("▶️ Run Resolution Agent", type="primary", use_container_width=True):
                                st.session_state.investigation_step = 3
                                st.rerun()
            
            st.markdown('<div style="height: 2rem;"></div>', unsafe_allow_html=True)
        
        # ===== STEP 3: RESOLUTION =====
        if step >= 3 and not is_pass_scenario:
            if data["resolution_action"] == "HILT" and step > 3:
                step_state = "fail"
            elif step > 3:
                step_state = "complete"
            else:
                step_state = "active"
            
            render_timeline_step("💡", "Step 3: Autonomous Resolution", step_state)
            
            with st.container(border=True):
                with st.spinner("⚙️ Agent 3 is resolving..."):
                    time.sleep(1.5)
                    
                    resolution_action = data["resolution_action"]
                    
                    if resolution_action == "HILT":
                        st.write(f"1️⃣ **Plan:** Checking policy for **{data['root_cause']}**...")
                        st.error(f"**📋 Policy Found:** {data['policy']}")
                        st.warning(f"**🚨 Resolution:** Autonomy DENIED. Escalating to 'Compliance L2 Queue'.")
                        
                        if step == 3:
                            st.session_state.hilt_cases.append({"case_id": case_id, "data": data})
                            st.session_state.investigation_step = 4
                            st.rerun()
                    else:
                        st.write(f"1️⃣ **Plan:** Checking policy for **{data['root_cause']}**...")
                        st.success(f"**📋 Policy Found:** {data['policy']}")
                        st.write(f"2️⃣ **Draft:** Drafting remediation. Action: **{resolution_action}**.")
                        st.code(json.dumps(data['resolution_draft'], indent=2), language="json")
                        st.write(f"3️⃣ **Execute:** Action **{resolution_action}** executed via secure connector.")
                        st.success(f"**✅ Resolution Complete:** Action {resolution_action} executed autonomously.")
                        
                        if step == 3:
                            st.markdown("<br>", unsafe_allow_html=True)
                            if st.button("▶️ Run Audit Agent", type="primary", use_container_width=True):
                                st.session_state.investigation_step = 4
                                st.rerun()
            
            st.markdown('<div style="height: 2rem;"></div>', unsafe_allow_html=True)
        
        # ===== STEP 4: AUDIT =====
        if step >= 4:
            render_timeline_step("🔍", "Step 4: Explainability and Auditability", "complete")
            
            with st.container(border=True):
                with st.spinner("📝 Narrator Agent building human-readable audit bundle..."):
                    time.sleep(1)
                    
                    st.success("✅ **Audit Bundle Generated**")
                    
                    # Build audit log
                    audit_bundle = {"case_id": case_id, "steps": []}
                    audit_bundle["steps"].append({
                        "step": 1,
                        "agent": "Agent 1 (Parser)",
                        "action": "Ingest & Parse",
                        "details": "Parsed successfully."
                    })
                    
                    if is_pass_scenario:
                        audit_bundle["steps"].append({
                            "step": 2,
                            "agent": "Agent 2 (Triage)",
                            "action": "Validate",
                            "details": "All checks passed."
                        })
                    else:
                        audit_bundle["steps"].append({
                            "step": 2,
                            "agent": "Agent 2 (Triage)",
                            "action": "Diagnose",
                            "details": f"Root Cause: {data['root_cause']}"
                        })
                        audit_bundle["steps"].append({
                            "step": 3,
                            "agent": "Agent 3 (Resolution)",
                            "action": data['resolution_action'],
                            "details": f"Policy: {data['policy']}"
                        })
                        
                        if st.session_state.human_decision:
                            audit_bundle["steps"].append({
                                "step": 3.5,
                                "agent": "Human (Compliance L2)",
                                "action": "Manual Decision",
                                "details": st.session_state.human_decision
                            })
                    
                    st.code(json.dumps(audit_bundle, indent=2), language="json")
                    
                    st.markdown("---")
                    st.subheader("📄 Human-Readable Summary")
                    
                    if is_pass_scenario:
                        st.markdown("✅ Payment was processed successfully with no exceptions.")
                    else:
                        if data["message"]["payload"]["MsgId"] == "XYZ-789":
                            summary = (
                                "🔍 In this case, a **legacy SWIFT MT103** message was received. "
                                "**Agent 2 (Triage)** diagnosed a **Compliance Hit**. "
                                "**Agent 3 (Resolution)** denied autonomy and escalated to **Compliance_L2**."
                            )
                            if st.session_state.human_decision:
                                summary += f" A human analyst reviewed the case and **{st.session_state.human_decision}**."
                            else:
                                summary += " **Case is now pending manual review.**"
                            st.markdown(summary)
                        else:
                            st.markdown(f"⚠️ Payment failed with root cause: **{data['root_cause']}**. Resolution action: **{data['resolution_action']}**.")
                    
                    st.markdown("---")
                    st.header("✅ Investigation Complete")
                    st.toast(f'Case {case_id} successfully processed.', icon='✅')
                    
                    st.markdown("<br>", unsafe_allow_html=True)
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button("🏠 Return to Dashboard", use_container_width=True):
                            SessionStateManager.set_page("🏠 Dashboard")
                            st.rerun()
                    with col2:
                        if st.button("🔍 Start New Investigation", type="primary", use_container_width=True):
                            SessionStateManager.reset_investigation()
                            SessionStateManager.set_page("🔍 New Investigation")
                            st.rerun()

# ============================================================================
# SIDEBAR NAVIGATION
# ============================================================================

def render_sidebar():
    """Render the sidebar navigation."""
    with st.sidebar:
        render_logo(BIGTAPP_LOGO_PATH, width=120)
        
        st.header("Beeonix Platform")
        st.markdown("✨ *Agentic Investigation System*")
        
        # Main navigation
        main_nav_pages = ["🏠 Dashboard", "🔍 New Investigation", "📂 Case Registry", "📈 Analytics (Demo)"]
        
        try:
            current_index = main_nav_pages.index(st.session_state.page)
        except ValueError:
            current_index = None
        
        def handle_nav_change():
            st.session_state.page = st.session_state.main_nav_radio
            SessionStateManager.reset_investigation()
        
        st.radio(
            "Navigation",
            main_nav_pages,
            index=current_index,
            key="main_nav_radio",
            on_change=handle_nav_change
        )
        
        st.markdown("---")
        st.subheader("⚡ Work Queues")
        
        # HILT queue button
        hilt_count = len(st.session_state.hilt_cases)
        hilt_label = f"❗ Compliance L2 ({hilt_count})"
        
        if st.button(hilt_label, type="secondary", use_container_width=True):
            SessionStateManager.set_page("❗ Compliance L2")
            st.rerun()
        
        # Footer
        st.markdown("---")
        st.caption("© 2025 Beeonix AI")
        st.caption("Version 2.0.0")

# ============================================================================
# MAIN APPLICATION
# ============================================================================

def main():
    """Main application entry point."""
    # Page configuration
    config = PageConfig()
    st.set_page_config(
        page_title=config.title,
        page_icon=config.icon,
        layout=config.layout
    )
    
    # Initialize session state
    SessionStateManager.initialize()
    
    # Apply custom CSS
    apply_custom_css()
    
    # Render sidebar
    render_sidebar()
    
    # Route to appropriate page
    current_page = st.session_state.page
    
    if current_page == "🏠 Dashboard":
        render_dashboard()
    elif current_page == "🔍 New Investigation":
        render_new_investigation()
    elif current_page == "📂 Case Registry":
        render_case_registry()
    elif current_page == "📈 Analytics (Demo)":
        render_analytics()
    elif current_page == "❗ Compliance L2":
        render_hilt_queue()
    elif current_page == "Active Investigation":
        render_active_investigation()
    else:
        st.error(f"❌ Unknown page: {current_page}")

# ============================================================================
# ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    main()
