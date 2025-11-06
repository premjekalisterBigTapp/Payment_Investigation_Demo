import streamlit as st
import time
import json
import random

# --- Page Configuration ---
st.set_page_config(
    page_title="Beeonix Payments Investigation",
    page_icon="🐝",
    layout="wide"
)

# --- Define Logo Paths ---
beeonix_logo_path = r"D:\PremJeKalister\Projects_Official\Project_13\Beeonix_Demo\Beeonix AI Logo 1 (1).png"
bigtapp_logo_path = r"D:\PremJeKalister\Projects_Official\Project_13\Beeonix_Demo\Bigtapplogo 1.png"

# --- Custom CSS for Theming ---
cache_buster = random.randint(10000, 99999)

st.markdown(
    f"""
    <style>
    /* Cache Buster: {cache_buster} */
    /* ... [Rest of CSS is unchanged] ... */
    
    /* Gradient Background */
    [data-testid="stAppViewContainer"] {{
        background: linear-gradient(to right, #FFFFFF 0%, #E0F2F7 50%, #B3D9FF 100%);
    }}

    [data-testid="stHeader"] {{
        background-color: rgba(255, 255, 255, 0);
        color: #1F4A9F;
    }}

    [data-testid="stSidebar"] {{
        background-color: #F0F0F0;
        color: #303030;
        border-right: 1px solid #D0D0D0;
    }}

    .main .block-container {{
        background-color: #FFFFFF;
        border-radius: 10px;
        padding: 2rem;
        box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.1);
    }}

    :root {{
        --primary-color: #1F4A9F;
        --text-color: #303030;
    }}

    body, h3, h4, h5, h6, label, p, .st-bo, .st-bq {{
        color: var(--text-color);
    }}

    /* Header Rules */
    h1 {{
        color: #1F4A9F !important;
        font-size: 2.5em;
        text-align: center;
        padding-bottom: 10px;
        border-bottom: 2px solid #D0D0D0;
    }}
    h2, h3 {{
        color: #1F4A9F !important;
    }}

    /* --- CSS FIX: Center the markdown text below the title --- */
    .subtitle-text {{
        text-align: center;
    }}


    /* Button Styling */
    .stButton>button {{
        background-color: var(--primary-color);
        color: #FFFFFF !important;
        border: none;
        font-weight: bold;
        padding: 0.5rem 1rem;
        border-radius: 5px;
        transition: all 0.2s ease-in-out;
    }}
    .stButton>button:hover {{
        background-color: #163673;
        color: #FFFFFF;
    }}
    .stButton>button:active {{
        background-color: #0F254D;
        color: #FFFFFF;
    }}

    /* --- EXPANDERS (Step 1, Step 2, etc.) --- */
    [data-testid="stExpander"] {{
        background-color: #FFFFFF !important;
        border: 1px solid #D0D0D0 !important;
        border-radius: 8px !important;
        box-shadow: 0px 1px 4px rgba(0, 0, 0, 0.05);
        margin-bottom: 10px;
    }}

    [data-testid="stExpander"] > summary {{
        background: linear-gradient(90deg, #FFFFFF 0%, #F2F7FF 100%) !important;
        color: #1F4A9F !important;
        font-weight: 600 !important;
        font-size: 1.1em !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 10px 14px !important;
    }}

    [data-testid="stExpander"] > summary:hover {{
        background-color: #E6F0FF !important;
    }}

    [data-testid="stExpander"] svg {{
        fill: #1F4A9F !important;
    }}

    /* --- SELECTBOX (Dropdown) --- */
    [data-testid="stSelectbox"] div[data-baseweb="select"] > div {{
        background-color: #FFFFFF !important;
        color: #303030 !important;
        border: 1px solid #C0C0C0 !important;
        border-radius: 6px !important;
    }}

    [data-testid="stSelectbox"] div[data-baseweb="select"] span {{
        color: #303030 !important;
    }}

    div[data-baseweb="popover"] ul[role="listbox"] {{
        background-color: #FFFFFF !important;
        border: 1px solid #C0C0C0 !important;
        border-radius: 6px;
    }}

    div[data-baseweb="popover"] ul[role="listbox"] li {{
        background-color: #FFFFFF !important;
        color: #303030 !important;
    }}

    div[data-baseweb="popover"] ul[role="listbox"] li:hover {{
        background-color: #E6F0FF !important;
    }}

    /* --- !!! START: CORRECTED CODE BLOCK CSS !!! --- */
    pre, [data-testid="stCodeBlock"], [data-testid="stJson"], [data-testid="stJson"] > div {{
        background-color: #F0F2F6 !important;  /* This sets the light blue background */
        color: #1F4A9F !important;          /* This sets the default text to blue */
        border: 1px solid #D0D0D0;
        border-radius: 5px;
    }}

    /* This part forces ALL text inside the code block (including the highlighted parts) to be blue */
    [data-testid="stCodeBlock"] code,
    [data-testid="stCodeBlock"] code * {{
        background-color: transparent !important;
        color: #1F4A9F !important; /* Forces all text to be blue */
    }}
    /* --- !!! END: CORRECTED CODE BLOCK CSS !!! --- */

    [data-testid="stInfo"] {{
        background-color: #DDEBF7;
        border-color: #1F4A9F;
        color: #1F4A9F;
    }}

    </style>
    """,
    unsafe_allow_html=True
)

