"""Random Hostname Generator - Streamlit app.

Run locally:   streamlit run app/streamlit_app.py
"""
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

import hostnames as hn

st.set_page_config(page_title="Hostname Generator", page_icon="🖥️", layout="wide")

# Colors taken from the notebook
OS_COLORS = {"Linux": "#4655AE", "Solaris": "#F9734F", "AIX": "#6E56A0", "HP-UX": "#F25D71"}
ENV_COLORS = {"Development": "#F19A21", "Integration": "#F32A78", "Production": "#4655AE",
              "Staging": "#00ABD7", "Testing": "#9ACA29"}
COUNTRY_COLORS = {"Norway": "#9ACA29", "Germany": "#F32A78", "Italy": "#813696",
                  "Spain": "#00ABD7", "Ireland": "#F9734F", "France": "#012290"}

# ---------------- Sidebar ----------------
st.sidebar.header("⚙️ Settings")
n_hosts = st.sidebar.slider("Number of hostnames", 100, 10_000, 1500, step=100)
seed = st.sidebar.number_input("Random seed (0 = random)", min_value=0, value=0, step=1)
if st.sidebar.button("🔄 Generate new hostnames", width="stretch"):
    st.session_state.pop("df", None)

key = (n_hosts, seed)
if st.session_state.get("key") != key or "df" not in st.session_state:
    if seed:
        hn.random.seed(seed)
    st.session_state.df = hn.build_dataframe(n_hosts)
    st.session_state.key = key
df = st.session_state.df

# ---------------- Header ----------------
st.title("🖥️ Random Hostname Generator")
st.markdown(
    "Hostnames of 8 characters: **OS** (1) + **Environment** (2) + **Country** (3–5) + **Node** (6–8). "
    "Example: `AIGER789` → AIX | Integration | Germany | Node 789"
)

c1, c2, c3, c4 = st.columns(4)
c1.metric("Total hosts", f"{len(df):,}")
c2.metric("Top OS", df["os"].mode()[0])
c3.metric("Top environment", df["environment"].mode()[0])
c4.metric("Top country", df["country"].mode()[0])

tab_data, tab_charts, tab_decode, tab_rules = st.tabs(
    ["📋 Data", "📊 Charts", "🔍 Decode a hostname", "📐 Rules"])

# ---------------- Data ----------------
with tab_data:
    f1, f2, f3 = st.columns(3)
    os_f = f1.multiselect("OS", sorted(df["os"].unique()))
    env_f = f2.multiselect("Environment", sorted(df["environment"].unique()))
    ctry_f = f3.multiselect("Country", sorted(df["country"].unique()))
    view = df
    if os_f:
        view = view[view["os"].isin(os_f)]
    if env_f:
        view = view[view["environment"].isin(env_f)]
    if ctry_f:
        view = view[view["country"].isin(ctry_f)]
    st.caption(f"Showing {len(view):,} of {len(df):,} hosts")
    st.dataframe(view, width="stretch", hide_index=True, height=420)
    st.download_button("⬇️ Download hosts.csv", view.to_csv(index=False).encode(),
                       "hosts.csv", "text/csv")

