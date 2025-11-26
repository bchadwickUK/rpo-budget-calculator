import streamlit as st
import pandas as pd

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="Master RPO Budget Modeler", layout="wide")

# --- DATA LOADING (Based on your CSVs) ---
# In a production app, these could be loaded from external files or a database.

# 1. Workflow Mapping
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

# 2. FULL PRICING DATA (The Master Library)
# This includes T1-T7 for all vendors so you can switch tiers easily.
pricing_data = [
    # --- CIELO PRICES ---
    # London (High)
    {'Supplier': 'Cielo', 'Tier': 'T1', 'Cost_Type': 'High Cost', 'Price': 2485},
    {'Supplier': 'Cielo', 'Tier': 'T2', 'Cost_Type': 'High Cost', 'Price': 2835},
    {'Supplier': 'Cielo', 'Tier': 'T3', 'Cost_Type': 'High Cost', 'Price': 3595},
    {'Supplier': 'Cielo', 'Tier': 'T4', 'Cost_Type': 'High Cost', 'Price': 4290},
    {'Supplier': 'Cielo', 'Tier': 'T5', 'Cost_Type': 'High Cost', 'Price': 4688},
    {'Supplier': 'Cielo', 'Tier': 'T6', 'Cost_Type': 'High Cost', 'Price': 5939},
    {'Supplier': 'Cielo', 'Tier': 'T7', 'Cost_Type': 'High Cost', 'Price': 7538},
    # Dublin (Medium)
    {'Supplier': 'Cielo', 'Tier': 'T1', 'Cost_Type': 'Medium Cost', 'Price': 2207},
    {'Supplier': 'Cielo', 'Tier': 'T2', 'Cost_Type': 'Medium Cost', 'Price': 2527},
    {'Supplier': 'Cielo', 'Tier': 'T3', 'Cost_Type': 'Medium Cost', 'Price': 3217},
    {'Supplier': 'Cielo', 'Tier': 'T4', 'Cost_Type': 'Medium Cost', 'Price': 3857},
    {'Supplier': 'Cielo', 'Tier': 'T5', 'Cost_Type': 'Medium Cost', 'Price': 4204},
    {'Supplier': 'Cielo', 'Tier': 'T6', 'Cost_Type': 'Medium Cost', 'Price': 5343},
    {'Supplier': 'Cielo', 'Tier': 'T7', 'Cost_Type': 'Medium Cost', 'Price': 6793},
    # Warsaw (Low)
    {'Supplier': 'Cielo', 'Tier': 'T1', 'Cost_Type': 'Low Cost', 'Price': 1637},
    {'Supplier': 'Cielo', 'Tier': 'T2', 'Cost_Type': 'Low Cost', 'Price': 1867},
    {'Supplier': 'Cielo', 'Tier': 'T3', 'Cost_Type': 'Low Cost', 'Price': 2367},
    {'Supplier': 'Cielo', 'Tier': 'T4', 'Cost_Type': 'Low Cost', 'Price': 2817},
    {'Supplier': 'Cielo', 'Tier': 'T5', 'Cost_Type': 'Low Cost', 'Price': 3089},
    {'Supplier': 'Cielo', 'Tier': 'T6', 'Cost_Type': 'Low Cost', 'Price': 3899},
    {'Supplier': 'Cielo', 'Tier': 'T7', 'Cost_Type': 'Low Cost', 'Price': 4939},

    # --- RSR PRICES ---
    # London (High)
    {'Supplier': 'RSR', 'Tier': 'T1', 'Cost_Type': 'High Cost', 'Price': 3359},
    {'Supplier': 'RSR', 'Tier': 'T2', 'Cost_Type': 'High Cost', 'Price': 4079},
    {'Supplier': 'RSR', 'Tier': 'T3', 'Cost_Type': 'High Cost', 'Price': 5191},
    {'Supplier': 'RSR', 'Tier': 'T4', 'Cost_Type': 'High Cost', 'Price': 7138},
    {'Supplier': 'RSR', 'Tier': 'T5', 'Cost_Type': 'High Cost', 'Price': 6638},
    {'Supplier': 'RSR', 'Tier': 'T6', 'Cost_Type': 'High Cost', 'Price': 9482},
    {'Supplier': 'RSR', 'Tier': 'T7', 'Cost_Type': 'High Cost', 'Price': 13276},
    # Dublin (Medium)
    {'Supplier': 'RSR', 'Tier': 'T1', 'Cost_Type': 'Medium Cost', 'Price': 3119},
    {'Supplier': 'RSR', 'Tier': 'T2', 'Cost_Type': 'Medium Cost', 'Price': 3787},
    {'Supplier': 'RSR', 'Tier': 'T3', 'Cost_Type': 'Medium Cost', 'Price': 4820},
    {'Supplier': 'RSR', 'Tier': 'T4', 'Cost_Type': 'Medium Cost', 'Price': 6627},
    {'Supplier': 'RSR', 'Tier': 'T5', 'Cost_Type': 'Medium Cost', 'Price': 6058},
    {'Supplier': 'RSR', 'Tier': 'T6', 'Cost_Type': 'Medium Cost', 'Price': 8654},
    {'Supplier': 'RSR', 'Tier': 'T7', 'Cost_Type': 'Medium Cost', 'Price': 12116},
    # Birmingham (Medium/Low)
    {'Supplier': 'RSR', 'Tier': 'T1', 'Cost_Type': 'Medium/Low Cost', 'Price': 2780},
    {'Supplier': 'RSR', 'Tier': 'T2', 'Cost_Type': 'Medium/Low Cost', 'Price': 3376},
    {'Supplier': 'RSR', 'Tier': 'T3', 'Cost_Type': 'Medium/Low Cost', 'Price': 4297},
    {'Supplier': 'RSR', 'Tier': 'T4', 'Cost_Type': 'Medium/Low Cost', 'Price': 5908},
    {'Supplier': 'RSR', 'Tier': 'T5', 'Cost_Type': 'Medium/Low Cost', 'Price': 5150},
    {'Supplier': 'RSR', 'Tier': 'T6', 'Cost_Type': 'Medium/Low Cost', 'Price': 7357},
    {'Supplier': 'RSR', 'Tier': 'T7', 'Cost_Type': 'Medium/Low Cost', 'Price': 10300},
    # Warsaw (Low)
    {'Supplier': 'RSR', 'Tier': 'T1', 'Cost_Type': 'Low Cost', 'Price': 1597},
    {'Supplier': 'RSR', 'Tier': 'T2', 'Cost_Type': 'Low Cost', 'Price': 1939},
    {'Supplier': 'RSR', 'Tier': 'T3', 'Cost_Type': 'Low Cost', 'Price': 2468},
    {'Supplier': 'RSR', 'Tier': 'T4', 'Cost_Type': 'Low Cost', 'Price': 3393},
    {'Supplier': 'RSR', 'Tier': 'T5', 'Cost_Type': 'Low Cost', 'Price': 3214},
    {'Supplier': 'RSR', 'Tier': 'T6', 'Cost_Type': 'Low Cost', 'Price': 4592},
    {'Supplier': 'RSR', 'Tier': 'T7', 'Cost_Type': 'Low Cost', 'Price': 6428},

    # --- KORN FERRY PRICES ---
    # High Cost (London & Dublin)
    {'Supplier': 'KF', 'Tier': 'T1', 'Cost_Type': 'High Cost', 'Price': 2664},
    {'Supplier': 'KF', 'Tier': 'T2', 'Cost_Type': 'High Cost', 'Price': 3185},
    {'Supplier': 'KF', 'Tier': 'T3', 'Cost_Type': 'High Cost', 'Price': 4125},
    {'Supplier': 'KF', 'Tier': 'T4', 'Cost_Type': 'High Cost', 'Price': 5558},
    {'Supplier': 'KF', 'Tier': 'T5', 'Cost_Type': 'High Cost', 'Price': 5020},
    {'Supplier': 'KF', 'Tier': 'T6', 'Cost_Type': 'High Cost', 'Price': 7171},
    {'Supplier': 'KF', 'Tier': 'T7', 'Cost_Type': 'High Cost', 'Price': 10040},
    # Low Cost (Warsaw)
    {'Supplier': 'KF', 'Tier': 'T1', 'Cost_Type': 'Low Cost', 'Price': 2331},
    {'Supplier': 'KF', 'Tier': 'T2', 'Cost_Type': 'Low Cost', 'Price': 2809},
    {'Supplier': 'KF', 'Tier': 'T3', 'Cost_Type': 'Low Cost', 'Price': 3546},
    {'Supplier': 'KF', 'Tier': 'T4', 'Cost_Type': 'Low Cost', 'Price': 4835},
    {'Supplier': 'KF', 'Tier': 'T5', 'Cost_Type': 'Low Cost', 'Price': 4377},
    {'Supplier': 'KF', 'Tier': 'T6', 'Cost_Type': 'Low Cost', 'Price': 6253},
    {'Supplier': 'KF', 'Tier': 'T7', 'Cost_Type': 'Low Cost', 'Price': 8754},
]
df_pricing = pd.DataFrame(pricing_data)

