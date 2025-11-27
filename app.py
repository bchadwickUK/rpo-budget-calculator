import streamlit as st
import pandas as pd

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="Master RPO Budget Modeler", layout="wide")

# --- PASSWORD PROTECTION ---
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.title("🔒 Restricted Access")
    st.markdown("This tool is for authorized budget planning only.")
    password = st.text_input("Enter Access Code:", type="password")
    if st.button("Login"):
        if password == "1963":
            st.session_state.logged_in = True
            st.rerun()
        else:
            st.error("Incorrect Access Code.")
    st.stop()

# --- DATA & SESSION SETUP ---
if 'budget_lines' not in st.session_state:
    st.session_state.budget_lines = []

# NEW: Initialize Scenario Storage
if 'scenarios' not in st.session_state:
    st.session_state.scenarios = {}

# 1. WORKFLOW MAPPING (Your Selection List)
workflow_data = {
    'Workflow Name': [
        'SWE - RSR', 'SWE - KF', 'SWE - CIELO',
        'SRE - RSR', 'SRE - KF', 'SRE - CIELO',
        'TPgM - RSR', 'TPgM - KF', 'TPgM - CIELO',
        'GBOFx - RSR', 'GBOFx - KF', 'GBOFx - CIELO'
    ],
    'Supplier': [
        'RSR', 'KF', 'Cielo',
        'RSR', 'KF', 'Cielo',
        'RSR', 'KF', 'Cielo',
        'RSR', 'KF', 'Cielo'
    ],
    'Pricing Tier': [
        'T6', 'T6', 'T6',
        'T6', 'T6', 'T6',
        'T6', 'T6', 'T6',
        'T4', 'T4', 'T4'
    ],
    'Avg PPR': [6, 6, 6, 6.5, 6.5, 6.5, 6, 6, 6, 9, 9, 9]
}
df_workflows = pd.DataFrame(workflow_data)