# ---------------- Charts ----------------
with tab_charts:
    st.subheader("Distribution of Hosts by Country and Environment")
    fig, ax = plt.subplots(figsize=(14, 6))
    env_by_country = df.groupby(["country", "environment"]).size().unstack()
    env_by_country.plot(kind="bar", color=ENV_COLORS, edgecolor="white", ax=ax)
    ax.set_xlabel("")
    ax.set_ylabel("Number of Hosts", fontweight="bold")
    ax.tick_params(axis="x", rotation=45)
    ax.legend(title="Environment", shadow=True)
    ax.grid(axis="y", alpha=0.5, linestyle="--")
    fig.tight_layout()
    st.pyplot(fig)

    col_a, col_b = st.columns(2)
    with col_a:
        st.subheader("Operating Systems by Country")
        fig, ax = plt.subplots(figsize=(8, 6))
        df.groupby(["country", "os"]).size().unstack().plot(
            kind="barh", stacked=True, color=OS_COLORS, edgecolor="white", ax=ax)
        ax.set_xlabel("Number of hosts", fontweight="bold")
        ax.set_ylabel("")
        ax.legend(title="Operating System", shadow=True)
        ax.grid(axis="x", alpha=0.5)
        fig.tight_layout()
        st.pyplot(fig)

        st.subheader("Hosts by Country")
        counts = df["country"].value_counts().reset_index()
        counts.columns = ["country", "count"]
        fig, ax = plt.subplots(figsize=(8, 6))
        sns.barplot(data=counts, y="country", x="count", hue="country",
                    legend=False, palette="rocket", ax=ax)
        for i, v in enumerate(counts["count"]):
            ax.text(v + 5, i, str(v), va="center", fontweight="bold")
        ax.set_xlim(0, counts["count"].max() * 1.12)
        ax.set_xlabel("Number of hosts", fontweight="bold")
        ax.set_ylabel("")
        ax.grid(axis="x", alpha=0.5)
        fig.tight_layout()
        st.pyplot(fig)

    with col_b:
        st.subheader("Total Operating Systems")
        os_counts = df.groupby("os").size()
        fig, ax = plt.subplots(figsize=(8, 6))
        os_counts.plot(kind="pie", autopct="%1.1f%%", ax=ax, startangle=90, shadow=True,
                       colors=[OS_COLORS[o] for o in os_counts.index],
                       wedgeprops={"edgecolor": "white", "linewidth": 2},
                       textprops={"fontsize": 10, "fontweight": "bold"})
        ax.set_ylabel("")
        fig.tight_layout()
        st.pyplot(fig)

        st.subheader("Hosts by Environment and Country")
        fig, ax = plt.subplots(figsize=(8, 6))
        df.groupby(["country", "environment"]).size().unstack(0).plot(
            kind="bar", color=COUNTRY_COLORS, edgecolor="white", ax=ax)
        ax.set_xlabel("")
        ax.set_ylabel("Number of hosts", fontweight="bold")
        ax.tick_params(axis="x", rotation=0)
        ax.legend(title="Country", shadow=True)
        ax.grid(axis="y", alpha=0.5)
        fig.tight_layout()
        st.pyplot(fig)

    st.subheader("Expected vs. observed (%)")
    rows = []
    for col, codes in [("os", hn.OS_CODES), ("environment", hn.ENV_CODES),
                       ("country", hn.COUNTRY_CODES)]:
        obs = df[col].value_counts(normalize=True) * 100
        for name, weight in codes.values():
            rows.append({"Component": col, "Value": name, "Expected %": weight,
                         "Observed %": round(obs.get(name, 0), 1)})
    st.dataframe(rows, width="stretch", hide_index=True)

# ---------------- Decode ----------------
with tab_decode:
    hostname = st.text_input("Enter a hostname", "AIGER789", max_chars=8).upper().strip()
    if hostname:
        if hn.is_valid(hostname):
            d = hn.decode(hostname)
            k1, k2, k3, k4 = st.columns(4)
            k1.metric("OS", d["os"])
            k2.metric("Environment", d["environment"])
            k3.metric("Country", d["country"])
            k4.metric("Node", f"{d['node']:03d}")
            found = df[df["hostname"] == hostname]
            st.info(f"This hostname appears {len(found)} time(s) in the current dataset.")
        else:
            st.error("Invalid hostname. Format: OS + Environment + Country + Node (e.g. LPIRL001).")

# ---------------- Rules ----------------
with tab_rules:
    st.markdown("""
| Position | Component | Codes | Probability |
|---|---|---|---|
| 1 | OS | L (Linux), S (Solaris), A (AIX), H (HP-UX) | 40%, 30%, 20%, 10% |
| 2 | Environment | D (Dev), I (Integration), T (Testing), S (Staging), P (Production) | 10%, 10%, 25%, 25%, 30% |
| 3–5 | Country | NOR, FRA, ITA, ESP, GER, IRL | 6%, 9%, 16%, 16%, 23%, 30% |
| 6–8 | Node | 001–999 | Uniform |
""")
