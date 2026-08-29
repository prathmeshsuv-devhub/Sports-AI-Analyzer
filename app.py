import streamlit as st
import pandas as pd
import plotly.express as px

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Sports AI Analyzer",
    page_icon="🏆",
    layout="wide"
)

# =========================================================
# TITLE
# =========================================================

st.title("🏆 Sports AI Analyzer")
st.write("Sports Player Performance Analytics Dashboard")

# =========================================================
# UPLOAD SPORTS DATA
# =========================================================

st.header("📊 Sports Data")

uploaded_file = st.file_uploader(
    "Upload Sports Data",
    type=["csv", "xlsx"]
)

if uploaded_file is None:

    st.info("👆 Upload your CSV or Excel file to start.")

    st.stop()


# =========================================================
# READ FILE
# =========================================================

try:

    if uploaded_file.name.lower().endswith(".csv"):
        df = pd.read_csv(uploaded_file)

    else:
        df = pd.read_excel(uploaded_file)

except Exception as e:

    st.error(f"❌ Error reading file: {e}")

    st.stop()


st.success("✅ Sports data uploaded successfully!")


# =========================================================
# DISPLAY SPORTS DATA
# =========================================================

st.subheader("📋 Uploaded Sports Data")

st.dataframe(
    df,
    use_container_width=True
)


# =========================================================
# REQUIRED COLUMNS
# =========================================================

required_columns = [
    "Player",
    "Runs",
    "Goals",
    "Assists",
    "Pass_Accuracy",
    "Fitness"
]

missing_columns = [
    column
    for column in required_columns
    if column not in df.columns
]

if missing_columns:

    st.error(
        "❌ Missing columns: "
        + ", ".join(missing_columns)
    )

    st.info(
        "Required columns: "
        + ", ".join(required_columns)
    )

    st.stop()


# =========================================================
# CLEAN DATA
# =========================================================

numeric_columns = [
    "Runs",
    "Goals",
    "Assists",
    "Pass_Accuracy",
    "Fitness"
]

for column in numeric_columns:

    df[column] = pd.to_numeric(
        df[column],
        errors="coerce"
    )

df = df.dropna(
    subset=["Player"]
)

df[numeric_columns] = (
    df[numeric_columns]
    .fillna(0)
)


# =========================================================
# PERFORMANCE SCORE
# =========================================================

df["Performance Score"] = (

    df["Runs"].rank(pct=True) * 30

    + df["Goals"].rank(pct=True) * 25

    + df["Assists"].rank(pct=True) * 15

    + df["Pass_Accuracy"].rank(pct=True) * 15

    + df["Fitness"].rank(pct=True) * 15

)

df["Performance Score"] = (
    df["Performance Score"]
    .round(2)
)


# =========================================================
# PLAYER PERFORMANCE SCORES
# =========================================================

st.header("🏆 Player Performance Scores")

score_df = df[
    [
        "Player",
        "Runs",
        "Goals",
        "Assists",
        "Pass_Accuracy",
        "Fitness",
        "Performance Score"
    ]
].sort_values(
    "Performance Score",
    ascending=False
)

st.dataframe(
    score_df,
    use_container_width=True
)


# =========================================================
# TOP PERFORMER
# =========================================================

top_player = score_df.iloc[0]

st.success(
    f"🏆 Top Performer: {top_player['Player']} | "
    f"Score: {top_player['Performance Score']}/100"
)


# =========================================================
# OVERALL PERFORMANCE CHART
# =========================================================

st.header("📈 Overall Player Performance")

performance_chart = px.bar(
    score_df,
    x="Player",
    y="Performance Score",
    title="Overall Player Performance Score"
)

st.plotly_chart(
    performance_chart,
    use_container_width=True
)

# =========================================================
# ADVANCED PERFORMANCE CHARTS
# =========================================================

st.header("📊 Advanced Performance Charts")

chart_metric = st.selectbox(
    "Select Performance Metric",
    [
        "Runs",
        "Goals",
        "Assists",
        "Pass_Accuracy",
        "Fitness",
        "Performance Score"
    ],
    key="advanced_chart_metric"
)

metric_chart = px.bar(
    score_df,
    x="Player",
    y=chart_metric,
    title=f"{chart_metric} - Player Comparison"
)

st.plotly_chart(
    metric_chart,
    use_container_width=True
)
# =========================================================
# PLAYER COMPARISON
# =========================================================

st.header("🆚 Player Comparison")

player_list = score_df["Player"].tolist()

if len(player_list) < 2:

    st.warning(
        "⚠️ At least 2 players are required for comparison."
    )

