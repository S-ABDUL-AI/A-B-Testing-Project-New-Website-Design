import streamlit as st
import pandas as pd
import numpy as np
from scipy import stats
import altair as alt  # For plotting

# ==========================
# Streamlit App Config
# ==========================
st.set_page_config(page_title="A/B Testing Dashboard", page_icon="📊")

st.title("📊 A/B Testing Dashboard")
st.write("""
Upload your A/B test dataset or simulate one, and get instant conversion analysis.
The CSV must have the following columns: `user_id`, `group` (A/B), and `converted` (0/1).
""")

# ==========================
# Sidebar: Data Upload or Simulation
# ==========================
st.sidebar.header("Dataset Options")

uploaded_file = st.sidebar.file_uploader("Upload CSV", type=["csv"])
df = None
if uploaded_file:
    try:
        df = pd.read_csv(uploaded_file)
        st.sidebar.success("CSV uploaded successfully!")
    except Exception as e:
        st.sidebar.error(f"Error reading CSV: {e}")

# Simulation parameters
st.sidebar.header("Simulate A/B Test")
simulate = st.sidebar.checkbox("Simulate Sample Dataset")
if simulate:
    np.random.seed(42)
    n_users_a = st.sidebar.number_input("Users in Group A", min_value=10, value=250, step=10)
    n_users_b = st.sidebar.number_input("Users in Group B", min_value=10, value=250, step=10)
    p_a = st.sidebar.slider("Conversion Probability Group A", 0.0, 1.0, 0.2)
    p_b = st.sidebar.slider("Conversion Probability Group B", 0.0, 1.0, 0.25)
    n_simulations = st.sidebar.number_input("Number of Simulations", min_value=1, value=100, step=10)

    df_a = pd.DataFrame({
        "user_id": range(1, n_users_a + 1),
        "group": "A",
        "converted": np.random.binomial(1, p_a, n_users_a)
    })
    df_b = pd.DataFrame({
        "user_id": range(n_users_a + 1, n_users_a + n_users_b + 1),
        "group": "B",
        "converted": np.random.binomial(1, p_b, n_users_b)
    })
    df = pd.concat([df_a, df_b], ignore_index=True)
    st.sidebar.success("Sample dataset created!")

# ==========================
# Dataset Validation
# ==========================
if df is None:
    st.info("Upload a CSV or simulate a dataset from the sidebar to begin.")
    st.stop()

required_cols = {"user_id", "group", "converted"}
if not required_cols.issubset(df.columns):
    st.error(f"CSV must contain columns: {required_cols}. Found: {set(df.columns)}")
    st.stop()

st.subheader("Preview of Dataset")
st.dataframe(df.head())

# ==========================
# Confidence Level Selection
# ==========================
st.sidebar.header("Statistical Test Options")
confidence_level = st.sidebar.selectbox(
    "Select Confidence Level",
    options=[0.90, 0.95, 0.99],
    format_func=lambda x: f"{int(x * 100)}%"
)
alpha = 1 - confidence_level

# ==========================
# Single A/B Test Analysis
# ==========================
st.subheader("Single A/B Test Results")

conversion_table = df.groupby("group")["converted"].agg(['sum', 'count'])
conversion_table['conversion_rate'] = conversion_table['sum'] / conversion_table['count']
st.write("Conversion Summary:")
st.dataframe(conversion_table)

# Z-test for proportions
conv_a = conversion_table.loc['A', 'sum']
n_a = conversion_table.loc['A', 'count']
conv_b = conversion_table.loc['B', 'sum']
n_b = conversion_table.loc['B', 'count']

p_pool = (conv_a + conv_b) / (n_a + n_b)
se = np.sqrt(p_pool * (1 - p_pool) * (1 / n_a + 1 / n_b))
z_score = (conversion_table.loc['B', 'conversion_rate'] - conversion_table.loc['A', 'conversion_rate']) / se
p_value = 2 * (1 - stats.norm.cdf(abs(z_score)))

st.write(f"Z-score: {z_score:.4f}")
st.write(f"P-value: {p_value:.4f}")
st.write(f"Selected Confidence Level: {int(confidence_level * 100)}% (α = {alpha:.2f})")

if p_value < alpha:
    st.success(f"✅ Statistically significant difference detected between groups A and B!")
else:
    st.info(f"ℹ️ No statistically significant difference detected between groups A and B.")

# ==========================
# Conversion Rate Plot
# ==========================
st.subheader("Conversion Rate Visualization")

plot_df = conversion_table.reset_index()[['group', 'conversion_rate']]
chart = alt.Chart(plot_df).mark_bar(color="#3AA873").encode(
    x='group',
    y=alt.Y('conversion_rate', title='Conversion Rate'),
    tooltip=['group', alt.Tooltip('conversion_rate', format=".2%")]
).properties(
    width=500,
    height=400
)
st.altair_chart(chart, use_container_width=True)

# ==========================
# Multiple Simulations Analysis
# ==========================
if simulate and n_simulations > 1:
    st.subheader("Simulation: Distribution of Z-scores and P-values")

    z_scores = []
    p_values = []
    for _ in range(n_simulations):
        sim_a = np.random.binomial(1, p_a, n_users_a)
        sim_b = np.random.binomial(1, p_b, n_users_b)
        conv_a_sim = sim_a.sum()
        conv_b_sim = sim_b.sum()
        p_pool_sim = (conv_a_sim + conv_b_sim) / (n_users_a + n_users_b)
        se_sim = np.sqrt(p_pool_sim * (1 - p_pool_sim) * (1 / n_users_a + 1 / n_users_b))
        z = (sim_b.mean() - sim_a.mean()) / se_sim
        p = 2 * (1 - stats.norm.cdf(abs(z)))
        z_scores.append(z)
        p_values.append(p)

    sim_df = pd.DataFrame({'z_score': z_scores, 'p_value': p_values})

    # Plot Z-scores
    st.write("Z-score Distribution")
    z_chart = alt.Chart(sim_df).mark_bar(color="#FF7F50").encode(
        alt.X("z_score:Q", bin=alt.Bin(maxbins=30), title="Z-score"),
        y='count()',
        tooltip=['count()']
    ).properties(width=600, height=300)
    st.altair_chart(z_chart, use_container_width=True)

    # Plot P-values
    st.write("P-value Distribution")
    p_chart = alt.Chart(sim_df).mark_bar(color="#1E90FF").encode(
        alt.X("p_value:Q", bin=alt.Bin(maxbins=30), title="P-value"),
        y='count()',
        tooltip=['count()']
    ).properties(width=600, height=300)
    st.altair_chart(p_chart, use_container_width=True)

    significant = np.sum(sim_df['p_value'] < alpha)
    st.write(
        f"Out of {n_simulations} simulations, {significant} were statistically significant at {int(confidence_level * 100)}% confidence level.")