# --- Beeonix Logo ---
col1, col2, col3 = st.columns([3, 2, 3])
with col2:
    try:
        st.image(beeonix_logo_path, width=400)
    except Exception as e:
        st.error(f"Could not load Beeonix logo: {e}")

# --- Title ---
st.title("Beeonix: Agentic Payments Investigation")


# --- SCENARIOS (JSON Payloads) ---
# This map holds the "truth" - what the raw text *parses into*.
scenario_map = {
    "UAEFTS_FAIL": {
        "message": {"rail": "UAEFTS", "type": "pacs.008 (Rejection: pacs.002)", "payload": {"MsgId": "ABC-123", "Amt": "15000.00", "Ccy": "AED", "DbtrAcct": "AE290000000123456789012", "CdtrAcct": "AE8800000009876543210ZY"}},
        "root_cause": "INVALID_IBAN", "root_cause_details": "IBAN Checksum failed for CdtrAcct.", "policy": "LOW_RISK: IBAN checksum invalid. Autonomously recall payment.", "resolution_action": "RECALL", "resolution_draft": {"MsgType": "camt.056", "OriginalMsgId": "ABC-123"}
    },
    "SWIFT_MT103_FAIL": {
        "message": {"rail": "SWIFT", "type": "MT103 (International Wire)", "payload": {"MsgId": "XYZ-789", "Amt": "50000.00", "Ccy": "USD", "Dbtr": "John DDoe", "Cdtr": "Global Trading Inc."}},
        "root_cause": "COMPLIANCE_HIT: Name Mismatch", "root_cause_details": "Sender name 'John DDoe' failed sanction screening. Potential match: 'John Doe' (on watchlist).", "policy": "HIGH_RISK: Potential compliance hit. Deny autonomy. Escalate to 'Compliance_L2' for manual review.", "resolution_action": "HILT", "resolution_draft": {"CaseAction": "Escalate", "Queue": "Compliance_L2"}
    },
    "SWIFT_ISO20022_FAIL": {
        "message": {"rail": "SWIFT", "type": "pacs.008.001.08 (ISO 20022)", "payload": {"MsgId": "P-SWIFT-002", "Amt": "7500.00", "Ccy": "EUR", "Dbtr": {"Nm": "Demo Sender"}, "Cdtr": {"Nm": "Demo Receiver"}, "Purp": {"Cd": "INVALID_CODE"}}},
        "root_cause": "INVALID_PURPOSE_CODE", "root_cause_details": "ISO 20022 'Purpose Code' (INVALID_CODE) is not valid for this payment corridor. Rejected by intermediary.", "policy": "LOW_RISK: Invalid structured data. Autonomously recall payment.", "resolution_action": "RECALL", "resolution_draft": {"MsgType": "camt.056", "OriginalMsgId": "P-SWIFT-002"}
    },
    "IPI_FAIL": {
        "message": {"rail": "IPI", "type": "pacs.008", "payload": {"MsgId": "IPI-456", "Amt": "500.00", "Ccy": "AED", "DbtrAcct": "AE290000000123456789012", "CdtrAcct": "AE880000000987654321011"}},
        "root_cause": "DOWNSTREAM_TIMEOUT", "root_cause_details": "No response from Core Banking System within 3-second SLA.", "policy": "LOW_RISK: System timeout. Autonomously retry payment (Attempt 1/3).", "resolution_action": "RETRY", "resolution_draft": {"MsgType": "pacs.008", "OriginalMsgId": "IPI-456", "RetryAttempt": 1}
    },
    "UAEFTS_PASS": {
        "message": {"rail": "UAEFTS", "type": "pacs.008", "payload": {"MsgId": "PASS-UAE-001", "Amt": "250000.00", "Ccy": "AED", "DbtrAcct": "AE290000000111111111111", "CdtrAcct": "AE880000000222222222222"}},
        "root_cause": "N/A - PASS", "root_cause_details": "All checks passed.", "policy": "N/A", "resolution_action": "PASS", "resolution_draft": {}
    },
    "SWIFT_MT103_PASS": {
        "message": {"rail": "SWIFT", "type": "MT103 (International Wire)", "payload": {"MsgId": "PASS-MT-002", "Amt": "120000.00", "Ccy": "USD", "Dbtr": "Valid Sender Inc", "Cdtr": "Valid Receiver LLC"}},
        "root_cause": "N/A - PASS", "root_cause_details": "All checks passed.", "policy": "N/A", "resolution_action": "PASS", "resolution_draft": {}
    },
    "SWIFT_ISO20022_PASS": {
        "message": {"rail": "SWIFT", "type": "pacs.008.001.08 (ISO 20022)", "payload": {"MsgId": "PASS-ISO-003", "Amt": "95000.00", "Ccy": "EUR", "Dbtr": {"Nm": "Valid Sender GmbH"}, "Cdtr": {"Nm": "Valid Receiver S.A."}, "Purp": {"Cd": "GDDS"}}},
        "root_cause": "N/A - PASS", "root_cause_details": "All checks passed.", "policy": "N/A", "resolution_action": "PASS", "resolution_draft": {}
    },
    "IPI_PASS": {
        "message": {"rail": "IPI", "type": "pacs.008", "payload": {"MsgId": "PASS-IPI-004", "Amt": "150.00", "Ccy": "AED", "DbtrAcct": "AE290000000111111111111", "CdtrAcct": "AE880000000222222222222"}},
        "root_cause": "N/A - PASS", "root_cause_details": "All checks passed.", "policy": "N/A", "resolution_action": "PASS", "resolution_draft": {}
    }
}