# --- SESSION STATE MANAGEMENT ---
if 'budget_lines' not in st.session_state:
    st.session_state.budget_lines = []

# --- HELPER FUNCTIONS ---
def get_price(supplier, tier, cost_type):
    # Filter pricing data
    row = df_pricing[
        (df_pricing['Supplier'] == supplier) & 
        (df_pricing['Tier'] == tier) & 
        (df_pricing['Cost_Type'] == cost_type)
    ]
    if not row.empty:
        return row.iloc[0]['Price']
    return 0

# --- TITLE & HEADER ---
st.title("📊 Master RPO Budget Modeler")
st.markdown("""
Use this tool to build a multi-stream hiring budget. 
Add workflows to the model below to calculate total project cost and recruiter headcount requirements.
""")
st.markdown("---")

# --- SIDEBAR: INPUT FORM ---
with st.sidebar:
    st.header("1. Add Workflow")
    
    # Select Workflow
    selected_workflow = st.selectbox("Select Workflow:", df_workflows['Workflow Name'].unique())
    
    # Auto-fetch details
    wf_details = df_workflows[df_workflows['Workflow Name'] == selected_workflow].iloc[0]
    curr_supplier = wf_details['Supplier']
    curr_tier = wf_details['Pricing Tier']
    curr_ppr = wf_details['Avg PPR']
    
    st.info(f"**Supplier:** {curr_supplier} | **Tier:** {curr_tier} | **PPR:** {curr_ppr}")
    
    # Input Demand
    total_demand = st.number_input("Total Hires Needed (Demand):", min_value=1, value=10)
    
    st.subheader("2. Location Split (%)")
    st.caption("Ensure totals sum to 100%")
    
    # Dynamic Inputs based on Supplier capabilities
    high_pct = st.number_input("High Cost % (e.g. London):", 0, 100, 50)
    
    med_pct = 0
    if curr_supplier in ['RSR', 'Cielo']:
        med_pct = st.number_input("Medium Cost % (e.g. Dublin):", 0, 100, 0)
    else:
        st.caption("Medium Cost not applicable for KF (Dublin is High Cost)")
        
    med_low_pct = 0
    if curr_supplier == 'RSR':
        med_low_pct = st.number_input("Med/Low Cost % (RSR Only - B'ham):", 0, 100, 0)
        
    low_pct = st.number_input("Low Cost % (e.g. Warsaw):", 0, 100, 50)
    
    total_split = high_pct + med_pct + med_low_pct + low_pct
    
    if total_split != 100:
        st.error(f"Total Split is {total_split}%. Please adjust to equal 100%.")
        btn_disabled = True
    else:
        st.success("Split Valid")
        btn_disabled = False

    if st.button("Add to Model", disabled=btn_disabled):
        # Calculate Costs
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
        
        # Add to session state
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