else:

    # -----------------------------------------------------
    # SELECT TWO PLAYERS
    # -----------------------------------------------------

    col1, col2 = st.columns(2)

    with col1:

        player_a = st.selectbox(
            "👤 Select Player 1",
            player_list,
            key="player_comparison_1"
        )

    with col2:

        player_b = st.selectbox(
            "👤 Select Player 2",
            player_list,
            index=1,
            key="player_comparison_2"
        )


    # -----------------------------------------------------
    # GET PLAYER DATA
    # -----------------------------------------------------

    player_a_data = score_df[
        score_df["Player"] == player_a
    ].iloc[0]

    player_b_data = score_df[
        score_df["Player"] == player_b
    ].iloc[0]


    # =====================================================
    # INDIVIDUAL PLAYER PERFORMANCE
    # =====================================================

    st.subheader("👤 Individual Player Performance")


    # -----------------------------------------------------
    # PLAYER 1
    # -----------------------------------------------------

    st.markdown(f"### 🔵 {player_a}")

    a1, a2, a3, a4, a5, a6 = st.columns(6)

    with a1:

        st.metric(
            "Performance Score",
            f"{player_a_data['Performance Score']:.2f}"
        )

    with a2:

        st.metric(
            "Runs",
            f"{player_a_data['Runs']:.0f}"
        )

    with a3:

        st.metric(
            "Goals",
            f"{player_a_data['Goals']:.0f}"
        )

    with a4:

        st.metric(
            "Assists",
            f"{player_a_data['Assists']:.0f}"
        )

    with a5:

        st.metric(
            "Pass Accuracy",
            f"{player_a_data['Pass_Accuracy']:.1f}%"
        )

    with a6:

        st.metric(
            "Fitness",
            f"{player_a_data['Fitness']:.1f}%"
        )


    # -----------------------------------------------------
    # PLAYER 1 CHART
    # -----------------------------------------------------

    player_a_chart_df = pd.DataFrame({

        "Metric": [
            "Runs",
            "Goals",
            "Assists",
            "Pass Accuracy",
            "Fitness",
            "Performance Score"
        ],

        "Value": [

            player_a_data["Runs"],
            player_a_data["Goals"],
            player_a_data["Assists"],
            player_a_data["Pass_Accuracy"],
            player_a_data["Fitness"],
            player_a_data["Performance Score"]

        ]
    })

    chart_a = px.bar(
        player_a_chart_df,
        x="Metric",
        y="Value",
        title=f"{player_a} - Individual Performance"
    )

    st.plotly_chart(
        chart_a,
        use_container_width=True
    )


    # -----------------------------------------------------
    # PLAYER 2
    # -----------------------------------------------------

    st.markdown(f"### 🟢 {player_b}")

    b1, b2, b3, b4, b5, b6 = st.columns(6)

    with b1:

        st.metric(
            "Performance Score",
            f"{player_b_data['Performance Score']:.2f}"
        )

    with b2:

        st.metric(
            "Runs",
            f"{player_b_data['Runs']:.0f}"
        )

    with b3:

        st.metric(
            "Goals",
            f"{player_b_data['Goals']:.0f}"
        )

    with b4:

        st.metric(
            "Assists",
            f"{player_b_data['Assists']:.0f}"
        )

    with b5:

        st.metric(
            "Pass Accuracy",
            f"{player_b_data['Pass_Accuracy']:.1f}%"
        )

    with b6:

        st.metric(
            "Fitness",
            f"{player_b_data['Fitness']:.1f}%"
        )


    # -----------------------------------------------------
    # PLAYER 2 CHART
    # -----------------------------------------------------

    player_b_chart_df = pd.DataFrame({

        "Metric": [
            "Runs",
            "Goals",
            "Assists",
            "Pass Accuracy",
            "Fitness",
            "Performance Score"
        ],

        "Value": [

            player_b_data["Runs"],
            player_b_data["Goals"],
            player_b_data["Assists"],
            player_b_data["Pass_Accuracy"],
            player_b_data["Fitness"],
            player_b_data["Performance Score"]

        ]
    })

    chart_b = px.bar(
        player_b_chart_df,
        x="Metric",
        y="Value",
        title=f"{player_b} - Individual Performance"
    )

    st.plotly_chart(
        chart_b,
        use_container_width=True
    )


    # =====================================================
    # SIDE-BY-SIDE COMPARISON
    # =====================================================

    st.subheader(
        f"📊 {player_a} vs {player_b}"
    )

    comparison_df = pd.DataFrame({

        "Metric": [
            "Runs",
            "Goals",
            "Assists",
            "Pass Accuracy",
            "Fitness",
            "Performance Score"
        ],

        player_a: [

            player_a_data["Runs"],
            player_a_data["Goals"],
            player_a_data["Assists"],
            player_a_data["Pass_Accuracy"],
            player_a_data["Fitness"],
            player_a_data["Performance Score"]

        ],

        player_b: [

            player_b_data["Runs"],
            player_b_data["Goals"],
            player_b_data["Assists"],
            player_b_data["Pass_Accuracy"],
            player_b_data["Fitness"],
            player_b_data["Performance Score"]

        ]
    })

    st.dataframe(
        comparison_df,
        use_container_width=True
    )


    # =====================================================
    # COMPARISON CHART
    # =====================================================

    comparison_chart_data = comparison_df.melt(
        id_vars="Metric",
        var_name="Player",
        value_name="Value"
    )

    comparison_chart = px.bar(
        comparison_chart_data,
        x="Metric",
        y="Value",
        color="Player",
        barmode="group",
        title=f"{player_a} vs {player_b} - Performance Comparison"
    )

    st.plotly_chart(
        comparison_chart,
        use_container_width=True
    )


    # =====================================================
    # BETTER PERFORMER
    # =====================================================

    st.subheader("🏆 Comparison Result")

    if (
        player_a_data["Performance Score"]
        >
        player_b_data["Performance Score"]
    ):

        st.success(
            f"🏆 Better Overall Performer: {player_a}"
        )

    elif (
        player_b_data["Performance Score"]
        >
        player_a_data["Performance Score"]
    ):

        st.success(
            f"🏆 Better Overall Performer: {player_b}"
        )

    else:

        st.info(
            "🤝 Both players have the same overall performance score."
        )

