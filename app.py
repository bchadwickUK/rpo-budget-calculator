import streamlit as st
import pandas as pd

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="RPO Strategy Engine", 
    layout="wide", 
    page_icon="📊"
)

# --- CUSTOM CSS (SAFE MODE) ---
# Minimal styling to ensure Dark/Light mode compatibility while keeping Google colors
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Roboto', sans-serif;
    }
    
    /* Primary Buttons (Google Blue) */
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
        font-size: 2rem !important;
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
if 'scenarios' not in st.session_state:
    st.session_state.scenarios = {}

# 1. WORKFLOW DATA
workflow_data = {
    'Role': [
        'SWE', 'SWE', 'SWE',
        'SRE', 'SRE', 'SRE',
        'TPgM', 'TPgM', 'TPgM',
        'GBOFx', 'GBOFx', 'GBOFx'
    ],
    'Supplier': ['RSR', 'KF', 'Cielo'] * 4,
    'Pricing Tier': ['T6', 'T6', 'T6'] * 3 + ['T4', 'T4', 'T4'],
    'Avg PPR': [6, 6, 6, 6.5, 6.5, 6.5, 6, 6, 6, 9, 9, 9]
}
df_workflows = pd.DataFrame(workflow_data)
# Helper column for backend logic
df_workflows['Workflow Name'] = df_workflows['Role'] + " - " + df_workflows['Supplier']

