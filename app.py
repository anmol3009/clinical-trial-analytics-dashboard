import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ==========================================
# 1. PAGE CONFIGURATION & STYLING
# ==========================================
st.set_page_config(
    page_title="Clinical Trials Analytics",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS to just clean up the top whitespace, letting the rest scroll naturally
st.markdown("""
    <style>
    .block-container {
        padding-top: 1rem;
    }
    div[data-testid="stMetricValue"] {
        font-size: 1.8rem;
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 2. DATA LOADING
# ==========================================
@st.cache_data
def load_data():
    df = pd.read_csv('data/processed/clean_clinical_data.csv')
    if 'start_date' in df.columns:
        df['start_date'] = pd.to_datetime(df['start_date'], errors='coerce')
        df['start_year'] = df['start_date'].dt.year.fillna(0).astype(int)
    return df

df = load_data()

# ==========================================
# 3. SIDEBAR FILTERS
# ==========================================
st.sidebar.header("Dashboard Filters ⚙️")

available_phases = [p for p in df['phase'].unique() if str(p).lower() not in ['unknown', 'not applicable', 'nan', 'none']]
selected_phases = st.sidebar.multiselect("Select Trial Phase", available_phases, default=available_phases)

if 'condition_category' in df.columns:
    top_conditions_list = df['condition_category'].value_counts().head(20).index.tolist()
    selected_conditions = st.sidebar.multiselect("Select Condition", top_conditions_list, default=top_conditions_list[:5])
else:
    selected_conditions = []

filtered_df = df.copy()
if selected_phases:
    filtered_df = filtered_df[filtered_df['phase'].isin(selected_phases)]
if selected_conditions and 'condition_category' in df.columns:
    filtered_df = filtered_df[filtered_df['condition_category'].isin(selected_conditions)]

# ==========================================
# 4. MAIN DASHBOARD HEADER & KPIS (IN CARDS)
# ==========================================
st.title("Clinical Trial Performance & Conversion Analytics")

total_trials = len(filtered_df)
total_enrollment = filtered_df['enrollment'].sum() if 'enrollment' in filtered_df.columns else 0
avg_duration = filtered_df['duration_days'].mean() if 'duration_days' in filtered_df.columns else 0

if 'has_results' in filtered_df.columns:
    trials_with_results = len(filtered_df[filtered_df['has_results'].astype(str).str.lower().isin(['true', 'yes', '1'])]) if filtered_df['has_results'].dtype == object else filtered_df['has_results'].sum()
else:
    trials_with_results = 0

pct_with_results = (trials_with_results / total_trials * 100) if total_trials > 0 else 0
active_trials = filtered_df['is_recruiting'].sum() if 'is_recruiting' in filtered_df.columns else 0

# KPIs inside bordered containers
kpi1, kpi2, kpi3, kpi4, kpi5 = st.columns(5)
with kpi1.container(border=True):
    st.metric("Total Trials", f"{total_trials:,}")
with kpi2.container(border=True):
    st.metric("Total Enrollment", f"{total_enrollment:,.0f}")
with kpi3.container(border=True):
    st.metric("Avg Duration (Days)", f"{avg_duration:,.0f}")
with kpi4.container(border=True):
    st.metric("% with Results", f"{pct_with_results:.1f}%")
with kpi5.container(border=True):
    st.metric("Active (Recruiting)", f"{active_trials:,}")

if filtered_df.empty:
    st.warning("No data available for the selected filters.")
    st.stop()

# ==========================================
# 5. GRID LAYOUT WITH INDIVIDUAL SECTIONS
# ==========================================
col1, col2, col3, col4 = st.columns([1.2, 1, 1, 1])

# --- COLUMN 1: FUNNEL ---
with col1:
    with st.container(border=True):
        st.markdown("**Conversion Funnel**")
        enrollment_stage = len(filtered_df[filtered_df['enrollment'] > 0])
        treatment = len(filtered_df.dropna(subset=['start_date'])) if 'start_date' in filtered_df.columns else int(total_trials * 0.8)
        retention = filtered_df['is_completed'].sum() if 'is_completed' in filtered_df.columns else 0
        
        fig_funnel = go.Figure(go.Funnel(
            y=['Screening', 'Enrollment', 'Treatment', 'Retention', 'Outcome'], 
            x=[total_trials, enrollment_stage, treatment, retention, trials_with_results], 
            textinfo="value+percent initial",
            marker={"color": ["#6A98F0", "#4A6EE0", "#5A4FCF", "#483698", "#2F1B54"]}
        ))
        fig_funnel.update_layout(margin=dict(l=10, r=20, t=10, b=10), plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', height=630)
        st.plotly_chart(fig_funnel, use_container_width=True)

# --- COLUMN 2: TRENDS & CONDITIONS ---
with col2:
    with st.container(border=True):
        st.markdown("**Trial Trends (Last 12M)**")
        if 'start_date' in filtered_df.columns:
            filtered_df['start_month'] = filtered_df['start_date'].dt.to_period('M').astype(str)
            trend_data = filtered_df.groupby('start_month').size().reset_index(name='count').sort_values('start_month').tail(12)
            fig_trends = px.line(trend_data, x='start_month', y='count', markers=True, text='count', color_discrete_sequence=['#5C6BC0'])
            
            max_trend = trend_data['count'].max() if not trend_data.empty else 100
            # Force left alignment by setting l=0 and turning off the X-axis angle that pushes it right
            fig_trends.update_xaxes(tickangle=0)
            fig_trends.update_yaxes(range=[0, max_trend * 1.25], showgrid=True, gridcolor='rgba(128,128,128,0.2)', automargin=True)
            fig_trends.update_traces(fill='tozeroy', fillcolor='rgba(92, 107, 192, 0.2)', textposition="top center")
            fig_trends.update_layout(xaxis_title="", yaxis_title="", margin=dict(t=10, b=20, l=0, r=10), height=290, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig_trends, use_container_width=True)
    
    with st.container(border=True):
        st.markdown("**Top Conditions**")
        if 'condition_category' in filtered_df.columns:
            top_conditions = filtered_df[filtered_df['condition_category'].str.lower() != 'other']['condition_category'].value_counts().nlargest(5).reset_index()
            top_conditions.columns = ['condition', 'trial_count']
            fig_conditions = px.bar(top_conditions, x='trial_count', y='condition', orientation='h', text_auto=True, color_discrete_sequence=['#3949AB'])
            fig_conditions.update_traces(textposition='outside') 
            
            max_cond = top_conditions['trial_count'].max() if not top_conditions.empty else 100
            fig_conditions.update_xaxes(range=[0, max_cond * 1.25], visible=False) 
            # Automargin True ensures the long text labels don't get cut off, l=0 anchors it left
            fig_conditions.update_layout(yaxis={'categoryorder':'total ascending', 'title': '', 'automargin': True}, margin=dict(t=10, b=10, l=0, r=10), height=290, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig_conditions, use_container_width=True)

# --- COLUMN 3: COUNTRIES & PHASE ---
with col3:
    with st.container(border=True):
        st.markdown("**Top 5 Countries**")
        if 'country' in filtered_df.columns:
            df_countries = filtered_df.assign(country=filtered_df['country'].astype(str).str.split(r'[;,]')).explode('country')
            df_countries['country'] = df_countries['country'].str.strip()
            df_countries = df_countries[df_countries['country'].str.lower() != 'unknown']
            top_countries = df_countries.groupby('country')['enrollment'].sum().nlargest(5).reset_index()
            fig_countries = px.bar(top_countries, x='enrollment', y='country', orientation='h', text_auto='.2s', color_discrete_sequence=['#D4AF37'])
            fig_countries.update_traces(textposition='outside')
            
            max_country = top_countries['enrollment'].max() if not top_countries.empty else 100
            fig_countries.update_xaxes(range=[0, max_country * 1.25], visible=False)
            fig_countries.update_layout(yaxis={'categoryorder':'total ascending', 'title': '', 'automargin': True}, margin=dict(t=10, b=10, l=0, r=10), height=290, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig_countries, use_container_width=True)
        
    with st.container(border=True):
        st.markdown("**Trials by Phase**")
        if 'phase' in filtered_df.columns:
            phase_counts = filtered_df['phase'].value_counts().reset_index()
            phase_counts.columns = ['phase', 'count']
            fig_phase = px.pie(phase_counts, values='count', names='phase', hole=0.55, color_discrete_sequence=['#2F1B54', '#483698', '#5A4FCF', '#6A98F0'])
            fig_phase.update_traces(textposition='inside', textinfo='percent+label')
            fig_phase.update_layout(margin=dict(t=10, b=10, l=0, r=0), height=290, showlegend=False, paper_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig_phase, use_container_width=True)

# --- COLUMN 4: SPONSORS & STATUS ---
with col4:
    with st.container(border=True):
        st.markdown("**Top Sponsors**")
        if 'sponsor' in filtered_df.columns:
            top_sponsors = filtered_df['sponsor'].value_counts().nlargest(5).reset_index()
            top_sponsors.columns = ['sponsor', 'trial_count']
            fig_sponsors = px.bar(top_sponsors, x='trial_count', y='sponsor', orientation='h', text_auto=True, color_discrete_sequence=['#5A4FCF'])
            fig_sponsors.update_traces(textposition='outside')
            
            max_sponsor = top_sponsors['trial_count'].max() if not top_sponsors.empty else 100
            fig_sponsors.update_xaxes(range=[0, max_sponsor * 1.25], visible=False)
            fig_sponsors.update_layout(yaxis={'categoryorder':'total ascending', 'title': '', 'automargin': True}, margin=dict(t=10, b=10, l=0, r=10), height=290, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig_sponsors, use_container_width=True)

    with st.container(border=True):
        st.markdown("**Current Trial Status**")
        if 'status' in filtered_df.columns:
            status_counts = filtered_df['status'].value_counts().nlargest(5).reset_index()
            status_counts.columns = ['status', 'count']
            fig_status = px.bar(status_counts, x='status', y='count', text_auto=True, color_discrete_sequence=['#4A6EE0'])
            fig_status.update_traces(textposition='outside')
            
            max_status = status_counts['count'].max() if not status_counts.empty else 100
            fig_status.update_yaxes(range=[0, max_status * 1.25], visible=False) 
            fig_status.update_layout(
                xaxis={'categoryorder':'total descending', 'tickangle': -45, 'title': '', 'tickfont': dict(size=10)}, 
                margin=dict(t=10, b=20, l=0, r=10), height=290, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)'
            )
            st.plotly_chart(fig_status, use_container_width=True)