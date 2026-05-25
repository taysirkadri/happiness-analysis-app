import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_absolute_error
from pathlib import Path

# ── Config ────────────────────────────────────────────────────
st.set_page_config(
    page_title="The Recipe for a Happy Country",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Custom CSS ────────────────────────────────────────────────
st.markdown("""
<style>
    /* Base */
    .stApp { background-color: #FFFFFF; }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #F8F8F8;
        border-right: 1px solid #E0E0E0;
    }

    /* Metrics */
    [data-testid="stMetric"] {
        background-color: #F8F8F8;
        border: 1px solid #E0E0E0;
        border-radius: 8px;
        padding: 12px;
    }
    [data-testid="stMetricValue"] {
        color: #111111 !important;
        font-size: 1.8rem !important;
    }
    [data-testid="stMetricLabel"] {
        color: #666666 !important;
    }

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        background-color: #F0F0F0;
        border-radius: 6px;
        padding: 3px;
    }
    .stTabs [data-baseweb="tab"] {
        color: #444444;
        border-radius: 5px;
    }
    .stTabs [aria-selected="true"] {
        background-color: #111111 !important;
        color: #FFFFFF !important;
    }

    /* Typography */
    h1, h2, h3 { color: #111111 !important; }
    p, li { color: #333333; }

    /* Prediction box */
    .predict-box {
        background-color: #111111;
        border-radius: 10px;
        padding: 20px;
        text-align: center;
        margin-top: 20px;
    }
    .predict-score {
        font-size: 2.8rem;
        font-weight: bold;
        color: #FFFFFF;
    }
    .predict-label {
        color: #AAAAAA;
        font-size: 0.9rem;
        margin-top: 5px;
    }
    .predict-sublabel {
        color: #666666;
        font-size: 0.75rem;
        margin-top: 6px;
    }

    /* Hint box */
    .hint-box {
        background-color: #F8F8F8;
        border-left: 3px solid #111111;
        border-radius: 4px;
        padding: 10px 14px;
        margin-top: 12px;
        font-size: 0.8rem;
        color: #444444;
    }

    /* Dividers */
    hr { border-color: #E0E0E0; }
</style>
""", unsafe_allow_html=True)

# ── Data loading ──────────────────────────────────────────────
@st.cache_data
def load_data():
    base = Path(__file__).parent.parent / "data" / "processed"
    train = pd.read_csv(base / "lab4_train_model_ready.csv")
    test  = pd.read_csv(base / "lab4_test_model_ready.csv")
    return train, test

train_df, test_df = load_data()

FEATURES = ["gdp_per_capita", "social_support", "life_expectancy",
            "freedom", "trust", "generosity"]
LABELS   = ["GDP per Capita", "Social Support", "Life Expectancy",
            "Freedom", "Trust in Govt", "Generosity"]
TARGET   = "happiness_score"

# ── Train model ───────────────────────────────────────────────
@st.cache_resource
def train_model():
    model = LinearRegression()
    model.fit(train_df[FEATURES], train_df[TARGET])
    return model

model     = train_model()
preds     = model.predict(test_df[FEATURES])
r2        = r2_score(test_df[TARGET], preds)
mae       = mean_absolute_error(test_df[TARGET], preds)
residuals = test_df[TARGET].values - preds

# Compute mean and std from training data for real-world conversion
means = train_df[FEATURES].mean()
stds  = train_df[FEATURES].std()

# ── Sidebar ───────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🔮 Build Your Country")
    st.markdown("*Adjust real-world values to predict happiness*")
    st.markdown("---")
    slider_config = {
        "gdp_per_capita":  ("💰 GDP per Capita",  -3.0, 3.0, 0.0),
        "social_support":  ("🤝 Social Support",  -3.0, 3.0, 0.0),
        "life_expectancy": ("❤️ Life Expectancy",  -3.0, 3.0, 0.0),
        "freedom":         ("🗽 Freedom",          -3.0, 3.0, 0.0),
        "trust":           ("🏛️ Trust in Govt",    -3.0, 3.0, 0.0),
        "generosity":      ("🎁 Generosity",       -3.0, 3.0, 0.0),
    }

    user_vals_std = {}
    for feat, (label, lo, hi, default) in slider_config.items():
        user_vals_std[feat] = st.slider(label, lo, hi, default, 0.1)

    user_df     = pd.DataFrame([user_vals_std])
    raw_pred    = model.predict(user_df)[0]
    
    happiness   = float(np.clip(raw_pred, 2.5, 8.0))

    # Level and emoji
    if happiness >= 7.0:
        emoji, level = "🌟", "Very Happy Country"
    elif happiness >= 6.0:
        emoji, level = "😊", "Happy Country"
    elif happiness >= 5.0:
        emoji, level = "😐", "Average Country"
    elif happiness >= 4.0:
        emoji, level = "😟", "Struggling Country"
    else:
        emoji, level = "😔", "Very Unhappy Country"

    st.markdown(f"""
    <div class="predict-box">
        <div class="predict-score">{emoji} {happiness:.2f}</div>
        <div class="predict-label">{level}</div>
        <div class="predict-sublabel">out of 10 &nbsp;·&nbsp; world avg ≈ 5.4</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="hint-box">
        🌍 <b>Real examples:</b><br>
        Finland ≈ 7.8 &nbsp;|&nbsp; Algeria ≈ 5.2 &nbsp;|&nbsp; Burundi ≈ 2.9
    </div>
    """, unsafe_allow_html=True)

# ── Header ────────────────────────────────────────────────────
st.markdown("# 🌍 The Recipe for a Happy Country")
st.markdown("*A data science journey through the World Happiness Report (2015–2019)*")
st.markdown("---")

# ── KPI Row ───────────────────────────────────────────────────
k1, k2, k3, k4 = st.columns(4)
k1.metric("Countries Analyzed", "~156 / year")
k2.metric("Years Covered",      "2015 – 2019")
k3.metric("Model R²",           f"{r2:.2f}")
k4.metric("Mean Abs. Error",    f"{mae:.3f}")

st.markdown("---")

# ── Tabs ──────────────────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs([
    "📊 What Drives Happiness",
    "🎯 Model Performance",
    "🔍 Residuals",
    "📖 The Journey"
])