# 2. PRICING DATA
pricing_data = [
    {'Supplier': 'Cielo', 'Tier': 'T1', 'Cost_Type': 'High Cost', 'Price': 2485},
    {'Supplier': 'Cielo', 'Tier': 'T2', 'Cost_Type': 'High Cost', 'Price': 2835},
    {'Supplier': 'Cielo', 'Tier': 'T3', 'Cost_Type': 'High Cost', 'Price': 3595},
    {'Supplier': 'Cielo', 'Tier': 'T4', 'Cost_Type': 'High Cost', 'Price': 4290},
    {'Supplier': 'Cielo', 'Tier': 'T5', 'Cost_Type': 'High Cost', 'Price': 4688},
    {'Supplier': 'Cielo', 'Tier': 'T6', 'Cost_Type': 'High Cost', 'Price': 5938},
    {'Supplier': 'Cielo', 'Tier': 'T7', 'Cost_Type': 'High Cost', 'Price': 7538},
    {'Supplier': 'Cielo', 'Tier': 'T1', 'Cost_Type': 'Medium Cost', 'Price': 2207},
    {'Supplier': 'Cielo', 'Tier': 'T2', 'Cost_Type': 'Medium Cost', 'Price': 2527},
    {'Supplier': 'Cielo', 'Tier': 'T3', 'Cost_Type': 'Medium Cost', 'Price': 3217},
    {'Supplier': 'Cielo', 'Tier': 'T4', 'Cost_Type': 'Medium Cost', 'Price': 3857},
    {'Supplier': 'Cielo', 'Tier': 'T5', 'Cost_Type': 'Medium Cost', 'Price': 4204},
    {'Supplier': 'Cielo', 'Tier': 'T6', 'Cost_Type': 'Medium Cost', 'Price': 5343},
    {'Supplier': 'Cielo', 'Tier': 'T7', 'Cost_Type': 'Medium Cost', 'Price': 6793},
    {'Supplier': 'Cielo', 'Tier': 'T1', 'Cost_Type': 'Low Cost', 'Price': 1637},
    {'Supplier': 'Cielo', 'Tier': 'T2', 'Cost_Type': 'Low Cost', 'Price': 1867},
    {'Supplier': 'Cielo', 'Tier': 'T3', 'Cost_Type': 'Low Cost', 'Price': 2367},
    {'Supplier': 'Cielo', 'Tier': 'T4', 'Cost_Type': 'Low Cost', 'Price': 2817},
    {'Supplier': 'Cielo', 'Tier': 'T5', 'Cost_Type': 'Low Cost', 'Price': 3089},
    {'Supplier': 'Cielo', 'Tier': 'T6', 'Cost_Type': 'Low Cost', 'Price': 3899},
    {'Supplier': 'Cielo', 'Tier': 'T7', 'Cost_Type': 'Low Cost', 'Price': 4939},
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
    # This determines the entire state of the app
    mode = st.radio(
        "Select Mode:",
        ["📝 Budget Builder", "⚖️ Comparison"],
        index=0,
        label_visibility="collapsed"
    )
    
    st.divider()

    # --- SCENARIO SELECTOR (ONLY FOR COMPARISON MODE) ---
    target_bucket = "Current Draft" # Default
    
    if mode == "⚖️ Comparison":
        st.write("### 🏗️ Scenario Setup")
        
        # Scenario Selector
        existing_scenarios = list(st.session_state.scenarios.keys())
        scenario_options = ["+ Create New Scenario"] + existing_scenarios
        selected_scenario_option = st.selectbox("Select Target Scenario:", scenario_options)
        
        if selected_scenario_option == "+ Create New Scenario":
            new_scenario_name = st.text_input("Name New Scenario:", placeholder="e.g. Option B - Low Cost")
            if new_scenario_name:
                target_bucket = new_scenario_name
                # Initialize if not exists
                if target_bucket not in st.session_state.scenarios:
                    st.session_state.scenarios[target_bucket] = []
            else:
                target_bucket = None # Block adding until named
        else:
            target_bucket = selected_scenario_option

    # --- INPUT FORM (COMMON FOR BOTH MODES) ---
    st.write("### ⚙️ Configure Workflow")
    
    # Cascading Dropdowns
    unique_roles = df_workflows['Role'].unique()
    selected_role = st.selectbox("1. Role", unique_roles)
    
    available_suppliers = df_workflows[df_workflows['Role'] == selected_role]['Supplier'].unique()
    selected_supplier = st.selectbox("2. Supplier", available_suppliers)
    
    # Get Workflow Details
    wf_details = df_workflows[
        (df_workflows['Role'] == selected_role) & 
        (df_workflows['Supplier'] == selected_supplier)
    ].iloc[0]
    
    curr_supplier = wf_details['Supplier']
    wf_name_backend = wf_details['Workflow Name']

    # Efficiency Settings
    with st.expander("🛠️ Efficiency / PPR"):
        efficiency_mode = st.checkbox("Override Defaults", value=False)
        if efficiency_mode:
            st.info(f"Modifying {curr_supplier}")
            calc_ppr = st.number_input("Target PPR:", value=float(wf_details['Avg PPR']), step=0.5)
            calc_tier = st.selectbox("New Tier:", ['T1','T2','T3','T4','T5','T6','T7'], index=['T1','T2','T3','T4','T5','T6','T7'].index(wf_details['Pricing Tier']))
        else:
            calc_ppr = wf_details['Avg PPR']
            calc_tier = wf_details['Pricing Tier']

    # Volume & Locations
    total_demand = st.number_input("Demand Volume", min_value=1, value=50)
    
    st.caption("LOCATION SPLIT (%)")
    lon_pct = st.number_input("London %", 0, 100, 50)
    war_pct = st.number_input("Warsaw %", 0, 100, 50)
    
    dub_pct = st.number_input("Dublin %", 0, 100, 0)
    
    bir_pct = 0
    if curr_supplier == 'RSR': 
        bir_pct = st.number_input("Birmingham %", 0, 100, 0)
    
    total_split = lon_pct + war_pct + dub_pct + bir_pct
    
    # ADD BUTTON LOGIC
    if total_split != 100:
        st.error(f"Total: {total_split}%")
        btn_disabled = True
    elif mode == "⚖️ Comparison" and not target_bucket:
        st.warning("Name your scenario above.")
        btn_disabled = True
    else:
        btn_disabled = False

    # Dynamic Button Text
    if mode == "⚖️ Comparison":
        btn_text = f"Add to '{target_bucket}'"
    else:
        btn_text = "Add to Budget"

    if st.button(btn_text, disabled=btn_disabled, use_container_width=True):
        # 1. CALCULATE COST
        vol_lon = total_demand * (lon_pct/100)
        vol_war = total_demand * (war_pct/100)
        vol_dub = total_demand * (dub_pct/100)
        vol_bir = total_demand * (bir_pct/100)
        
        price_lon = get_price(curr_supplier, calc_tier, 'High Cost')
        price_war = get_price(curr_supplier, calc_tier, 'Low Cost')
        price_bir = get_price(curr_supplier, calc_tier, 'Medium/Low Cost')
        
        # Smart Dublin Logic
        if curr_supplier == 'KF': price_dub = get_price(curr_supplier, calc_tier, 'High Cost')
        else: price_dub = get_price(curr_supplier, calc_tier, 'Medium Cost')

        total_cost = (vol_lon * price_lon) + (vol_war * price_war) + (vol_dub * price_dub) + (vol_bir * price_bir)
        recruiters_needed = total_demand / calc_ppr
        
        wf_display_name = wf_name_backend
        if efficiency_mode: wf_display_name += f" (Eff: {calc_tier})"

        # 2. CREATE DATA OBJECT
        new_line = {
            "Workflow": wf_display_name,
            "Supplier": curr_supplier,
            "Demand": total_demand,
            "Tier": calc_tier,
            "Total Cost (€)": total_cost,
            "Recruiters": recruiters_needed,
            "Lon OA": vol_lon,
            "War OA": vol_war,
            "Dub OA": vol_dub,
            "Bir OA": vol_bir
        }

        # 3. ROUTE TO CORRECT BUCKET
        if mode == "📝 Budget Builder":
            st.session_state.budget_lines.append(new_line)
            st.toast("Added to Budget!")
        else:
            # Comparison Mode
            st.session_state.scenarios[target_bucket].append(new_line)
            st.toast(f"Added to {target_bucket}!")

# --- MAIN PAGE LOGIC ---
st.title("RPO Architect")
usd_rate = 1.15

# --- MODE 1: BUILDER VIEW ---
if mode == "📝 Budget Builder":
    st.subheader("📝 Single Budget Builder")
    
    if len(st.session_state.budget_lines) > 0:
        df_results = pd.DataFrame(st.session_state.budget_lines)
        
        # Calcs
        total_eur = df_results['Total Cost (€)'].sum()
        total_usd = total_eur * usd_rate
        total_hc = df_results['Recruiters'].sum()
        total_vol = df_results['Demand'].sum()
        avg_cpoa = total_usd / total_vol if total_vol > 0 else 0
        
        # Metrics
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Forecast (USD)", f"${total_usd:,.0f}")
        c2.metric("Forecast (EUR)", f"€{total_eur:,.0f}")
        c3.metric("Avg CPOA", f"${avg_cpoa:,.0f}")
        c4.metric("Headcount", f"{total_hc:.1f}")
        
        st.divider()
        
        # Table
        df_display = df_results.copy()
        df_display['CPOA ($)'] = (df_display['Total Cost (€)'] * usd_rate) / df_display['Demand']
        df_display['Total Cost ($)'] = (df_display['Total Cost (€)'] * usd_rate).apply(lambda x: f"${x:,.0f}")
        df_display['Total Cost (€)'] = df_display['Total Cost (€)'].apply(lambda x: f"€{x:,.0f}")
        df_display['CPOA ($)'] = df_display['CPOA ($)'].apply(lambda x: f"${x:,.0f}")
        df_display['Recruiters'] = df_display['Recruiters'].apply(lambda x: f"{x:.1f}")
        
        # Format Location OA Columns
        for col in ["Lon OA", "War OA", "Dub OA", "Bir OA"]:
            df_display[col] = df_display[col].apply(lambda x: f"{x:.1f}")

        st.dataframe(
            df_display[["Workflow", "Supplier", "Demand", "Lon OA", "War OA", "Dub OA", "Bir OA", "CPOA ($)", "Total Cost ($)", "Recruiters"]], 
            use_container_width=True
        )
        
        # --- NEW MANAGEMENT SECTION ---
        st.divider()
        st.write("### 🛠️ Manage Data")
        
        c_m1, c_m2, c_m3 = st.columns(3)
        
        with c_m1:
            # CSV Download
            csv = df_results.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Download CSV",
                data=csv,
                file_name="rpo_budget_draft.csv",
                mime="text/csv",
                use_container_width=True
            )
            
        with c_m2:
            # Row Deletion
            # Create friendly labels: "1. SWE - RSR (50 roles)"
            del_options = [f"{i+1}. {row['Workflow']} ({row['Demand']})" for i, row in enumerate(st.session_state.budget_lines)]
            selected_del = st.selectbox("Select line to remove", del_options, label_visibility="collapsed")
            
            if st.button("🗑️ Remove Line", use_container_width=True):
                if selected_del:
                    # Extract index from string "1. ..." -> 0
                    idx_to_del = int(selected_del.split(".")[0]) - 1
                    st.session_state.budget_lines.pop(idx_to_del)
                    st.rerun()

        with c_m3:
             if st.button("💥 Clear All", type="primary", use_container_width=True):
                st.session_state.budget_lines = []
                st.rerun()

    else:
        st.info("👈 Select inputs in the sidebar and click **'Add to Budget'**.")

