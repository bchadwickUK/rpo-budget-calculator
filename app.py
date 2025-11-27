import streamlit as st
import pandas as pd

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

    /* Metric Cards styling */
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
# Create the full name automatically to keep the rest of the app working
df_workflows['Workflow Name'] = df_workflows['Role'] + " - " + df_workflows['Supplier']

# 2. PRICING DATA
pricing_data = [
    {'Supplier': 'Cielo', 'Tier': 'T1', 'Cost_Type': 'High Cost', 'Price': 2485, 'PPR_Ref': '16+'},
    {'Supplier': 'Cielo', 'Tier': 'T2', 'Cost_Type': 'High Cost', 'Price': 2835, 'PPR_Ref': '13-16'},
    {'Supplier': 'Cielo', 'Tier': 'T3', 'Cost_Type': 'High Cost', 'Price': 3595, 'PPR_Ref': '10-12'},
    {'Supplier': 'Cielo', 'Tier': 'T4', 'Cost_Type': 'High Cost', 'Price': 4290, 'PPR_Ref': '<=9'},
    {'Supplier': 'Cielo', 'Tier': 'T5', 'Cost_Type': 'High Cost', 'Price': 4688, 'PPR_Ref': '8+'},
    {'Supplier': 'Cielo', 'Tier': 'T6', 'Cost_Type': 'High Cost', 'Price': 5939, 'PPR_Ref': '6-7'},
    {'Supplier': 'Cielo', 'Tier': 'T7', 'Cost_Type': 'High Cost', 'Price': 7538, 'PPR_Ref': '<=5'},
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
    {'Supplier': 'RSR', 'Tier': 'T1', 'Cost_Type': 'High Cost', 'Price': 3359, 'PPR_Ref': '16+'},
    {'Supplier': 'RSR', 'Tier': 'T2', 'Cost_Type': 'High Cost', 'Price': 4079, 'PPR_Ref': '13-16'},
    {'Supplier': 'RSR', 'Tier': 'T3', 'Cost_Type': 'High Cost', 'Price': 5191, 'PPR_Ref': '10-12'},
    {'Supplier': 'RSR', 'Tier': 'T4', 'Cost_Type': 'High Cost', 'Price': 7138, 'PPR_Ref': '<=9'},
    {'Supplier': 'RSR', 'Tier': 'T5', 'Cost_Type': 'High Cost', 'Price': 6638, 'PPR_Ref': '8+'},
    {'Supplier': 'RSR', 'Tier': 'T6', 'Cost_Type': 'High Cost', 'Price': 9482, 'PPR_Ref': '6-7'},
    {'Supplier': 'RSR', 'Tier': 'T7', 'Cost_Type': 'High Cost', 'Price': 13276,'PPR_Ref': '<=5'},
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
    {'Supplier': 'KF', 'Tier': 'T1', 'Cost_Type': 'High Cost', 'Price': 2664, 'PPR_Ref': '16+'},
    {'Supplier': 'KF', 'Tier': 'T2', 'Cost_Type': 'High Cost', 'Price': 3185, 'PPR_Ref': '13-16'},
    {'Supplier': 'KF', 'Tier': 'T3', 'Cost_Type': 'High Cost', 'Price': 4125, 'PPR_Ref': '10-12'},
    {'Supplier': 'KF', 'Tier': 'T4', 'Cost_Type': 'High Cost', 'Price': 5558, 'PPR_Ref': '<=9'},
    {'Supplier': 'KF', 'Tier': 'T5', 'Cost_Type': 'High Cost', 'Price': 5020, 'PPR_Ref': '8+'},
    {'Supplier': 'KF', 'Tier': 'T6', 'Cost_Type': 'High Cost', 'Price': 7171, 'PPR_Ref': '6-7'},
    {'Supplier': 'KF', 'Tier': 'T7', 'Cost_Type': 'High Cost', 'Price': 10040,'PPR_Ref': '<=5'},
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
    # Google Logo (PNG)
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/c/c1/Google_%22G%22_logo.svg/480px-Google_%22G%22_logo.svg.png", width=40)
    st.markdown("### Strategy Engine")
    st.markdown("---")
    
    # Workflow Inputs
    st.caption("CONFIGURATION")
    
    # 1. SELECT ROLE
    unique_roles = df_workflows['Role'].unique()
    selected_role = st.selectbox("1. Select Role / Job Family", unique_roles)
    
    # 2. SELECT SUPPLIER (Filtered by Role)
    # We only show suppliers that actually handle the selected role
    available_suppliers = df_workflows[df_workflows['Role'] == selected_role]['Supplier'].unique()
    selected_supplier = st.selectbox("2. Select Supplier", available_suppliers)
    
    # RECONSTRUCT THE WORKFLOW OBJECT
    # The rest of your app expects a single row of data, so we find it here
    wf_details = df_workflows[
        (df_workflows['Role'] == selected_role) & 
        (df_workflows['Supplier'] == selected_supplier)
    ].iloc[0]
    
    selected_workflow = wf_details['Workflow Name']
    curr_supplier = wf_details['Supplier']
    
    # ... (The rest of your code: Efficiency Toggle, Demand, etc. continues here) ...
    
    # Efficiency Toggle
    with st.expander("🛠️  Efficiency / PPR Settings"):
        efficiency_mode = st.checkbox("Enable Efficiency Override", value=False)
        if efficiency_mode:
            st.info(f"Modifying {curr_supplier}")
            calc_ppr = st.number_input("Target PPR:", value=float(wf_details['Avg PPR']), step=0.5)
            calc_tier = st.selectbox("New Tier:", ['T1','T2','T3','T4','T5','T6','T7'], index=['T1','T2','T3','T4','T5','T6','T7'].index(wf_details['Pricing Tier']))
        else:
            calc_ppr = wf_details['Avg PPR']
            calc_tier = wf_details['Pricing Tier']

    total_demand = st.number_input("Demand Volume", min_value=1, value=50)
    
    # --- LOCATION SPLIT (BY CITY NAME) ---
    st.markdown("---")
    st.caption("LOCATION STRATEGY (%)")
    
    # 1. London (Always High Cost)
    lon_pct = st.number_input("London %", 0, 100, 50)
    
    # 2. Warsaw (Always Low Cost)
    war_pct = st.number_input("Warsaw %", 0, 100, 50)
    
    # 3. Dublin (The Variable One)
    dub_pct = st.number_input("Dublin %", 0, 100, 0)
    
    # 4. Birmingham (RSR Only)
    bir_pct = 0
    if curr_supplier == 'RSR': 
        bir_pct = st.number_input("Birmingham %", 0, 100, 0)
    
    total_split = lon_pct + war_pct + dub_pct + bir_pct
    
    if total_split != 100:
        st.error(f"Total: {total_split}%")
        btn_disabled = True
    else:
        st.success("Split: 100%")
        btn_disabled = False

    st.write("")
    if st.button("Add to Model", disabled=btn_disabled, use_container_width=True):
        # VOLUME CALCS
        vol_lon = total_demand * (lon_pct/100)
        vol_war = total_demand * (war_pct/100)
        vol_dub = total_demand * (dub_pct/100)
        vol_bir = total_demand * (bir_pct/100)
        
        # PRICE MAPPING LOGIC
        price_lon = get_price(curr_supplier, calc_tier, 'High Cost')
        price_war = get_price(curr_supplier, calc_tier, 'Low Cost')
        price_bir = get_price(curr_supplier, calc_tier, 'Medium/Low Cost')
        
        # DUBLIN LOGIC SWITCH
        if curr_supplier == 'KF':
            price_dub = get_price(curr_supplier, calc_tier, 'High Cost')
        else:
            price_dub = get_price(curr_supplier, calc_tier, 'Medium Cost')

        # TOTAL COST
        total_cost = (
            (vol_lon * price_lon) +
            (vol_war * price_war) +
            (vol_dub * price_dub) +
            (vol_bir * price_bir)
        )
        
        recruiters_needed = total_demand / calc_ppr
        
        wf_display_name = selected_workflow
        if efficiency_mode: wf_display_name += f" (Eff: {calc_tier})"

        st.session_state.budget_lines.append({
            "Workflow": wf_display_name,
            "Supplier": curr_supplier,
            "Demand": total_demand,
            "Tier": calc_tier,
            "Total Cost (€)": total_cost,
            "Recruiters": recruiters_needed
        })
        st.toast("Workflow Added!")

    # --- SCENARIO MANAGER ---
    st.markdown("---")
    st.caption("SCENARIO MANAGER")
    
    scenario_name = st.text_input("Name Scenario", placeholder="e.g. Option A")
    
    if st.button("💾 Save Snapshot", use_container_width=True):
        if len(st.session_state.budget_lines) > 0 and scenario_name:
            st.session_state.scenarios[scenario_name] = list(st.session_state.budget_lines)
            st.toast(f"Saved '{scenario_name}'!")
    
    st.write("")
    if st.button("🗑️ Clear Current", use_container_width=True):
        st.session_state.budget_lines = []
        st.rerun()

# --- MAIN PAGE ---
st.title("RPO Budget & Strategy Engine")
usd_rate = 1.15

tab_builder, tab_strategy = st.tabs(["Builder", "Comparison"])

# --- TAB 1: BUILDER ---
with tab_builder:
    if len(st.session_state.budget_lines) > 0:
        df_results = pd.DataFrame(st.session_state.budget_lines)
        
        # Calculations
        total_eur = df_results['Total Cost (€)'].sum()
        total_usd = total_eur * usd_rate
        total_hc = df_results['Recruiters'].sum()
        total_demand = df_results['Demand'].sum()
        
        # Calculate Average CPOA (Aggregated)
        if total_demand > 0:
            agg_cpoa = total_usd / total_demand
        else:
            agg_cpoa = 0
        
        # Google Material Card Look for Metrics
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Forecast (USD)", f"${total_usd:,.0f}")
        c2.metric("Forecast (EUR)", f"€{total_eur:,.0f}")
        c3.metric("Avg CPOA ($)", f"${agg_cpoa:,.0f}") # New Metric
        c4.metric("Headcount", f"{total_hc:.1f}")
        
        st.markdown("---")
        
        df_display = df_results.copy()
        
        # Calculate Row-Level CPOA
        df_display['CPOA ($)'] = (df_display['Total Cost (€)'] * usd_rate) / df_display['Demand']
        
        # Formatting
        df_display['Total Cost ($)'] = (df_display['Total Cost (€)'] * usd_rate).apply(lambda x: f"${x:,.0f}")
        df_display['Total Cost (€)'] = df_display['Total Cost (€)'].apply(lambda x: f"€{x:,.0f}")
        df_display['CPOA ($)'] = df_display['CPOA ($)'].apply(lambda x: f"${x:,.0f}")
        df_display['Recruiters'] = df_display['Recruiters'].apply(lambda x: f"{x:.1f}")
        
        st.dataframe(
            df_display[["Workflow", "Supplier", "Demand", "Tier", "CPOA ($)", "Total Cost ($)", "Recruiters"]], 
            use_container_width=True
        )
        
        with st.expander("Edit / Remove Items"):
            options = [f"{i}. {row['Workflow']}" for i, row in enumerate(st.session_state.budget_lines)]
            selected_to_remove = st.multiselect("Select lines to remove:", options)
            if st.button("Remove Selected"):
                if selected_to_remove:
                    indices = [int(s.split('.')[0]) for s in selected_to_remove]
                    st.session_state.budget_lines = [r for i, r in enumerate(st.session_state.budget_lines) if i not in indices]
                    st.rerun()
    else:
        st.info("👈 Use the sidebar to add your first workflow.")

# --- TAB 2: STRATEGY ---
with tab_strategy:
    if len(st.session_state.scenarios) > 0:
        
        comp_data = []
        for name, lines in st.session_state.scenarios.items():
            df_temp = pd.DataFrame(lines)
            comp_data.append({
                'Scenario': name, 
                'Cost (€)': df_temp['Total Cost (€)'].sum(), 
                'Recruiters': df_temp['Recruiters'].sum()
            })
            
        if len(st.session_state.budget_lines) > 0:
            curr_lines = st.session_state.budget_lines
            df_curr = pd.DataFrame(curr_lines)
            comp_data.append({
                'Scenario': 'Current Draft', 
                'Cost (€)': df_curr['Total Cost (€)'].sum(), 
                'Recruiters': df_curr['Recruiters'].sum()
            })
            
        df_comp = pd.DataFrame(comp_data)
        
        # EXECUTIVE SUMMARY
        if len(df_comp) >= 2:
            base = df_comp.iloc[0]
            prop = df_comp.iloc[-1]
            diff = prop['Cost (€)'] - base['Cost (€)']
            diff_usd = diff * usd_rate
            
            if diff < 0:
                st.success(f"**Insight:** **{prop['Scenario']}** is **${abs(diff_usd):,.0f}** cheaper than **{base['Scenario']}**.")
            elif diff > 0:
                st.warning(f"**Insight:** **{prop['Scenario']}** is **${abs(diff_usd):,.0f}** more expensive than **{base['Scenario']}**.")

        # SIDE BY SIDE CHARTS (GOOGLE COLORS)
        c_chart1, c_chart2 = st.columns(2)
        with c_chart1:
            st.caption("Spend Comparison (€)")
            st.bar_chart(df_comp, x='Scenario', y='Cost (€)', color="#4285F4")
        with c_chart2:
            st.caption("Headcount Comparison")
            st.bar_chart(df_comp, x='Scenario', y='Recruiters', color="#DB4437")

        st.markdown("---")
        st.subheader("Data Breakdown")
        df_comp['Cost ($)'] = (df_comp['Cost (€)'] * usd_rate).apply(lambda x: f"${x:,.0f}")
        df_comp['Cost (€)'] = df_comp['Cost (€)'].apply(lambda x: f"€{x:,.0f}")
        df_comp['Recruiters'] = df_comp['Recruiters'].apply(lambda x: f"{x:.1f}")
        st.dataframe(df_comp, use_container_width=True)
        
        if st.button("Clear All Scenarios"):
            st.session_state.scenarios = {}
            st.rerun()
            
    else:
        st.info("Save a scenario in the sidebar to view comparisons.")