# ── TAB 1: Coefficients ───────────────────────────────────────
with tab1:
    st.subheader("Feature Importance — OLS Coefficients")
    st.caption("All features standardized → coefficients are directly comparable")

    coef_df = pd.DataFrame({
        "Feature":     LABELS,
        "Coefficient": model.coef_,
    }).sort_values("Coefficient", ascending=True)

    fig = px.bar(
        coef_df,
        x="Coefficient",
        y="Feature",
        orientation="h",
        color="Coefficient",
        color_continuous_scale=["#EEEEEE", "#888888", "#111111"],
        template="plotly_dark",
        title="Which features predict happiness most?"
    )
    fig.update_layout(
        plot_bgcolor="#FFFFFF",
        paper_bgcolor="#FFFFFF",
        font_color="#111111",
        showlegend=False,
        coloraxis_showscale=False,
        height=400,
        margin=dict(l=20, r=20, t=50, b=20)
    )
    fig.add_vline(x=0, line_color="#ffffff", line_width=1)
    st.plotly_chart(fig, use_container_width=True)

    c1, c2, c3 = st.columns(3)
    c1.info("💰 **GDP** is the strongest single predictor at +0.407")
    c2.success("🗽 **Freedom + Social Support** combined (0.556) nearly match GDP")
    c3.warning("🎁 **Generosity** barely moves the needle globally (0.024)")

# ── TAB 2: Actual vs Predicted ────────────────────────────────
with tab2:
    st.subheader("Actual vs Predicted Happiness Scores")

    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(
        x=test_df[TARGET],
        y=preds,
        mode="markers",
        marker=dict(color="#2980b9", size=10, opacity=0.8,
                    line=dict(color="#ffffff", width=1)),
        name="Countries",
        hovertemplate="Actual: %{x:.2f}<br>Predicted: %{y:.2f}<extra></extra>"
    ))
    mn = min(test_df[TARGET].min(), preds.min()) - 0.2
    mx = max(test_df[TARGET].max(), preds.max()) + 0.2
    fig2.add_trace(go.Scatter(
        x=[mn, mx], y=[mn, mx],
        mode="lines",
        line=dict(color="#f39c12", dash="dash", width=2),
        name="Perfect prediction"
    ))
    fig2.update_layout(
        plot_bgcolor="#FFFFFF",
        paper_bgcolor="#FFFFFF",
        font_color="#111111",
        xaxis_title="Actual Happiness Score",
        yaxis_title="Predicted Happiness Score",
        template="plotly_dark",
        height=450,
        margin=dict(l=20, r=20, t=30, b=20)
    )
    st.plotly_chart(fig2, use_container_width=True)
    st.caption(f"R² = {r2:.3f} — dots close to the orange line = accurate predictions")