# --- MODE 2: COMPARISON VIEW ---
elif mode == "⚖️ Comparison":
    st.subheader("⚖️ Strategy Comparison")
    
    if len(st.session_state.scenarios) > 0:
        # Prepare Data
        comp_data = []
        for name, lines in st.session_state.scenarios.items():
            if lines:
                df_temp = pd.DataFrame(lines)
                cost_eur = df_temp['Total Cost (€)'].sum()
                cost_usd = cost_eur * usd_rate
                hc = df_temp['Recruiters'].sum()
                vol = df_temp['Demand'].sum()
                cpoa = cost_usd / vol if vol > 0 else 0
                
                comp_data.append({
                    'Scenario': name, 
                    'Cost ($)': cost_usd,
                    'Cost (€)': cost_eur, 
                    'Recruiters': hc,
                    'CPOA ($)': cpoa
                })
        
        if comp_data:
            df_comp = pd.DataFrame(comp_data)
            
            # 1. Executive Summary
            if len(df_comp) >= 2:
                base = df_comp.iloc[0]
                prop = df_comp.iloc[-1]
                diff = prop['Cost ($)'] - base['Cost ($)']
                
                st.write(f"### 🔎 Insight")
                if diff < 0:
                    st.success(f"**{prop['Scenario']}** saves **${abs(diff):,.0f}** vs **{base['Scenario']}**.")
                elif diff > 0:
                    st.warning(f"**{prop['Scenario']}** costs **${abs(diff):,.0f}** more than **{base['Scenario']}**.")
                else:
                    st.info("Costs are identical.")

            # 2. Charts
            c_chart1, c_chart2 = st.columns(2)
            with c_chart1:
                st.caption("Total Spend (USD)")
                st.bar_chart(df_comp, x='Scenario', y='Cost ($)', color="#4285F4")
            with c_chart2:
                st.caption("Headcount Required")
                st.bar_chart(df_comp, x='Scenario', y='Recruiters', color="#DB4437")

            # 3. Table
            st.divider()
            st.write("### Data Breakdown")
            df_comp['Cost ($)'] = df_comp['Cost ($)'].apply(lambda x: f"${x:,.0f}")
            df_comp['CPOA ($)'] = df_comp['CPOA ($)'].apply(lambda x: f"${x:,.0f}")
            df_comp['Recruiters'] = df_comp['Recruiters'].apply(lambda x: f"{x:.1f}")
            
            st.dataframe(df_comp[['Scenario', 'Cost ($)', 'CPOA ($)', 'Recruiters']], use_container_width=True)

            # Manage Scenarios
            with st.expander("Manage Scenarios"):
                c_del1, c_del2 = st.columns(2)
                
                with c_del1:
                    to_delete = st.selectbox("Delete a Scenario:", ["None"] + list(st.session_state.scenarios.keys()))
                    if st.button("Delete Selected"):
                        if to_delete != "None":
                            del st.session_state.scenarios[to_delete]
                            st.rerun()
                
                with c_del2:
                    st.write("") # Spacer for alignment
                    st.write("")
                    if st.button("🗑️ Delete ALL Scenarios", type="primary"):
                        st.session_state.scenarios = {}
                        st.rerun()
        else:
             st.info("Scenarios created, but they are empty. Add items using the sidebar.")
    else:
        st.info("👈 Select **'+ Create New Scenario'** in the sidebar to start.")
    