# 2. FULL PRICING DATA (Master Library)
pricing_data = [
    # CIELO
    {'Supplier': 'Cielo', 'Tier': 'T1', 'Cost_Type': 'High Cost', 'Price': 2485},
    {'Supplier': 'Cielo', 'Tier': 'T2', 'Cost_Type': 'High Cost', 'Price': 2835},
    {'Supplier': 'Cielo', 'Tier': 'T3', 'Cost_Type': 'High Cost', 'Price': 3595},
    {'Supplier': 'Cielo', 'Tier': 'T4', 'Cost_Type': 'High Cost', 'Price': 4290},
    {'Supplier': 'Cielo', 'Tier': 'T5', 'Cost_Type': 'High Cost', 'Price': 4688},
    {'Supplier': 'Cielo', 'Tier': 'T6', 'Cost_Type': 'High Cost', 'Price': 5939},
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
    # RSR
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
    # KF
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
    row = df_pricing[
        (df_pricing['Supplier'] == supplier) & 
        (df_pricing['Tier'] == tier) & 
        (df_pricing['Cost_Type'] == cost_type)
    ]
    if not row.empty:
        return row.iloc[0]['Price']
    return 0

# --- SIDEBAR: INPUT & SCENARIO MANAGER ---
with st.sidebar:
    st.header("1. Add Workflow")
    
    # Workflow Inputs
    selected_workflow = st.selectbox("Select Workflow:", df_workflows['Workflow Name'].unique())
    wf_details = df_workflows[df_workflows['Workflow Name'] == selected_workflow].iloc[0]
    curr_supplier = wf_details['Supplier']
    curr_tier = wf_details['Pricing Tier']
    curr_ppr = wf_details['Avg PPR']
    
    st.info(f"**Supplier:** {curr_supplier} | **Tier:** {curr_tier} | **PPR:** {curr_ppr}")
    total_demand = st.number_input("Total Hires Needed (Demand):", min_value=1, value=10)
    
    st.subheader("Location Split (%)")
    high_pct = st.number_input("High Cost % (e.g. London):", 0, 100, 50)
    med_pct = 0
    if curr_supplier in ['RSR', 'Cielo']:
        med_pct = st.number_input("Medium Cost % (e.g. Dublin):", 0, 100, 0)
    else:
        st.caption("Medium Cost not applicable for KF")
    med_low_pct = 0
    if curr_supplier == 'RSR':
        med_low_pct = st.number_input("Med/Low Cost % (RSR Only):", 0, 100, 0)
    low_pct = st.number_input("Low Cost % (e.g. Warsaw):", 0, 100, 50)
    
    total_split = high_pct + med_pct + med_low_pct + low_pct
    
    if total_split != 100:
        st.error(f"Total Split is {total_split}%. Must equal 100%.")
        btn_disabled = True
    else:
        btn_disabled = False

    if st.button("Add to Model", disabled=btn_disabled):
        vol_high = total_demand * (high_pct/100)
        vol_med = total_demand * (med_pct/100)
        vol_med_low = total_demand * (med_low_pct/100)
        vol_low = total_demand * (low_pct/100)
        
        price_high = get_price(curr_supplier, curr_tier, 'High Cost')
        price_med = get_price(curr_supplier, curr_tier, 'Medium Cost')
        price_med_low = get_price(curr_supplier, curr_tier, 'Medium/Low Cost')
        price_low = get_price(curr_supplier, curr_tier, 'Low Cost')
        
        total_cost = (
            (vol_high * price_high) +
            (vol_med * price_med) +
            (vol_med_low * price_med_low) +
            (vol_low * price_low)
        )
        recruiters_needed = total_demand / curr_ppr
        
        st.session_state.budget_lines.append({
            "Workflow": selected_workflow,
            "Supplier": curr_supplier,
            "Demand": total_demand,
            "High Cost %": f"{high_pct}%",
            "Low Cost %": f"{low_pct}%",
            "Total Cost (€)": total_cost,
            "Recruiters": recruiters_needed
        })
        st.success("Added!")

    # --- NEW: SCENARIO MANAGER SIDEBAR ---
    st.markdown("---")
    st.header("💾 Scenario Manager")
    st.markdown("Save your current model to compare it with others later.")
    
    scenario_name = st.text_input("Name this Scenario (e.g. 'Option A'):")
    
    if st.button("Save Snapshot"):
        if len(st.session_state.budget_lines) > 0 and scenario_name:
            # Save a copy of the list
            st.session_state.scenarios[scenario_name] = list(st.session_state.budget_lines)
            st.success(f"Saved '{scenario_name}'!")
        else:
            st.warning("Create a budget and name it first.")

    if st.button("Clear Current Model"):
        st.session_state.budget_lines = []
        st.rerun()

# --- MAIN PAGE DISPLAY ---

st.title("📊 Master RPO Budget Modeler")
st.markdown("Add workflows to build your budget. Save scenarios to compare strategies.")
st.markdown("---")

# USD Rate
usd_rate = 1.15

if len(st.session_state.budget_lines) > 0:
    # Convert list to DataFrame
    df_results = pd.DataFrame(st.session_state.budget_lines)
    
    # CALCULATIONS
    total_eur = df_results['Total Cost (€)'].sum()
    total_usd = total_eur * usd_rate
    total_headcount = df_results['Recruiters'].sum()
    total_volume = df_results['Demand'].sum()

    # METRICS
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Project Cost (€)", f"€{total_eur:,.0f}")
    c2.metric("Total Project Cost ($)", f"${total_usd:,.0f}")
    c3.metric("Total Hires", f"{total_volume}")
    c4.metric("Recruiters Required", f"{total_headcount:.1f}")
    
    st.markdown("---")

    # DETAILED TABLE
    st.subheader("Current Model Breakdown")
    
    df_display = df_results.copy()
    df_display['Total Cost ($)'] = df_display['Total Cost (€)'] * usd_rate
    df_display['Total Cost (€)'] = df_display['Total Cost (€)'].apply(lambda x: f"€{x:,.0f}")
    df_display['Total Cost ($)'] = df_display['Total Cost ($)'].apply(lambda x: f"${x:,.0f}")
    df_display['Recruiters'] = df_display['Recruiters'].apply(lambda x: f"{x:.1f}")
    
    column_order = [
        "Workflow", "Supplier", "Demand", 
        "High Cost %", "Low Cost %", 
        "Total Cost (€)", "Total Cost ($)", 
        "Recruiters"
    ]
    st.dataframe(df_display[column_order], use_container_width=True)
    
    # Remove Functionality
    st.write("### Manage Rows")
    c_rem1, c_rem2 = st.columns([3, 1])
    with c_rem1:
        options = [f"{i}. {row['Workflow']} (Demand: {row['Demand']})" for i, row in enumerate(st.session_state.budget_lines)]
        selected_to_remove = st.multiselect("Select lines to remove:", options)
    with c_rem2:
        st.write("")
        st.write("") 
        if st.button("Remove Selected"):
            if selected_to_remove:
                indices = [int(s.split('.')[0]) for s in selected_to_remove]
                st.session_state.budget_lines = [r for i, r in enumerate(st.session_state.budget_lines) if i not in indices]
                st.rerun()

    # Download
    csv = df_results.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Download Current View to CSV", csv, "budget_current.csv", "text/csv")

else:
    st.info("👈 Use the sidebar to add your first workflow.")

# --- COMPARISON ENGINE ---
st.markdown("---")

if len(st.session_state.scenarios) > 0:
    st.header("⚔️ Scenario Comparison")
    
    # Prepare comparison data
    comp_data = []
    
    # Add Saved Scenarios
    for name, lines in st.session_state.scenarios.items():
        df_temp = pd.DataFrame(lines)
        cost = df_temp['Total Cost (€)'].sum()
        recs = df_temp['Recruiters'].sum()
        comp_data.append({'Scenario': name, 'Cost (€)': cost, 'Recruiters': recs})
    
    # Add Current Model (if exists)
    if len(st.session_state.budget_lines) > 0:
        current_cost = pd.DataFrame(st.session_state.budget_lines)['Total Cost (€)'].sum()
        current_recs = pd.DataFrame(st.session_state.budget_lines)['Recruiters'].sum()
        comp_data.append({'Scenario': 'Current Draft', 'Cost (€)': current_cost, 'Recruiters': current_recs})
    
    df_comp = pd.DataFrame(comp_data)
    
    # Show Comparison Metrics
    col_chart, col_data = st.columns([2, 1])
    
    with col_chart:
        st.subheader("Cost Comparison")
        st.bar_chart(df_comp, x='Scenario', y='Cost (€)', color="#34A853")
        
    with col_data:
        st.subheader("Data Comparison")
        df_comp['Cost ($)'] = (df_comp['Cost (€)'] * usd_rate).apply(lambda x: f"${x:,.0f}")
        df_comp['Cost (€)'] = df_comp['Cost (€)'].apply(lambda x: f"€{x:,.0f}")
        df_comp['Recruiters'] = df_comp['Recruiters'].apply(lambda x: f"{x:.1f}")
        st.dataframe(df_comp[['Scenario', 'Cost (€)', 'Cost ($)', 'Recruiters']], hide_index=True)
        
    if st.button("🗑️ Clear All Saved Scenarios"):
        st.session_state.scenarios = {}
        st.rerun()