# --- MAIN DISPLAY ---

if len(st.session_state.budget_lines) > 0:
    # Convert list to DataFrame
    df_results = pd.DataFrame(st.session_state.budget_lines)
    
    # USD Conversion Rate
    usd_rate = 1.15
    
    # 1. TOP LINE METRICS
    total_eur = df_results['Total Cost (€)'].sum()
    total_usd = total_eur * usd_rate
    total_headcount = df_results['Recruiters'].sum()
    total_volume = df_results['Demand'].sum()

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Project Cost (€)", f"€{total_eur:,.0f}")
    c2.metric("Total Project Cost ($)", f"${total_usd:,.0f}")
    c3.metric("Total Hires", f"{total_volume}")
    c4.metric("Recruiters Required", f"{total_headcount:.1f}")
    
    st.markdown("---")

    # 2. DETAILED TABLE & MANAGEMENT
    st.subheader("Budget Breakdown")
    
    # Prepare data for display
    df_display = df_results.copy()
    
    # CALCULATE USD COLUMN (New Step)
    df_display['Total Cost ($)'] = df_display['Total Cost (€)'] * usd_rate
    
    # Format columns (Add €/$ symbols and commas)
    df_display['Total Cost (€)'] = df_display['Total Cost (€)'].apply(lambda x: f"€{x:,.0f}")
    df_display['Total Cost ($)'] = df_display['Total Cost ($)'].apply(lambda x: f"${x:,.0f}")
    df_display['Recruiters'] = df_display['Recruiters'].apply(lambda x: f"{x:.1f}")
    
    # Reorder columns so Money is next to Money
    column_order = [
        "Workflow", "Supplier", "Demand", 
        "High Cost %", "Low Cost %", 
        "Total Cost (€)", "Total Cost ($)", 
        "Recruiters"
    ]
    
    # Show the table
    st.dataframe(df_display[column_order], use_container_width=True)
    
    # --- NEW REMOVE FUNCTIONALITY ---
    st.write("### Manage Rows")
    
    # --- NEW REMOVE FUNCTIONALITY ---
    st.write("### Manage Rows")
    c_rem1, c_rem2 = st.columns([3, 1])
    
    with c_rem1:
        # Create a list of options that looks like: "0. SWE - RSR (Demand: 10)"
        # We use 'enumerate' to get the ID (0, 1, 2...) of each row
        options = [f"{i}. {row['Workflow']} (Demand: {row['Demand']})" for i, row in enumerate(st.session_state.budget_lines)]
        selected_to_remove = st.multiselect("Select lines to remove:", options)
    
    with c_rem2:
        st.write("") # Spacing
        st.write("") # Spacing
        if st.button("Remove Selected"):
            if selected_to_remove:
                # 1. Get the ID numbers from the selection (the number before the dot)
                indices_to_remove = [int(s.split('.')[0]) for s in selected_to_remove]
                
                # 2. Rebuild the list, keeping only the rows we did NOT select
                new_list = [
                    row for i, row in enumerate(st.session_state.budget_lines) 
                    if i not in indices_to_remove
                ]
                
                # 3. Update the session state and refresh
                st.session_state.budget_lines = new_list
                st.rerun()

    if st.button("Clear Entire Model"):
        st.session_state.budget_lines = []
        st.rerun()

    st.markdown("---")

    # 3. VISUALIZATION
    c_chart1, c_chart2 = st.columns(2)
    
    with c_chart1:
        st.subheader("Spend by Vendor")
        vendor_spend = df_results.groupby("Supplier")['Total Cost (€)'].sum().reset_index()
        st.bar_chart(vendor_spend, x="Supplier", y="Total Cost (€)", color="#4285F4") # Google Blue

    with c_chart2:
        st.subheader("Spend by Workflow")
        st.bar_chart(df_results, x="Workflow", y="Total Cost (€)", color="#34A853") # Google Green

else:
    st.info("👈 Use the sidebar to add your first workflow scenario.")

# --- FOOTER ---
st.markdown("---")
st.caption("RPO Budget Calculator | Rates based on T6/T4 Contract Data | FX Rate €1 = $1.15")