# ── TAB 3: Residuals ─────────────────────────────────────────
with tab3:
    st.subheader("Residuals — What the Model Gets Wrong")

    col1, col2 = st.columns(2)

    with col1:
        fig3 = go.Figure()
        fig3.add_trace(go.Scatter(
            x=preds, y=residuals,
            mode="markers",
            marker=dict(color="#27ae60", size=9, opacity=0.8),
            hovertemplate="Predicted: %{x:.2f}<br>Residual: %{y:.2f}<extra></extra>"
        ))
        fig3.add_hline(y=0, line_color="#f39c12", line_dash="dash", line_width=2)
        fig3.update_layout(
            plot_bgcolor="#FFFFFF",
            paper_bgcolor="#FFFFFF",
            font_color="#111111",
            xaxis_title="Predicted",
            yaxis_title="Residual",
            title="Residuals vs Predicted",
            template="plotly_dark",
            height=380
        )
        st.plotly_chart(fig3, use_container_width=True)

    with col2:
        fig4 = px.histogram(
            x=residuals, nbins=15,
            template="plotly_dark",
            title="Residual Distribution",
            color_discrete_sequence=["#2980b9"]
        )
        fig4.update_layout(
            plot_bgcolor="#FFFFFF",
            paper_bgcolor="#FFFFFF",
            font_color="#111111",
            xaxis_title="Residual",
            yaxis_title="Count",
            height=380
        )
        st.plotly_chart(fig4, use_container_width=True)

    st.caption("Random scatter around 0 = linear model is appropriate. Bell-shaped histogram = errors are normally distributed.")

# ── TAB 4: Story ─────────────────────────────────────────────
with tab4:
    st.subheader("The Journey — Lab by Lab")

    labs = [
        ("🗂️ Lab 0", "Dataset Selection",
         "Five CSVs, five different schemas. Built a 12-entry normalization map before writing a single line of analysis."),
        ("📈 Lab 1", "Trust vs Happiness",
         "Trust alone: R² = 0.18. I expected more. That single number set the agenda for everything that followed."),
        ("📊 Lab 2", "Inferential Statistics",
         "Cohen's d > 1.0 between high/low trust countries. Large effect — but GDP is almost certainly the confounder."),
        ("🔍 Lab 3", "Data Provenance",
         "Documented where every row came from. Reproducibility isn't a checkbox — it's the difference between 'I got these results' and 'anyone can get these results'."),
        ("🧹 Lab 4", "Preprocessing",
         "Split before scaling. That one rule prevents data leakage and protects every model that follows."),
        ("⚙️ Lab 4b", "Feature Engineering",
         "Built 4 new features: GDP×social interaction, life expectancy squared, freedom/trust ratio, generosity residual."),
        ("🔭 Lab 5", "Full EDA",
         "GDP and life expectancy correlate at r=0.84. Multicollinearity flagged — the model can't fully separate them."),
        ("🤖 Lab 6", "Baseline Model",
         "Linear regression: R²=0.76 on holdout. 5-fold CV confirmed 0.74. The convergence is exactly what I wanted to see."),
        ("🏆 Lab 7", "OLS vs Ridge vs Lasso",
         "All three scored R²=0.76. Regularization didn't help — with 6 features and small N, overfitting isn't the problem."),
    ]

    for icon_title, subtitle, body in labs:
        with st.expander(f"{icon_title} — {subtitle}"):
            st.markdown(f"*{body}*")

    st.markdown("---")
    st.markdown("""
    **Final answer:** GDP matters most. But Freedom + Social Support combined nearly match it —
    and those are things a country can actually build, independently of raw wealth.
    """)
    st.sidebar.caption(f"raw model output: {raw_pred:.3f}")