# =========================================================
# PLAYER PERFORMANCE REPORT
# =========================================================

st.header("📄 Player Performance Report")

report_player = st.selectbox(
    "Select Player for Report",
    score_df["Player"].tolist(),
    key="report_player"
)

report_data = score_df[
    score_df["Player"] == report_player
].iloc[0]

report_text = f"""
SPORTS AI ANALYZER
PLAYER PERFORMANCE REPORT
========================================

Player Name: {report_data['Player']}

Performance Metrics
----------------------------------------
Performance Score : {report_data['Performance Score']:.2f}/100
Runs              : {report_data['Runs']:.0f}
Goals             : {report_data['Goals']:.0f}
Assists           : {report_data['Assists']:.0f}
Pass Accuracy     : {report_data['Pass_Accuracy']:.1f}%
Fitness            : {report_data['Fitness']:.1f}%

Performance Summary
----------------------------------------
"""

if report_data["Performance Score"] >= 80:
    report_text += "Excellent overall performance."

elif report_data["Performance Score"] >= 60:
    report_text += "Good overall performance with room for improvement."

else:
    report_text += "The player has potential for improvement."


st.text_area(
    "📋 Report Preview",
    report_text,
    height=300
)

st.download_button(
    "⬇️ Download Player Performance Report",
    data=report_text,
    file_name=f"{report_player}_Performance_Report.txt",
    mime="text/plain"
)
# =========================================================
# =========================================================
# REAL AI PLAYER ANALYSIS
# =========================================================

from openai import OpenAI

st.header("🤖 AI Player Analysis")

selected_player = st.selectbox(
    "Select a Player",
    score_df["Player"].tolist(),
    key="ai_player"
)

selected_data = score_df[
    score_df["Player"] == selected_player
].iloc[0]

st.subheader(
    f"📋 {selected_player} Performance"
)

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric(
        "Performance Score",
        f"{selected_data['Performance Score']:.2f}/100"
    )

with c2:
    st.metric(
        "Runs",
        f"{selected_data['Runs']:.0f}"
    )

with c3:
    st.metric(
        "Goals",
        f"{selected_data['Goals']:.0f}"
    )

with c4:
    st.metric(
        "Fitness",
        f"{selected_data['Fitness']:.1f}%"
    )

if st.button(
    "🤖 Generate AI Analysis",
    key="generate_ai_analysis"
):

    try:

        client = OpenAI(
            api_key=st.secrets["OPENAI_API_KEY"]
        )

        prompt = f"""
Analyze this sports player's performance:

Player: {selected_player}
Runs: {selected_data['Runs']}
Goals: {selected_data['Goals']}
Assists: {selected_data['Assists']}
Pass Accuracy: {selected_data['Pass_Accuracy']}%
Fitness: {selected_data['Fitness']}%
Performance Score: {selected_data['Performance Score']}/100

Give a clear professional analysis with:

1. Overall Performance
2. Strengths
3. Areas for Improvement
4. Recommendation
"""

        with st.spinner(
            "🤖 AI is analyzing the player..."
        ):

            response = client.responses.create(
                model="gpt-5-mini",
                input=prompt
            )

        st.subheader("🤖 AI Performance Analysis")

        st.write(response.output_text)

    except Exception as e:

        st.error(
            f"❌ AI Analysis Error: {e}"
        )

# =========================================================
# FOOTER
# =========================================================

st.markdown("---")

st.caption(
    "🏆 Sports AI Analyzer | Player Performance Analytics"
)