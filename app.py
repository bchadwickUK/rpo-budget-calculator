import streamlit as st
import pandas as pd
import altair as alt

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="RPO Strategy Engine", 
    layout="wide", 
    page_icon="📊"
)

# --- CUSTOM CSS (SAFE MODE) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Roboto', sans-serif;
    }
    
    /* Primary Buttons */
    div.stButton > button:first-child {
        background-color: #4285F4;
        color: white;
        border: none;
        border-radius: 4px;
        box-shadow: 0 1px 2px rgba(0,0,0,0.1);
        font-weight: 500;
    }
    div.stButton > button:first-child:hover {
        background-color: #3367D6;
        color: white;
    }

    /* Metric Cards */
    [data-testid="stMetricValue"] {
        font-size: 1.8rem !important;
        font-weight: 400;
    }
    
    /* Clean up tables */
    thead tr th:first-child {display:none}
    tbody th {display:none}
</style>
""", unsafe_allow_html=True)

# --- PASSWORD PROTECTION ---
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    c1, c2, c3 = st.columns([1,1,1])
    with c2:
        st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/c/c1/Google_%22G%22_logo.svg/480px-Google_%22G%22_logo.svg.png", width=100)
        st.write("### RPO Strategy Engine")
        password = st.text_input("Passcode", type="password", label_visibility="collapsed")
        if st.button("Sign In"):
            if password == "1963":
                st.session_state.logged_in = True
                st.rerun()
            else:
                st.error("Access Denied")
        st.stop()

# --- DATA SETUP ---
if 'budget_lines' not in st.session_state:
    st.session_state.budget_lines = []

# A/B Scenarios
if 'scenario_a' not in st.session_state:
    st.session_state.scenario_a = []
if 'scenario_b' not in st.session_state:
    st.session_state.scenario_b = []

# 1. WORKFLOW DATA
workflow_data = {
    'Role': [
        'SWE', 'SWE', 'SWE',
        'SRE', 'SRE', 'SRE',
        'TPgM', 'TPgM', 'TPgM',
        'GBOFx', 'GBOFx', 'GBOFx'
    ],
    'Supplier': ['RSR', 'KF', 'Cielo'] * 4,
    'Pricing Tier': ['T6', 'T6', 'T6'] * 3 + ['T4', 'T4', 'T4']
}
df_workflows = pd.DataFrame(workflow_data)
df_workflows['Workflow Name'] = df_workflows['Role'] + " - " + df_workflows['Supplier']

# 2. PRICING DATA
pricing_data = [
    # --- CIELO (BLENDED RATES) ---
    {'Supplier': 'Cielo', 'Tier': 'T1', 'Cost_Type': 'Blended', 'Price': 1940},
    {'Supplier': 'Cielo', 'Tier': 'T2', 'Cost_Type': 'Blended', 'Price': 2224},
    {'Supplier': 'Cielo', 'Tier': 'T3', 'Cost_Type': 'Blended', 'Price': 2841},
    {'Supplier': 'Cielo', 'Tier': 'T4', 'Cost_Type': 'Blended', 'Price': 3401},
    {'Supplier': 'Cielo', 'Tier': 'T5', 'Cost_Type': 'Blended', 'Price': 3841},
    {'Supplier': 'Cielo', 'Tier': 'T6', 'Cost_Type': 'Blended', 'Price': 4849},
    {'Supplier': 'Cielo', 'Tier': 'T7', 'Cost_Type': 'Blended', 'Price': 6141},

    # --- KEEP RSR AND KF BELOW ---
    {'Supplier': 'RSR', 'Tier': 'T1', 'Cost_Type': 'High Cost', 'Price': 3359},
    {'Supplier': 'RSR', 'Tier': 'T2', 'Cost_Type': 'High Cost', 'Price': 4079},
    {'Supplier': 'RSR', 'Tier': 'T3', 'Cost_Type': 'High Cost', 'Price': 5191},
    {'Supplier': 'RSR', 'Tier': 'T4', 'Cost_Type': 'High Cost', 'Price': 7138},
    {'Supplier': 'RSR', 'Tier': 'T5', 'Cost_Type': 'High Cost', 'Price': 6638},
    {'Supplier': 'RSR', 'Tier': 'T6', 'Cost_Type': 'High Cost', 'Price': 9482},
    {'Supplier': 'RSR', 'Tier': 'T7', 'Cost_Type': 'High Cost', 'Price': 13276},
    {'Supplier': 'RSR', 'Tier': 'T1', 'Cost_Type': 'Medium Cost', 'Price': 3119},
    {'Supplier': 'RSR', 'Tier': 'T2', 'Cost_Type': 'Medium Cost', 'Price': 3787},
    {'Supplier': 'RSR', 'Tier': 'T3', 'Cost_Type': 'Medium Cost', 'Price': 4820},
    {'Supplier': 'RSR', 'Tier': 'T4', 'Cost_Type': 'Medium Cost', 'Price': 6627},
    {'Supplier': 'RSR', 'Tier': 'T5', 'Cost_Type': 'Medium Cost', 'Price': 6058},
    {'Supplier': 'RSR', 'Tier': 'T6', 'Cost_Type': 'Medium Cost', 'Price': 8654},
    {'Supplier': 'RSR', 'Tier': 'T7', 'Cost_Type': 'Medium Cost', 'Price': 12116},
    {'Supplier': 'RSR', 'Tier': 'T1', 'Cost_Type': 'Medium/Low Cost', 'Price': 2780},
    {'Supplier': 'RSR', 'Tier': 'T2', 'Cost_Type': 'Medium/Low Cost', 'Price': 3376},
    {'Supplier': 'RSR', 'Tier': 'T3', 'Cost_Type': 'Medium/Low Cost', 'Price': 4297},
    {'Supplier': 'RSR', 'Tier': 'T4', 'Cost_Type': 'Medium/Low Cost', 'Price': 5908},
    {'Supplier': 'RSR', 'Tier': 'T5', 'Cost_Type': 'Medium/Low Cost', 'Price': 5150},
    {'Supplier': 'RSR', 'Tier': 'T6', 'Cost_Type': 'Medium/Low Cost', 'Price': 7357},
    {'Supplier': 'RSR', 'Tier': 'T7', 'Cost_Type': 'Medium/Low Cost', 'Price': 10300},
    {'Supplier': 'RSR', 'Tier': 'T1', 'Cost_Type': 'Low Cost', 'Price': 1597},
    {'Supplier': 'RSR', 'Tier': 'T2', 'Cost_Type': 'Low Cost', 'Price': 1939},
    {'Supplier': 'RSR', 'Tier': 'T3', 'Cost_Type': 'Low Cost', 'Price': 2468},
    {'Supplier': 'RSR', 'Tier': 'T4', 'Cost_Type': 'Low Cost', 'Price': 3393},
    {'Supplier': 'RSR', 'Tier': 'T5', 'Cost_Type': 'Low Cost', 'Price': 3214},
    {'Supplier': 'RSR', 'Tier': 'T6', 'Cost_Type': 'Low Cost', 'Price': 4592},
    {'Supplier': 'RSR', 'Tier': 'T7', 'Cost_Type': 'Low Cost', 'Price': 6428},
    {'Supplier': 'KF', 'Tier': 'T1', 'Cost_Type': 'High Cost', 'Price': 2664},
    {'Supplier': 'KF', 'Tier': 'T2', 'Cost_Type': 'High Cost', 'Price': 3185},
    {'Supplier': 'KF', 'Tier': 'T3', 'Cost_Type': 'High Cost', 'Price': 4125},
    {'Supplier': 'KF', 'Tier': 'T4', 'Cost_Type': 'High Cost', 'Price': 5558},
    {'Supplier': 'KF', 'Tier': 'T5', 'Cost_Type': 'High Cost', 'Price': 5020},
    {'Supplier': 'KF', 'Tier': 'T6', 'Cost_Type': 'High Cost', 'Price': 7171},
    {'Supplier': 'KF', 'Tier': 'T7', 'Cost_Type': 'High Cost', 'Price': 10040},
    {'Supplier': 'KF', 'Tier': 'T1', 'Cost_Type': 'Low Cost', 'Price': 2331},
    {'Supplier': 'KF', 'Tier': 'T2', 'Cost_Type': 'Low Cost', 'Price': 2809},
    {'Supplier': 'KF', 'Tier': 'T3', 'Cost_Type': 'Low Cost', 'Price': 3546},
    {'Supplier': 'KF', 'Tier': 'T4', 'Cost_Type': 'Low Cost', 'Price': 4835},
    {'Supplier': 'KF', 'Tier': 'T5', 'Cost_Type': 'Low Cost', 'Price': 4377},
    {'Supplier': 'KF', 'Tier': 'T6', 'Cost_Type': 'Low Cost', 'Price': 6253},
    {'Supplier': 'KF', 'Tier': 'T7', 'Cost_Type': 'Low Cost', 'Price': 8754},
]
df_pricing = pd.DataFrame(pricing_data)

# --- FUNCTIONS ---
def get_price(supplier, tier, cost_type):
    row = df_pricing[(df_pricing['Supplier'] == supplier) & (df_pricing['Tier'] == tier) & (df_pricing['Cost_Type'] == cost_type)]
    if not row.empty: return row.iloc[0]['Price']
    return 0

# --- SIDEBAR ---
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/c/c1/Google_%22G%22_logo.svg/480px-Google_%22G%22_logo.svg.png", width=40)
    
    # --- TOP LEVEL NAVIGATION ---
    mode = st.radio(
        "Select Mode:",
        ["📝 Budget Builder", "⚡ Quick Compare"],
        index=0,
        label_visibility="collapsed"
    )
    
    st.divider()

    # --- A/B TOGGLE (Comparison Mode Only) ---
    active_scenario = "Budget" # Default for Builder
    if mode == "⚡ Quick Compare":
        st.write("### 🔀 Comparison Toggle")
        active_scenario = st.radio(
            "Add lines to:",
            ["Scenario A", "Scenario B"],
            label_visibility="collapsed"
        )
        st.divider()

    # --- INPUT FORM ---
    st.write("### ⚙️ Configure Workflow")
    
    unique_roles = df_workflows['Role'].unique()
    selected_role = st.selectbox("1. Role", unique_roles)
    
    available_suppliers = df_workflows[df_workflows['Role'] == selected_role]['Supplier'].unique()
    selected_supplier = st.selectbox("2. Supplier", available_suppliers)
    
    wf_details = df_workflows[
        (df_workflows['Role'] == selected_role) & 
        (df_workflows['Supplier'] == selected_supplier)
    ].iloc[0]

    st.caption(f"Standard Tier: {wf_details['Pricing Tier']}")
    
    curr_supplier = wf_details['Supplier']
    wf_name_backend = wf_details['Workflow Name']

    # Simplified Tier Override
    with st.expander("🛠️ Manual Tier Override"):
        override_active = st.checkbox("Enable Override", value=False)
        if override_active:
            calc_tier = st.selectbox("Select Tier:", ['T1','T2','T3','T4','T5','T6','T7'], index=['T1','T2','T3','T4','T5','T6','T7'].index(wf_details['Pricing Tier']))
        else:
            calc_tier = wf_details['Pricing Tier']

    # --- INPUT GROUP 2: VOLUME & LOCATION ---
    st.divider()
    
    # 1. Volume Input (Conditional Layout)
    st.write("📊 **Volume & Phasing**")
    use_quarterly = st.checkbox("Enable Quarterly Phasing", value=False)

    if use_quarterly:
        cq1, cq2 = st.columns(2)
        cq3, cq4 = st.columns(2)
        with cq1: q1_vol = st.number_input("Q1", min_value=0, value=10)
        with cq2: q2_vol = st.number_input("Q2", min_value=0, value=10)
        with cq3: q3_vol = st.number_input("Q3", min_value=0, value=10)
        with cq4: q4_vol = st.number_input("Q4", min_value=0, value=10)
        total_demand = q1_vol + q2_vol + q3_vol + q4_vol
        st.caption(f"**Total Annual Demand: {total_demand}**")
    else:
        total_demand = st.number_input("Annual Demand", min_value=1, value=50)
        # Store 0 for breakdown if not used
        q1_vol, q2_vol, q3_vol, q4_vol = 0, 0, 0, 0
    
    # 2. Location Split (Grid Layout)
    st.write("📍 **Location Split (%)**")
    
    # Check for blended
    is_blended = (curr_supplier == 'Cielo')
    
    # Create 2 Columns for compact view
    c_loc1, c_loc2 = st.columns(2)
    
    with c_loc1:
        lon_pct = st.number_input("London %", 0, 100, 50, disabled=is_blended)
        dub_pct = st.number_input("Dublin %", 0, 100, 0, disabled=is_blended)
        
    with c_loc2:
        war_pct = st.number_input("Warsaw %", 0, 100, 50, disabled=is_blended)
        if curr_supplier == 'RSR': 
            bir_pct = st.number_input("Birmingham %", 0, 100, 0, disabled=is_blended)
        else:
            bir_pct = 0
    
    total_split = lon_pct + war_pct + dub_pct + bir_pct
    
    # Validation Logic
    btn_disabled = False
    if not is_blended and total_split != 100:
        st.error(f"⚠️ Total Split: {total_split}% (Must be 100%)")
        btn_disabled = True

    # Button Logic
    if mode == "⚡ Quick Compare":
        if "Scenario A" in active_scenario:
            btn_text = "Add to Scenario A"
            btn_color = "primary" # Normal blue
        else:
            btn_text = "Add to Scenario B"
            btn_color = "secondary" # Grey/White to differentiate
    else:
        btn_text = "Add to Budget"
        btn_color = "primary"

    if st.button(btn_text, disabled=btn_disabled, type="primary" if btn_color=="primary" else "secondary", use_container_width=True):
        # 1. CALCULATE COST
        if is_blended:
            vol_lon = 0
            vol_war = 0
            vol_dub = 0
            vol_bir = 0
            blended_price = get_price(curr_supplier, calc_tier, 'Blended')
            total_cost = total_demand * blended_price
        else:
            vol_lon = total_demand * (lon_pct/100)
            vol_war = total_demand * (war_pct/100)
            vol_dub = total_demand * (dub_pct/100)
            vol_bir = total_demand * (bir_pct/100)
            
            price_lon = get_price(curr_supplier, calc_tier, 'High Cost')
            price_war = get_price(curr_supplier, calc_tier, 'Low Cost')
            price_bir = get_price(curr_supplier, calc_tier, 'Medium/Low Cost')
            
            if curr_supplier == 'KF': price_dub = get_price(curr_supplier, calc_tier, 'High Cost')
            else: price_dub = get_price(curr_supplier, calc_tier, 'Medium Cost')

            total_cost = (vol_lon * price_lon) + (vol_war * price_war) + (vol_dub * price_dub) + (vol_bir * price_bir)
            
        wf_display_name = wf_name_backend
        if override_active: wf_display_name += f" (Override: {calc_tier})"

        # Calculate Quarterly Costs
        unit_price = total_cost / total_demand if total_demand > 0 else 0
        
        if use_quarterly:
            c_q1 = q1_vol * unit_price
            c_q2 = q2_vol * unit_price
            c_q3 = q3_vol * unit_price
            c_q4 = q4_vol * unit_price
        else:
            c_q1, c_q2, c_q3, c_q4 = 0, 0, 0, 0

        new_line = {
            "Workflow": wf_display_name,
            "Supplier": curr_supplier,
            "Demand": total_demand,
            "Tier": calc_tier,
            "Total Cost (€)": total_cost,
            "Lon OA": vol_lon,
            "War OA": vol_war,
            "Dub OA": vol_dub,
            "Bir OA": vol_bir,
            # STORE PCT FOR BREAKDOWN
            "Lon %": lon_pct, "War %": war_pct, "Dub %": dub_pct, "Bir %": bir_pct,
            # QUARTERLY DATA
            "Q1 Vol": q1_vol, "Q2 Vol": q2_vol, "Q3 Vol": q3_vol, "Q4 Vol": q4_vol,
            "Q1 Cost": c_q1, "Q2 Cost": c_q2, "Q3 Cost": c_q3, "Q4 Cost": c_q4
        }

        if mode == "📝 Budget Builder":
            st.session_state.budget_lines.append(new_line)
            st.toast("Added to Budget!")
        elif "Scenario A" in active_scenario:
            st.session_state.scenario_a.append(new_line)
            st.toast("Added to Scenario A!")
        else:
            st.session_state.scenario_b.append(new_line)
            st.toast("Added to Scenario B!")

# --- MAIN PAGE LOGIC ---
st.title("RPO Architect")
usd_rate = 1.15

# --- MODE 1: BUILDER VIEW ---
if mode == "📝 Budget Builder":
    st.subheader("📝 Single Budget Builder")
    
    if len(st.session_state.budget_lines) > 0:
        df_results = pd.DataFrame(st.session_state.budget_lines)
        
        # AGGREGATE TOTALS
        total_eur = df_results['Total Cost (€)'].sum()
        total_usd = total_eur * usd_rate
        total_vol = df_results['Demand'].sum()
        avg_cpoa = total_usd / total_vol if total_vol > 0 else 0
        
        # QUARTERLY TOTALS
        q1_tot = df_results['Q1 Cost'].sum() * usd_rate
        q2_tot = df_results['Q2 Cost'].sum() * usd_rate
        q3_tot = df_results['Q3 Cost'].sum() * usd_rate
        q4_tot = df_results['Q4 Cost'].sum() * usd_rate
        
        # ROW 1: PRIMARY METRICS
        c1, c2, c3 = st.columns(3)
        c1.metric("Forecast (USD)", f"${total_usd:,.0f}")
        c2.metric("Forecast (EUR)", f"€{total_eur:,.0f}")
        c3.metric("Avg CPOA", f"${avg_cpoa:,.0f}")
        
        # ROW 2: QUARTERLY BREAKDOWN (CONDITIONAL)
        if (q1_tot + q2_tot + q3_tot + q4_tot) > 0:
            cq1, cq2, cq3, cq4 = st.columns(4)
            cq1.metric("Q1 (USD)", f"${q1_tot:,.0f}")
            cq2.metric("Q2 (USD)", f"${q2_tot:,.0f}")
            cq3.metric("Q3 (USD)", f"${q3_tot:,.0f}")
            cq4.metric("Q4 (USD)", f"${q4_tot:,.0f}")
        
        st.divider()
        
        # --- VIEW TOGGLE ---
        view_mode = st.radio("Table View:", ["Summary", "📅 Quarterly Detail"], horizontal=True, label_visibility="collapsed")

        # PREPARE DISPLAY DATA
        df_display = df_results.copy()
        
        # Standard Formatting
        df_display['CPOA ($)'] = (df_display['Total Cost (€)'] * usd_rate) / df_display['Demand']
        df_display['Total Cost ($)'] = (df_display['Total Cost (€)'] * usd_rate).apply(lambda x: f"${x:,.0f}")
        df_display['Total Cost (€)'] = df_display['Total Cost (€)'].apply(lambda x: f"€{x:,.0f}")
        df_display['CPOA ($)'] = df_display['CPOA ($)'].apply(lambda x: f"${x:,.0f}")
        
        for col in ["Lon OA", "War OA", "Dub OA", "Bir OA"]:
            df_display[col] = df_display[col].apply(lambda x: f"{x:.1f}")

        if view_mode == "Summary":
            # EXISTING SUMMARY VIEW
            st.dataframe(
                df_display[["Workflow", "Supplier", "Demand", "Lon OA", "War OA", "Dub OA", "Bir OA", "CPOA ($)", "Total Cost ($)"]], 
                use_container_width=True
            )
        else:
            # NEW VERTICAL QUARTERLY VIEW
            vertical_rows = []
            
            for index, row in df_results.iterrows():
                # Process each quarter
                quarters = [
                    ("Q1", row['Q1 Vol'], row['Q1 Cost']),
                    ("Q2", row['Q2 Vol'], row['Q2 Cost']),
                    ("Q3", row['Q3 Vol'], row['Q3 Cost']),
                    ("Q4", row['Q4 Vol'], row['Q4 Cost'])
                ]
                
                for q_name, q_vol, q_cost in quarters:
                    # Show all quarters if Demand exists
                    if row['Demand'] > 0:
                        l_o = q_vol * (row['Lon %'] / 100)
                        w_o = q_vol * (row['War %'] / 100)
                        d_o = q_vol * (row['Dub %'] / 100)
                        b_o = q_vol * (row['Bir %'] / 100)
                        
                        cost_usd = q_cost * usd_rate
                        
                        vertical_rows.append({
                            "Workflow": row['Workflow'],
                            "Period": q_name,
                            "Volume": q_vol,
                            "Lon": f"{l_o:.1f}",
                            "War": f"{w_o:.1f}",
                            "Dub": f"{d_o:.1f}",
                            "Bir": f"{b_o:.1f}",
                            "Cost ($)": f"${cost_usd:,.0f}"
                        })

            if len(vertical_rows) > 0:
                df_vert = pd.DataFrame(vertical_rows)
                st.dataframe(df_vert, use_container_width=True)
            else:
                st.info("ℹ️ No quarterly data found. Check 'Enable Quarterly Phasing' when adding lines to see this view.")
        
        st.divider()
        st.write("### 🛠️ Manage Data")
        
        c_m1, c_m2, c_m3 = st.columns(3)
        
        with c_m1:
            csv = df_results.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Download CSV",
                data=csv,
                file_name="rpo_budget_draft.csv",
                mime="text/csv",
                use_container_width=True
            )
            
        with c_m2:
            del_options = [f"{i+1}. {row['Workflow']} ({row['Demand']})" for i, row in enumerate(st.session_state.budget_lines)]
            selected_del = st.selectbox("Select line to remove", del_options, label_visibility="collapsed")
            
            if st.button("🗑️ Remove Line", use_container_width=True):
                if selected_del:
                    idx_to_del = int(selected_del.split(".")[0]) - 1
                    st.session_state.budget_lines.pop(idx_to_del)
                    st.rerun()

        with c_m3:
             if st.button("💥 Clear All", type="primary", use_container_width=True):
                st.session_state.budget_lines = []
                st.rerun()

    else:
        st.info("👈 Select inputs in the sidebar and click **'Add to Budget'**.")

# --- MODE 2: A/B COMPARE VIEW ---
elif mode == "⚡ Quick Compare":
    st.subheader("⚡ A/B Scenario Comparison")
    
    # SCENARIO NAMING
    with st.expander("⚙️ Scenario Names", expanded=False):
        c_name1, c_name2 = st.columns(2)
        name_a = c_name1.text_input("Label for Scenario A", value="Scenario A (Baseline)")
        name_b = c_name2.text_input("Label for Scenario B", value="Scenario B (Proposed)")

    # 1. Calc Totals
    cost_a, cost_b = 0, 0
    df_a = pd.DataFrame()
    df_b = pd.DataFrame()
    
    if st.session_state.scenario_a:
        df_a = pd.DataFrame(st.session_state.scenario_a)
        cost_a = (df_a['Total Cost (€)'].sum()) * usd_rate
        df_a['Scenario'] = name_a 
        
    if st.session_state.scenario_b:
        df_b = pd.DataFrame(st.session_state.scenario_b)
        cost_b = (df_b['Total Cost (€)'].sum()) * usd_rate
        df_b['Scenario'] = name_b 
    
    # 2. Executive Scoreboard
    col1, col2, col3 = st.columns(3)
    col1.metric(name_a, f"${cost_a:,.0f}")
    
    # Delta Logic (Corrected Green/Red arrow)
    val_delta = cost_b - cost_a
    fmt_delta = f"-${abs(val_delta):,.0f}" if val_delta < 0 else f"${val_delta:,.0f}"
    col2.metric(name_b, f"${cost_b:,.0f}", delta=fmt_delta, delta_color="inverse")
    
    # --- NATURAL LANGUAGE SUMMARY (NEW) ---
    if cost_a > 0 and cost_b > 0:
        pct_change = ((cost_b - cost_a) / cost_a) * 100
        if val_delta < 0:
            st.success(f"✅ **Savings Opportunity:** By adopting {name_b}, you would save **${abs(val_delta):,.0f}** ({pct_change:.1f}%) annually vs. the baseline.")
        elif val_delta > 0:
            st.error(f"📈 **Investment Required:** {name_b} requires an additional investment of **${val_delta:,.0f}** (+{pct_change:.1f}%) annually vs. the baseline.")
        else:
            st.info("⚖️ **Neutral Impact:** Both scenarios have the exact same annual cost.")

    # 3. Stacked Chart (Visual Upgrade)
    st.divider()
    if not df_a.empty or not df_b.empty:
        # Prepare Data for Stacked Chart
        # We need a single DF with: Scenario, Supplier, Cost_USD
        
        # Add Scenario Label to DataFrames
        if not df_a.empty: df_a['Scenario'] = name_a
        if not df_b.empty: df_b['Scenario'] = name_b
        
        # Combine
        df_chart = pd.concat([df_a, df_b], ignore_index=True)
        
        # Convert to USD for Charting
        df_chart['Cost USD'] = df_chart['Total Cost (€)'] * usd_rate
        
        # Group by Scenario and Supplier to handle multiple lines of same supplier
        df_chart_grouped = df_chart.groupby(['Scenario', 'Supplier'])['Cost USD'].sum().reset_index()

        # Create Stacked Bar Chart
        chart = (
            alt.Chart(df_chart_grouped)
            .mark_bar()
            .encode(
                x=alt.X('Scenario', axis=None),
                y=alt.Y('Cost USD', axis=alt.Axis(format='$,.0f', title='Total Spend')),
                color=alt.Color('Supplier', scale=alt.Scale(scheme='tableau10')),
                tooltip=['Scenario', 'Supplier', alt.Tooltip('Cost USD', format='$,.0f')]
            )
            .properties(height=400)
            .configure_axis(grid=False)
            .configure_view(strokeWidth=0)
        )
        
        st.altair_chart(chart, use_container_width=True)

    # 4. Data Table & Clipboard
    st.divider()
    st.write("### 📋 Breakdown & Export")
    
    if not df_a.empty or not df_b.empty:
        df_combined = pd.concat([df_a, df_b], ignore_index=True)
        
        df_display = df_combined.copy()
        df_display['Total Cost ($)'] = (df_display['Total Cost (€)'] * usd_rate)
        
        cols = ['Scenario', 'Workflow', 'Supplier', 'Demand', 'Total Cost ($)', 'Lon OA', 'War OA', 'Dub OA', 'Bir OA']
        df_export = df_display[cols]
        
        st.dataframe(df_export.style.format({'Total Cost ($)': "${:,.0f}"}), use_container_width=True)
        
        st.write("#### ✂️ Copy to Google Sheets")
        st.caption("Click inside, Press Ctrl+A, then Ctrl+C. Paste into cell A1 of your Sheet.")
        
        tsv = df_export.to_csv(sep='\t', index=False)
        st.text_area("Clipboard Data", tsv, height=150)
        
    else:
        st.info("👈 Use the toggle in the sidebar to add items to Scenario A or B.")

    # 5. Clear Buttons
    st.divider()
    c_clear1, c_clear2 = st.columns(2)
    with c_clear1:
        if st.button(f"🗑️ Clear {name_a}"):
            st.session_state.scenario_a = []
            st.rerun()
    with c_clear2:
        if st.button(f"🗑️ Clear {name_b}"):
            st.session_state.scenario_b = []
            st.rerun()