# --- NEW: RAW MESSAGE MAP ---
# This map holds the "raw text" that the user will paste.
# The app will find the key (e.g., "SWIFT_MT103_FAIL") by matching this raw text.
raw_message_map = {
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


# --- Sidebar ---
with st.sidebar:
    try:
        st.image(bigtapp_logo_path, width=120)
    except Exception as e:
        st.error(f"Could not load Bigtapp logo: {e}")

    st.header("Demo Controls")
    
    # --- UPDATED: Text Area for pasting the RAW message ---
    # We pre-populate it with the MT103 Fail scenario
    default_raw_message = raw_message_map["SWIFT_MT103_FAIL"]
    
    ingested_message_str = st.text_area(
        "Paste Raw Payment Message (MT103 or XML):",
        value=default_raw_message,
        height=300
    )
    
    start_button = st.button("Start Investigation", type="primary")


# --- Main Page Content ---
st.markdown("<p class='subtitle-text'>This simulation demonstrates the autonomous flow for processing payment messages.</p>", unsafe_allow_html=True)


# --- Main Logic ---
if start_button:
    
    scenario_key_to_run = None
    
    # --- UPDATED: New logic to find the scenario from the RAW text ---
    try:
        # Trim whitespace to ensure a clean match
        ingested_raw_text = ingested_message_str.strip()

        # Find the matching scenario key by comparing raw text
        for key, raw_text in raw_message_map.items():
            if raw_text.strip() == ingested_raw_text:
                scenario_key_to_run = key
                break
        
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")
        scenario_key_to_run = None # Ensure we don't proceed

    # --- End of new parsing logic ---

    if scenario_key_to_run:
        scenario_data = scenario_map[scenario_key_to_run]
        
        # --- This is the "Pass Check" logic ---
        if scenario_data["resolution_action"] == "PASS":
            case_id = f"CASE-{time.strftime('%H%M%S')}"
            
            # --- UPDATED STEP 1 (for PASS) ---
            with st.expander(f"**Step 1: Ingestion & Parsing (Agent 1 / Case: {case_id})**", expanded=True):
                st.info(f"Ingestion layer received message from **{scenario_data['message']['rail']}**.")
                st.write("Raw message received:")
                st.code(ingested_message_str, language="text") # Show the raw text
                time.sleep(1)
                st.write(f"✅ **MsgParse Agent** successfully parsed message:")
                st.code(json.dumps(scenario_data['message'], indent=2), language="json") # Show the parsed JSON
                time.sleep(0.5)
                st.write(f"✅ **Agentic Supervisor** initiated check...")
            
            with st.expander("**Step 2: Validation & Resolution**", expanded=True):
                with st.spinner("Agent is performing validation checks..."):
                    time.sleep(1)
                    st.write("...`FieldValidator Agent` running...")
                    time.sleep(0.5)
                    st.write("...`ScreenContext Agent` running...")
                    time.sleep(1)
                st.success("**Validation Complete: All checks passed.**")

            st.header(f"Investigation Complete: {case_id} (PASS)")
            st.toast(f'Case {case_id} successfully processed (PASS).', icon='✅')

        # --- This is the "Fail" scenario logic ---
        else:
            selected_message = scenario_data["message"]
            root_cause = scenario_data["root_cause"]
            root_cause_details = scenario_data["root_cause_details"]
            policy = scenario_data["policy"]
            resolution_action = scenario_data["resolution_action"]
            resolution_draft = scenario_data["resolution_draft"]
            case_id = f"CASE-{time.strftime('%H%M%S')}"

            # --- UPDATED STEP 1 (for FAIL) ---
            with st.expander(f"**Step 1: Ingestion & Parsing (Agent 1 / Case: {case_id})**", expanded=True):
                st.info(f"Ingestion layer received message from **{selected_message['rail']}**.")
                st.write("Raw message received:")
                st.code(ingested_message_str, language="text") # Show the raw text
                time.sleep(1)
                st.write(f"✅ **MsgParse Agent** successfully parsed message:")
                st.code(json.dumps(selected_message, indent=2), language="json") # Show the parsed JSON
                time.sleep(1)
                st.write(f"✅ **Agentic Supervisor** initiated triage. Assigned **{case_id}**.")


            # --- STEP 2 ---
            with st.expander("**Step 2: Agentic Triage and Diagnosis (Agent 2)**", expanded=True):
                with st.spinner("Agent 2 is investigating the parsed data..."):
                    time.sleep(1)
                    st.write("...`FieldValidator Agent` running (checking rules)...")
                    time.sleep(1)
                    st.write("...`UETRTrace Agent` running (tracing transaction history)...")
                    time.sleep(1)
                    st.write("...`ScreenContext Agent` running (screening for compliance)...")
                    time.sleep(2)

                st.error(f"**Diagnosis Complete:** Root cause identified: **{root_cause}**")
                st.write(f"**Details:** {root_cause_details}")

            # --- STEP 3 ---
            with st.expander("**Step 3: Autonomous Resolution (Agent 3)**", expanded=True):
                if resolution_action == "HILT":
                    with st.spinner("Agent 3 is checking policy..."):
                        time.sleep(1)
                        st.write(f"1. **Plan:** Checking policy for **{root_cause}**...")
                        time.sleep(1)
                        st.error(f"**Policy Found:** {policy}")

                    st.warning(f"**Resolution:** Autonomy DENIED. Escalating to human analyst (HILT).")

                else:
                    with st.spinner("Agent 3 is resolving autonomously..."):
                        time.sleep(1)
                        st.write(f"1. **Plan:** Checking policy for **{root_cause}**...")
                        time.sleep(1)
                        st.success(f"**Policy Found:** {policy}")
                        time.sleep(1)
                        st.write(f"2. **Draft:** Drafting remediation. Action: **{resolution_action}**.")
                        st.code(json.dumps(resolution_draft, indent=2), language="text")
                        time.sleep(1)
                        st.write(f"3. **Execute:** Action **{resolution_action}** executed via secure connector to **{selected_message['rail']}**.")
                        time.sleep(0.5)
                        st.write("4. **Log:** All steps logged to immutable audit store.")

                    st.success(f"**Resolution Complete:** Action {resolution_action} executed autonomously.")

            # --- STEP 4 ---
            with st.expander("**Step 4: Explainability and Auditability (Agent 4)**", expanded=True):
                audit_bundle = {}
                with st.spinner("...Narrator Agent building human-readable audit bundle..."):
                    time.sleep(2)
                    audit_bundle = {
                        "case_id": case_id,
                        "scenario_key": scenario_key_to_run,
                        "steps": [
                            {"step": 1, "agent": "Agent 1 (Parser)", "action": "Ingest & Parse",
                             "details": f"Received {selected_message['type']} from {selected_message['rail']}. Parsed successfully."},
                            {"step": 2, "agent": "Agent 2 (Triage)", "action": "Diagnose",
                             "details": f"Root Cause: {root_cause}. Details: {root_cause_details}"},
                            {"step": 3, "agent": "Agent 3 (Resolution)", "action": resolution_action,
                             "details": f"Policy: {policy}. Draft: {json.dumps(resolution_draft)}"}
                        ]
                    }

                st.success("✅ **Audit Bundle Generated**")
                st.write("This bundle provides a complete, human-readable trail for compliance and regulatory review.")
                st.code(json.dumps(audit_bundle, indent=2), language="text")

                # Human-Readable Summary
                st.subheader("Human-Readable Summary")
                
                if scenario_key_to_run == "UAEFTS_FAIL":
                    st.markdown(
                        """
                        In this case, a **UAEFTS** XML message was rejected.
                        **Agent 1 (Parser)** ingested the raw XML and converted it to clean JSON.
                        **Agent 2 (Triage)** diagnosed the problem as an **Invalid IBAN**.
                        **Agent 3 (Resolution)** autonomously issued a `camt.056` (recall) message.
                        """
                    )
                elif scenario_key_to_run == "SWIFT_MT103_FAIL":
                    st.markdown(
                        """
                        In this case, a **legacy SWIFT MT103** message was received.
                        **Agent 1 (Parser)** ingested the raw text and converted it to clean JSON.
                        **Agent 2 (Triage)** diagnosed a **Compliance Hit** (name mismatch 'John DDoe').
                        **Agent 3 (Resolution)** denied autonomy and escalated to **Compliance_L2**.
                        """
                    )
                elif scenario_key_to_run == "SWIFT_ISO20022_FAIL":
                     st.markdown(
                        """
                        In this case, a **new ISO 20022 `pacs.008`** XML message was received.
                        **Agent 1 (Parser)** ingested the raw XML and converted it to clean JSON.
                        **Agent 2 (Triage)** diagnosed a structured data error: **Invalid 'Purpose of Payment' Code**.
                        **Agent 3 (Resolution)** autonomously issued a `camt.056` (recall) message.
                        """
                    )
                elif scenario_key_to_run == "IPI_FAIL":
                    st.markdown(
                        """
                        In this case, an **IPI (Instant Payment)** XML message failed.
                        **Agent 1 (Parser)** ingested the raw XML and converted it to clean JSON.
                        **Agent 2 (Triage)** diagnosed a **Downstream Timeout**.
                        **Agent 3 (Resolution)** autonomously retried the payment.
                        """
                    )

            st.header(f"Investigation Complete: {case_id}")
            st.toast(f'Case {case_id} successfully processed.', icon='✅')
    
    # --- This 'else' now catches if no matching raw text was found ---
    else:
        st.error("Error: Ingested message not recognized. Please paste one of the 8 pre-defined raw scenarios.")