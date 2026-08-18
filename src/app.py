import os

import plotly.express as px
import streamlit as st

from backend import backend_mode
from database import get_recent_events, init_db, log_event, verify_login
from firebase_auth import sign_in_with_email_password
from model import train_model
from stream_service import start_live_stream, stream_snapshot
from utils import compute_rfm, load_data

st.set_page_config(page_title="Customer Intelligence", layout="wide")

st.markdown(
    """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

        html, body, [class*="css"] {
            font-family: 'Inter', sans-serif;
            background: linear-gradient(135deg, #071120 0%, #0d1f38 45%, #0a1325 100%);
            color: #eaf2ff;
        }

        .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
            max-width: 1500px;
        }

        .main > div {
            background: rgba(10, 17, 30, 0.72);
            border: 1px solid rgba(148, 163, 184, 0.15);
            border-radius: 22px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.25);
            padding: 1.2rem 1.5rem;
        }

        .glass-panel {
            background: rgba(15, 23, 42, 0.85);
            border: 1px solid rgba(148, 163, 184, 0.18);
            border-radius: 18px;
            padding: 1.2rem;
            box-shadow: 0 8px 25px rgba(15, 23, 42, 0.25);
            margin-bottom: 1rem;
        }

        .main-title {
            font-size: 2.6rem;
            font-weight: 800;
            letter-spacing: -0.04em;
            margin: 0;
            color: #f8fbff;
        }

        .subtitle {
            font-size: 0.95rem;
            color: #a8bbd8;
            margin-top: 0.35rem;
            margin-bottom: 1.5rem;
        }

        .metric-box {
            background: linear-gradient(135deg, rgba(30, 41, 59, 0.9), rgba(15, 118, 110, 0.08));
            border: 1px solid rgba(96, 165, 250, 0.18);
            border-radius: 18px;
            padding: 1rem 1.1rem;
            min-height: 120px;
        }

        .metric-label {
            color: #93a9c9;
            font-size: 0.84rem;
            text-transform: uppercase;
            letter-spacing: 0.08em;
        }

        .metric-value {
            font-size: 2rem;
            font-weight: 800;
            margin-top: 0.45rem;
            color: white;
        }

        .stTabs [role="tablist"] {
            gap: 0.75rem;
        }

        .stTabs [role="tab"] {
            height: 2.7rem;
            white-space: nowrap;
            background: rgba(15, 23, 42, 0.7);
            border: 1px solid rgba(148, 163, 184, 0.15);
            border-radius: 12px;
            color: #dfeafb;
            padding: 0 1rem;
        }

        .stTabs [role="tab"][aria-selected="true"] {
            background: linear-gradient(135deg, #2563eb, #38bdf8);
            color: white;
            border-color: transparent;
        }

        .stButton > button {
            width: 100%;
            border-radius: 12px;
            border: none;
            background: linear-gradient(135deg, #2563eb, #38bdf8);
            color: white;
            font-weight: 700;
            padding: 0.7rem 1rem;
        }

        .stButton > button:hover {
            background: linear-gradient(135deg, #1d4ed8, #0ea5e9);
        }

        .stTextInput > div > div > input,
        .stNumberInput > div > div > input,
        .stSelectbox > div > div > select {
            background: rgba(15, 23, 42, 0.9);
            color: #eff6ff;
            border: 1px solid rgba(148, 163, 184, 0.24);
            border-radius: 12px;
        }

        .stDataFrame {
            background: rgba(15, 23, 42, 0.7);
            border-radius: 14px;
        }

        .stJson {
            background: rgba(15, 23, 42, 0.7);
            border-radius: 12px;
            padding: 0.75rem;
        }

        .success {
            color: #86efac;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

init_db()

if 'auth_user' not in st.session_state:
    st.session_state.auth_user = None

if st.session_state.auth_user is None:
    st.title("Secure Access")
    st.caption(f"Authentication backend: {backend_mode()}")

    with st.container():
        col_left, col_right = st.columns([1.2, 0.8])
        with col_left:
            st.markdown('<div class="glass-panel"><h2 style="margin:0; color:#f8fbff;">Customer Intelligence</h2><p style="color:#bfd0ea; margin:8px 0 0 0;">Enterprise analytics for growth, retention, and customer value.</p></div>', unsafe_allow_html=True)
        with col_right:
            st.markdown('<div class="glass-panel"><div class="metric-label">Status</div><div class="metric-value" style="font-size:1.2rem;">Live</div></div>', unsafe_allow_html=True)

    username = st.text_input("Username or Email", value="admin")
    password = st.text_input("Password", type="password", value="admin123")

    if st.button("Login"):
        firebase_user = sign_in_with_email_password(username, password) if '@' in username else None
        if firebase_user:
            st.session_state.auth_user = {'username': firebase_user['email'], 'email': firebase_user['email']}
            log_event(firebase_user['email'], 'firebase_login', 'Firebase login success')
            st.success("Firebase login successful")
            st.rerun()
        else:
            user = verify_login(username, password)
            if user:
                st.session_state.auth_user = user
                log_event(username, 'login', 'Successful login')
                st.success("Login successful")
                st.rerun()
            else:
                st.error("Invalid credentials")
    st.stop()

st.markdown('<p class="main-title">Customer Intelligence Dashboard</p>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Backend mode: <strong>{}</strong> | Firebase-ready configuration active</div>'.format(backend_mode()), unsafe_allow_html=True)

if st.button("Logout"):
    st.session_state.auth_user = None
    st.rerun()

start_live_stream()

# Load data with automatic path resolution
df = load_data()
rfm = compute_rfm(df)
model = train_model(rfm)

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown('<div class="metric-box"><div class="metric-label">Customers</div><div class="metric-value">{}</div></div>'.format(len(rfm)), unsafe_allow_html=True)
with col2:
    st.markdown('<div class="metric-box"><div class="metric-label">Revenue</div><div class="metric-value">${:,.0f}</div></div>'.format(df['TotalAmount'].sum()), unsafe_allow_html=True)
with col3:
    st.markdown('<div class="metric-box"><div class="metric-label">Avg Frequency</div><div class="metric-value">{}</div></div>'.format(round(rfm['Frequency'].mean(), 2)), unsafe_allow_html=True)
with col4:
    st.markdown('<div class="metric-box"><div class="metric-label">User</div><div class="metric-value" style="font-size:1.25rem;">{}</div></div>'.format(st.session_state.auth_user['username']), unsafe_allow_html=True)

segment_filter = st.selectbox("Select Segment", ["All"] + list(rfm['Segment'].unique()))
filtered = rfm if segment_filter == "All" else rfm[rfm['Segment'] == segment_filter]

st.subheader("Segment Distribution")
segment_counts = filtered['Segment'].value_counts().reset_index()
segment_counts.columns = ['Segment', 'Customers']
fig = px.bar(segment_counts, x='Segment', y='Customers', title='Segments')
fig.update_layout(
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    font=dict(color='#eaf2ff'),
    title_font=dict(color='#f8fbff', size=18),
    legend=dict(font=dict(color='#dfeafb')),
    xaxis=dict(color='#dfeafb', gridcolor='rgba(148,163,184,0.14)'),
    yaxis=dict(color='#dfeafb', gridcolor='rgba(148,163,184,0.14)'),
)
st.plotly_chart(fig, use_container_width=True)

st.subheader("Customer Data")
st.dataframe(filtered.head(), use_container_width=True)

st.subheader("Predict Customer Value")
with st.container():
    col_a, col_b, col_c = st.columns(3)
    with col_a:
        r = st.number_input("Recency", 0)
    with col_b:
        f = st.number_input("Frequency", 0)
    with col_c:
        m = st.number_input("Monetary", 0.0)

    if st.button("Predict"):
        pred = model.predict([[r, f, m]])[0]
        if pred == 1:
            st.success("VIP Customer")
            log_event(st.session_state.auth_user['username'], 'prediction', 'VIP prediction', {'recency': r, 'frequency': f, 'monetary': m})
        else:
            st.warning("Normal Customer")
            log_event(st.session_state.auth_user['username'], 'prediction', 'Normal customer prediction', {'recency': r, 'frequency': f, 'monetary': m})

st.subheader("Live Event Stream")
feed = stream_snapshot()[-10:]
if feed:
    st.json(feed)
else:
    st.info("No live events yet.")

st.subheader("Recent Database Events")
st.json(get_recent_events(10))

st.caption("This is a SaaS-style foundation powered by SQLite for local storage and a live event stream for real-time updates.")
