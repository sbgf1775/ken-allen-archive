
import streamlit as st
import pandas as pd
import os
import random
from datetime import datetime
from pyvis.network import Network
import streamlit.components.v1 as components
import plotly.express as px
import plotly.graph_objects as go
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from collections import Counter
import re
import itertools

st.set_page_config(page_title="Ken Allen Archive", page_icon="🗂️", layout="wide")

@st.cache_data(ttl=0)
def load_data():
    if os.path.exists("ken_allen_scored.csv"):
        df = pd.read_csv("ken_allen_scored.csv")
        if "year" in df.columns:
            df["year"] = pd.to_numeric(df["year"], errors="coerce")
        return df
    return pd.DataFrame()

df = load_data()

# --- Header ---
header_col, spacer_col, logo_col = st.columns([5, 1, 1])
with header_col:
    st.title("🗂️ Ken Allen Archive")
    st.markdown(f"**Samuel B. Griffith Foundation for Chinese Military Studies** © {datetime.now().year}")
with logo_col:
    if os.path.exists("/Users/workspace/sbgf_logo.webp"):
        st.markdown("<br>", unsafe_allow_html=True)
        st.image("/Users/workspace/sbgf_logo.webp", width=80)
st.divider()

# --- Bio Section ---
col_photo, col_bio = st.columns([1, 3], gap="large")
with col_photo:
    if os.path.exists("/Users/workspace/ken_allen_photo.webp"):
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.image("/Users/workspace/ken_allen_photo.webp", use_container_width=True, caption="Kenneth W. Allen")
with col_bio:
    st.subheader("About Kenneth W. Allen")
    st.markdown("""
Kenneth W. Allen is a leading China military analyst whose work has profoundly shaped Western
understanding of the People's Liberation Army (PLA), particularly the PLA Air Force (PLAAF).
Over a career spanning nearly five decades, he has become widely regarded as one of the premier
authorities on Chinese airpower, personnel systems, and military organization. He is currently
**Advisor Emeritus** at the Samuel B. Griffith Foundation for Chinese Military Studies.

A retired U.S. Air Force officer, Allen served 21 years as a linguist and intelligence officer,
including a tour as Assistant Air Force Attaché in Beijing from 1987 to 1989. After leaving active
duty, he held senior analytical positions at the Center for Naval Analyses, Defense Group Inc.,
and the U.S. Air Force's China Aerospace Studies Institute (CASI), where he most recently served
as Director of Research.

Allen has authored or coauthored numerous influential studies, including *70 Years of the
People's Liberation Army Air Force*, a major 2022 report on PLA personnel for the U.S.-China
Economic and Security Review Commission, and most recently *The People's Liberation Army as
Organization, Volume 3.0* (2025). He holds BAs from the University of California, Davis and
the University of Maryland, and an MA in international relations from Boston University.
""")

st.divider()
st.markdown("Search and explore Kenneth Allen's corpus of PLA research, reports, and analysis.")
st.divider()

if df.empty:
    st.warning("Index not yet available.")
    st.stop()

# --- Filter out drafts ---
if "is_draft" in df.columns:
    df_filtered = df[df["is_draft"] == False].copy()
else:
    df_filtered = df.copy()

df_filtered["year"] = pd.to_numeric(df_filtered["year"], errors="coerce")

# --- Sidebar ---
st.sidebar.markdown(f"**Total documents in archive:** {len(df)}")
if "is_draft" in df.columns:
    st.sidebar.markdown(f"**Publicly available documents:** {int(len(df) - df['is_draft'].sum())}")

# --- Mode ---
mode = st.radio("Select mode:", ["🔍 Search", "📚 Browse", "📊 Insights & Network"], horizontal=True)
st.divider()

# --- Topic colors (shared across all modes) ---
topic_colors_plotly = {
    "PLAAF":        "#1f77b4",
    "PLAN":         "#2ca02c",
    "PLAAF/GF":     "#8c564b",
    "Organization": "#9467bd",
    "Personnel":    "#e377c2",
    "Doctrine":     "#d62728",
    "Diplomacy":    "#ff7f0e",
    "Technology":   "#17becf",
    "Leadership":   "#bcbd22",
    "Cross-Domain": "#7f7f7f",
}

topic_colors_net = {
    "PLAAF":        "#1f77b4",
    "PLAN":         "#2ca02c",
    "PLAAF/GF":     "#8c564b",
    "Organization": "#9467bd",
    "Personnel":    "#e377c2",
    "Doctrine":     "#d62728",
    "Diplomacy":    "#ff7f0e",
    "Technology":   "#17becf",
    "Leadership":   "#bcbd22",
    "Cross-Domain": "#7f7f7f",
}

def drive_link(file_id):
    return f"https://drive.google.com/file/d/{file_id}/view"

def render_result(row, show_relevance=False, relevance=None):
    header = f"📄 {row['filename']}  |  {row['folder']}"
    if show_relevance and relevance:
        header += f"  |  relevance: {relevance}"
    with st.expander(header):
        col1, col2, col3 = st.columns(3)
        col1.markdown(f"**Topic:** {row['dominant_topic']}")
        col2.markdown(f"**Sentiment:** {row['sentiment']:.2f}")
        col3.markdown(f"**Keywords:** {row['top_keywords']}")
        st.markdown("**Snippet:**")
        st.markdown(f"> {str(row['text_snippet'])[:1500]}")
        st.markdown("---")
        if row.get("file_id"):
            st.link_button("📂 View original in Google Drive", drive_link(row["file_id"]))

# PLA stopwords for keyword analysis
pla_stopwords = {
    "also", "would", "could", "said", "from", "that", "this", "with",
    "have", "been", "were", "their", "they", "which", "more", "other",
    "into", "than", "will", "upon", "about", "after", "under", "over",
    "such", "each", "both", "when", "year", "time", "number", "total",
    "include", "including", "however", "therefore", "although", "while",
    "since", "where", "there", "here", "these", "those", "some", "many",
    "first", "second", "third", "used", "using", "based", "well", "make",
    "made", "take", "taken", "part", "report", "reports", "paper", "papers",
    "article", "section", "chapter", "page", "data", "information", "notes",
    "https", "http", "html", "website", "june", "july", "january", "february",
    "march", "april", "august", "september", "october", "november", "december",
    "china", "chinese", "military", "pla", "force", "forces", "army",
    "people", "national", "government", "countries", "country", "world",
    "international", "foreign", "defense", "security", "policy", "level",
    "senior", "system", "systems", "program", "programs", "unit", "units",
    "number", "general", "major", "support", "work", "works", "area",
    "areas", "related", "within", "between", "through", "during", "across",
    "rforce", "naairforce", "chinaairforce", "chinaa", "lnaa", "inaa",
    "jswj", "gfbw", "cmbs", "nids", "issn", "kbol", "edefe", "wang",
    "mark", "sina", "baidu", "baike", "ralston", "text", "version",
    "cover", "english", "white", "staff", "chief", "civil", "power",
    "strategic", "joint", "strategy", "operations", "warfare", "taiwan",
    "current", "recent", "role", "roles", "office", "offices", "various"
}

# ============================================================
# SEARCH MODE
# ============================================================
if mode == "🔍 Search":
    st.subheader("Search the Archive")

    search_suggestions = [
        "PLAAF pilot training", "military diplomacy", "PLA force reductions",
        "naval aviation", "CMC leadership", "officer recruitment",
        "PLA doctrine reform", "PLAN submarine", "airborne operations",
        "Taiwan Strait", "Xi Jinping military", "PLA academic institutions",
        "military exchanges", "PLAAF bomber", "NCO program",
        "joint operations", "PLA logistics", "3-star promotions",
        "defense white paper", "military personnel policy",
        "PLAAF organization", "China military diplomacy 2023",
        "PLA ground forces", "Second Artillery", "strategic support force",
    ]

    if "search_placeholder" not in st.session_state:
        picks = random.sample(search_suggestions, 2)
        st.session_state.search_placeholder = f"e.g. {picks[0]}, {picks[1]}..."

    query = st.text_input("Enter search terms", placeholder=st.session_state.search_placeholder)

    if not query:
        st.info("Enter a search term above to find relevant documents.")
        st.stop()

    query_terms = query.lower().split()

    def relevance_score(row):
        text = " ".join([
            str(row.get("filename", "")),
            str(row.get("text_snippet", "")),
            str(row.get("top_keywords", ""))
        ]).lower()
        return sum(text.count(term) for term in query_terms)

    df_filtered["relevance"] = df_filtered.apply(relevance_score, axis=1)
    results = df_filtered[df_filtered["relevance"] > 0].sort_values("relevance", ascending=False)

    col1, col2, col3 = st.columns(3)
    col1.metric("Results Found", len(results))
    col2.metric("Folders Covered", results["folder"].nunique() if len(results) > 0 else 0)
    col3.metric("Top Topic", results["dominant_topic"].mode()[0] if len(results) > 0 else "N/A")
    st.divider()

    if len(results) == 0:
        st.warning("No documents matched your search. Try different keywords.")
    else:
        st.markdown(f"**Top {min(25, len(results))} results — ranked by relevance**")
        for _, row in results.head(25).iterrows():
            render_result(row, show_relevance=True, relevance=int(row["relevance"]))

# ============================================================
# BROWSE MODE
# ============================================================
elif mode == "📚 Browse":
    st.subheader("Browse the Archive")

    st.sidebar.markdown("---")
    st.sidebar.markdown("**Browse Filters**")

    all_folders = sorted(df_filtered["folder"].unique().tolist())
    selected_folder = st.sidebar.selectbox("Subject Folder", ["All folders"] + all_folders)

    all_topics = sorted(df_filtered["dominant_topic"].unique().tolist())
    selected_topic = st.sidebar.selectbox("PLA Topic", ["All topics"] + all_topics)

    st.sidebar.markdown("**Publication Year**")
    st.sidebar.markdown("*Year is extracted from the document filename where available. For documents covering a range of years, the most recent year is used.*")
    year_range = st.sidebar.slider("Year range", 1981, 2024, (1981, 2024), 1)
    filter_by_year = st.sidebar.toggle("Apply year filter", value=False)

    browsed = df_filtered.copy()
    browsed["year"] = pd.to_numeric(browsed["year"], errors="coerce")

    if selected_folder != "All folders":
        browsed = browsed[browsed["folder"] == selected_folder]
    if selected_topic != "All topics":
        browsed = browsed[browsed["dominant_topic"] == selected_topic]
    if filter_by_year:
        browsed = browsed[
            (browsed["year"].isna()) |
            ((browsed["year"] >= year_range[0]) & (browsed["year"] <= year_range[1]))
        ]

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Documents", len(browsed))
    col2.metric("Folders", browsed["folder"].nunique())
    col3.metric("Avg Sentiment", f"{browsed['sentiment'].mean():.2f}" if len(browsed) > 0 else "N/A")
    col4.metric("Top Topic", browsed["dominant_topic"].mode()[0] if len(browsed) > 0 else "N/A")
    st.divider()

    if len(browsed) > 0:
        st.subheader("Topic Distribution")
        topic_counts = browsed["dominant_topic"].value_counts().reset_index()
        topic_counts.columns = ["Topic", "Count"]
        st.bar_chart(topic_counts.set_index("Topic"))
        st.divider()

    if selected_folder == "All folders" and len(browsed) > 0:
        st.subheader("Documents by Folder")
        folder_counts = browsed["folder"].value_counts().reset_index()
        folder_counts.columns = ["Folder", "Count"]
        st.dataframe(folder_counts, use_container_width=True, hide_index=True)
        st.divider()

    st.subheader(f"Documents ({len(browsed)})")
    if len(browsed) == 0:
        st.info("No documents match the selected filters.")
    else:
        for _, row in browsed.head(50).iterrows():
            render_result(row)
        if len(browsed) > 50:
            st.info(f"Showing 50 of {len(browsed)}. Use filters to narrow down.")

# ============================================================
# INSIGHTS & NETWORK MODE
# ============================================================
elif mode == "📊 Insights & Network":

    insight_tab, network_tab = st.tabs(["📊 Analytics", "🕸️ Network Graph"])

    # ============================================================
    # ANALYTICS TAB
    # ============================================================
    with insight_tab:
        st.subheader("Archive Analytics")
        st.markdown("This section uses computational methods to extract patterns and insights from Kenneth Allen's full corpus of 943 publicly available documents. The visualizations below reveal how his research focus has shifted over time, which topics dominate specific subject areas, and how the archive is structured as a whole. Together, they offer a data-driven portrait of one of the most comprehensive bodies of open-source PLA research ever assembled.")
        st.divider()

        df_analytics = df_filtered.copy()
        df_analytics["year"] = pd.to_numeric(df_analytics["year"], errors="coerce")

        # ---- CHART 1: Research Focus Over Time ----
        st.markdown("### 📅 Research Focus Over Time")
        st.markdown("""
This stacked area chart shows how the volume and topic composition of Kenneth Allen's research output has changed from 1991 through 2024.
Each colored band represents a different PLA research topic, and the height of each band in a given year reflects how many documents
were classified under that topic that year. A wider band means more documents; a narrower band means fewer.
**How to read it:** Hover your cursor over any colored area to see the topic name, year, and document count.
Look for years where one color dominates — those represent periods of concentrated research focus.
The dramatic rise after 2015 reflects the post-reform period of PLA organizational restructuring that Ken Allen tracked closely.
Note: 502 of 943 documents have a detectable publication year; the remainder are undated and not shown here.
        """)

        df_time = df_analytics[df_analytics["year"].notna()].copy()
        df_time["year"] = df_time["year"].astype(int)
        df_time = df_time[df_time["year"] >= 1990]

        if len(df_time) >= 5:
            pivot = df_time.groupby(["year", "dominant_topic"]).size().reset_index(name="count")
            all_years = range(df_time["year"].min(), df_time["year"].max() + 1)
            all_topics_list = list(topic_colors_plotly.keys())
            full_index = pd.DataFrame(
                list(itertools.product(all_years, all_topics_list)),
                columns=["year", "dominant_topic"]
            )
            pivot_full = full_index.merge(pivot, on=["year", "dominant_topic"], how="left").fillna(0)

            fig_area = go.Figure()
            for topic in all_topics_list:
                topic_data = pivot_full[pivot_full["dominant_topic"] == topic]
                fig_area.add_trace(go.Scatter(
                    x=topic_data["year"],
                    y=topic_data["count"],
                    name=topic,
                    mode="lines",
                    stackgroup="one",
                    fillcolor=topic_colors_plotly.get(topic, "#7f7f7f"),
                    line=dict(color=topic_colors_plotly.get(topic, "#7f7f7f"), width=0.5),
                    hovertemplate="<b>%{fullData.name}</b><br>Year: %{x}<br>Documents: %{y}<extra></extra>"
                ))

            fig_area.update_layout(
                height=600,
                plot_bgcolor="#0e1117",
                paper_bgcolor="#0e1117",
                font=dict(color="white", size=13),
                hovermode="closest",
                legend=dict(
                    title=dict(text="Research Topic", font=dict(color="white", size=13)),
                    font=dict(color="white", size=12),
                    orientation="h",
                    yanchor="bottom",
                    y=1.02,
                    xanchor="right",
                    x=1
                ),
                xaxis=dict(
                    title=dict(text="Year", font=dict(color="white", size=13)),
                    color="white",
                    showgrid=False,
                    dtick=2,
                    tickfont=dict(color="white", size=11)
                ),
                yaxis=dict(
                    title=dict(text="Documents Published", font=dict(color="white", size=13)),
                    color="white",
                    showgrid=True,
                    gridcolor="#2a2a2a",
                    tickfont=dict(color="white", size=11)
                )
            )
            st.plotly_chart(fig_area, use_container_width=True)

            col1, col2, col3, col4 = st.columns(4)
            yearly_totals = df_time.groupby("year").size()
            peak_year = int(yearly_totals.idxmax())
            peak_count = int(yearly_totals.max())
            top_topic = df_analytics["dominant_topic"].value_counts().index[0]
            top_pct = round(df_analytics["dominant_topic"].value_counts().iloc[0] / len(df_analytics) * 100, 1)
            col1.metric("Most Productive Year", str(peak_year), f"{peak_count} docs")
            col2.metric("Dominant Research Focus", top_topic, f"{top_pct}% of corpus")
            col3.metric("Years Covered", f"{df_time['year'].min()}–{df_time['year'].max()}")
            col4.metric("Dated Documents", f"{len(df_time)} of {len(df_analytics)}")
        else:
            st.warning("Not enough dated documents to render timeline.")

        st.divider()

        # ---- CHART 2: Top Keywords by Topic ----
        st.markdown("### 🔑 Top Keywords by Research Topic")
        st.markdown("""
This horizontal bar chart shows the most frequently occurring substantive keywords within each of Ken Allen's ten research topic categories.
Select a topic from the dropdown to see which terms appear most often across the documents classified under that subject area.
**How to read it:** Longer bars indicate higher keyword frequency. These terms are drawn from the NLP-extracted keyword field of each document,
filtered through a curated stopword list that removes generic terms like 'China,' 'military,' and 'force' to surface analytically distinctive vocabulary.
For example, selecting **Diplomacy** will show terms like 'exchanges,' 'exercises,' 'bilateral,' and 'peacekeeping' — the actual substance of Allen's diplomatic writing.
        """)

        kw_col1, kw_col2 = st.columns([1, 3])
        with kw_col1:
            selected_kw_topic = st.selectbox(
                "Select research topic:",
                list(topic_colors_plotly.keys()),
                key="kw_topic_select"
            )

        topic_df = df_analytics[df_analytics["dominant_topic"] == selected_kw_topic]
        kw_counter = Counter()
        for kw_string in topic_df["top_keywords"].dropna():
            for kw in str(kw_string).split(","):
                kw = kw.strip().lower()
                if len(kw) > 3 and kw not in pla_stopwords:
                    kw_counter[kw] += 1

        if len(kw_counter) >= 5:
            top_kws = kw_counter.most_common(20)
            kw_df = pd.DataFrame(top_kws, columns=["keyword", "count"]).sort_values("count")
            color = topic_colors_plotly.get(selected_kw_topic, "#7f7f7f")

            fig_kw = px.bar(
                kw_df,
                x="count",
                y="keyword",
                orientation="h",
                labels={"count": "Frequency", "keyword": ""},
                height=650,
                color_discrete_sequence=[color]
            )
            fig_kw.update_layout(
                plot_bgcolor="#0e1117",
                paper_bgcolor="#0e1117",
                font=dict(color="white", size=13),
                xaxis=dict(showgrid=True, gridcolor="#2a2a2a", color="white",
                           title=dict(text="Frequency", font=dict(color="white", size=13)),
                           tickfont=dict(color="white", size=12)),
                yaxis=dict(showgrid=False, color="white",
                           tickfont=dict(size=13, color="white")),
                showlegend=False,
                title=dict(
                    text=f"Top 20 Keywords — {selected_kw_topic} ({len(topic_df)} documents)",
                    font=dict(color="white", size=15)
                )
            )
            with kw_col2:
                st.plotly_chart(fig_kw, use_container_width=True)
        else:
            with kw_col2:
                st.info("Not enough keyword data for this topic.")

        st.divider()

        # ---- CHART 3: Heatmap ----
        st.markdown("### 🔥 Topic Concentration by Subject Folder")
        st.markdown("""
This heatmap shows how research topics are distributed across Kenneth Allen's 24 subject folders.
Each row is a subject folder; each column is one of the ten PLA research topics.
The number in each cell represents what percentage of that folder's documents fall under that topic.
Darker blue cells indicate stronger topic concentration — meaning that folder is heavily focused on one subject area.
**How to read it:** A row that is mostly dark blue in one column represents a highly focused, topic-pure folder.
A row with moderate values spread across multiple columns represents a cross-domain folder covering several subjects.
For example, the 'PLAAF' folder is predictably dark blue under the PLAAF topic column.
The 'PLA Military Diplomacy Reports' folder shows concentration in Diplomacy but also touches Leadership and Organization —
reflecting the cross-domain nature of diplomatic engagement work.
        """)

        heat_df = df_analytics.groupby(["folder", "dominant_topic"]).size().reset_index(name="count")
        heat_pivot = heat_df.pivot(index="folder", columns="dominant_topic", values="count").fillna(0)
        heat_norm = heat_pivot.div(heat_pivot.sum(axis=1), axis=0) * 100
        folder_totals = df_analytics["folder"].value_counts()
        sorted_folders = [f for f in folder_totals.index if f in heat_norm.index]
        heat_norm = heat_norm.loc[sorted_folders]

        fig_heat = px.imshow(
            heat_norm,
            color_continuous_scale="Blues",
            aspect="auto",
            height=750,
            text_auto=".0f"
        )
        fig_heat.update_layout(
            plot_bgcolor="#0e1117",
            paper_bgcolor="#0e1117",
            font=dict(color="white", size=12),
            xaxis=dict(
                title=dict(text="Research Topic", font=dict(color="white", size=13, family="Arial Black")),
                color="white",
                tickangle=-35,
                tickfont=dict(size=12, color="white")
            ),
            yaxis=dict(
                title=dict(text="Subject Folder", font=dict(color="white", size=13)),
                color="white",
                tickfont=dict(size=11, color="white")
            ),
            coloraxis_colorbar=dict(
                title="% of Folder",
                tickfont=dict(color="white"),
            ),
            title=dict(
                text="Topic Concentration Heatmap — Subject Folder × Research Topic",
                font=dict(color="white", size=14)
            )
        )
        fig_heat.update_traces(textfont=dict(color="white", size=10))
        st.plotly_chart(fig_heat, use_container_width=True)

        st.divider()

        # ---- CHART 4: Treemap ----
        st.markdown("### 🗺️ Archive Structure — Treemap")
        st.markdown("""
This treemap gives you a bird's-eye view of the entire archive — all 943 publicly available documents — organized by folder and research topic simultaneously.
Each large outer rectangle represents one of Ken Allen's 24 subject folders. Inside each folder, smaller rectangles show how documents within that folder
are distributed across PLA research topics, with size proportional to document count. Colors match the topic color legend used throughout this app.
**How to read it:** Larger rectangles mean more documents. Click on any rectangle to zoom into that folder or topic.
Click the back button to zoom out. Hover over any cell to see the exact document count.
This visualization makes it immediately clear which folders are the largest, which topics dominate each folder,
and where Ken Allen's research has been most concentrated over his career.
        """)

        tree_df = df_analytics.groupby(["folder", "dominant_topic"]).size().reset_index(name="count")

        fig_tree = px.treemap(
            tree_df,
            path=["folder", "dominant_topic"],
            values="count",
            color="dominant_topic",
            color_discrete_map=topic_colors_plotly,
            height=750,
        )
        fig_tree.update_traces(
            textfont=dict(size=13, color="white"),
            hovertemplate="<b>%{label}</b><br>Documents: %{value}<br>Parent: %{parent}<extra></extra>",
            marker=dict(line=dict(width=1.5, color="#0e1117"))
        )
        fig_tree.update_layout(
            paper_bgcolor="#0e1117",
            font=dict(color="white", size=13),
            title=dict(
                text="Ken Allen Archive — Full Structure by Folder and Topic",
                font=dict(color="white", size=14)
            ),
            margin=dict(t=50, l=10, r=10, b=10)
        )
        st.plotly_chart(fig_tree, use_container_width=True)


        st.divider()

        # ---- CHART 5: Leadership Mentions Over Time ----
        st.markdown("### 👤 PLA Leadership Mentions Over Time")
        st.markdown("""
This chart tracks how frequently the names of key PLA and Chinese political leaders appear across Kenneth Allen\'s
dated documents, year by year. Each line represents one leader. A spike in a given year means Allen was writing
about or referencing that leader frequently — often coinciding with a promotion, policy announcement, military reform,
or significant event associated with that figure.

**How to read it:** Higher points on a line mean more document mentions that year. Leaders who appear consistently
across many years were central figures throughout Allen\'s research career. Leaders who spike briefly and then disappear
likely served during a specific period or were subjects of a focused study.

This visualization captures the evolution of PLA civil-military leadership as reflected through one analyst\'s
three-decade body of work — a unique lens on which figures dominated open-source PLA analysis at different moments in time.

**Tiers covered:** Top political leadership (General Secretaries), CMC senior members, and PLAAF commanders.
Use the multiselect below to customize which leaders are displayed.
        """)

        # Define leaders to track
        leaders = {
            # Political
            "Jiang Zemin":    ["Jiang Zemin", "Jiang"],
            "Hu Jintao":      ["Hu Jintao", "Hu Jintao"],
            "Xi Jinping":     ["Xi Jinping", "Xi Jinping"],
            # CMC / Senior Military
            "Liu Huaqing":    ["Liu Huaqing"],
            "Chi Haotian":    ["Chi Haotian"],
            "Xu Caihou":      ["Xu Caihou"],
            "Guo Boxiong":    ["Guo Boxiong"],
            "Fan Changlong":  ["Fan Changlong"],
            "Zhang Youxia":   ["Zhang Youxia"],
            "He Weidong":     ["He Weidong"],
            # PLAAF Commanders
            "Xu Qiliang":     ["Xu Qiliang"],
            "Ma Xiaotian":    ["Ma Xiaotian"],
            "Yi Xiaoguang":   ["Yi Xiaoguang"],
            "Chang Dingqiu":  ["Chang Dingqiu"],
            "Wang Hai":       ["Wang Hai"],
        }

        # Default selection
        default_leaders = ["Xi Jinping", "Hu Jintao", "Jiang Zemin", "Xu Qiliang", "Ma Xiaotian", "Xu Caihou"]

        selected_leaders = st.multiselect(
            "Select leaders to display:",
            options=list(leaders.keys()),
            default=default_leaders,
            key="leader_select"
        )

        # Build mention counts per leader per year
        df_lead = df_analytics[df_analytics["year"].notna()].copy()
        df_lead["year"] = df_lead["year"].astype(int)
        df_lead = df_lead[df_lead["year"] >= 1990]

        if len(df_lead) > 0 and selected_leaders:
            mention_records = []
            for _, row in df_lead.iterrows():
                snippet = str(row.get("text_snippet", "")) + " " + str(row.get("filename", ""))
                for leader_name in selected_leaders:
                    search_terms = leaders[leader_name]
                    count = sum(snippet.count(term) for term in search_terms)
                    if count > 0:
                        mention_records.append({
                            "year": int(row["year"]),
                            "leader": leader_name,
                            "mentions": count
                        })

            if mention_records:
                lead_df = pd.DataFrame(mention_records)
                lead_agg = lead_df.groupby(["year", "leader"])["mentions"].sum().reset_index()

                # Fill in zeros for missing year/leader combos
                all_lead_years = range(df_lead["year"].min(), df_lead["year"].max() + 1)
                full_lead_index = pd.DataFrame(
                    list(itertools.product(all_lead_years, selected_leaders)),
                    columns=["year", "leader"]
                )
                lead_full = full_lead_index.merge(lead_agg, on=["year", "leader"], how="left").fillna(0)

                fig_lead = px.line(
                    lead_full,
                    x="year",
                    y="mentions",
                    color="leader",
                    markers=True,
                    labels={"year": "Year", "mentions": "Document Mentions", "leader": "Leader"},
                    height=520,
                )
                fig_lead.update_layout(
                    plot_bgcolor="#0e1117",
                    paper_bgcolor="#0e1117",
                    font=dict(color="white", size=13),
                    hovermode="closest",
                    legend=dict(
                        title=dict(text="Leader", font=dict(color="white", size=13)),
                        font=dict(color="white", size=12),
                        orientation="v",
                        x=1.01,
                        y=1
                    ),
                    xaxis=dict(
                        title=dict(text="Year", font=dict(color="white", size=13)),
                        color="white",
                        showgrid=False,
                        dtick=2,
                        tickfont=dict(color="white", size=11)
                    ),
                    yaxis=dict(
                        title=dict(text="Document Mentions", font=dict(color="white", size=13)),
                        color="white",
                        showgrid=True,
                        gridcolor="#2a2a2a",
                        tickfont=dict(color="white", size=11)
                    )
                )
                st.plotly_chart(fig_lead, use_container_width=True)

                # Top mentioned leaders overall
                top_leaders = lead_df.groupby("leader")["mentions"].sum().sort_values(ascending=False)
                st.markdown("**Total mentions across all dated documents:**")
                cols = st.columns(len(selected_leaders) if len(selected_leaders) <= 5 else 5)
                for i, (leader, count) in enumerate(top_leaders.items()):
                    cols[i % 5].metric(leader, int(count))
            else:
                st.info("No mentions of selected leaders found in dated documents. Try different names.")
        else:
            st.info("Select at least one leader above.")


    # ============================================================
    # NETWORK GRAPH TAB
    # ============================================================
    with network_tab:
        st.subheader("Document Network Graph")
        st.markdown("""
This interactive network graph visualizes relationships between documents in Kenneth Allen's archive based on shared research vocabulary.
**Each dot (node)** represents one document, colored by its dominant PLA research topic.
**Each line (edge)** connects two documents that share a minimum number of keywords in common — meaning their subject matter overlaps in a measurable way.

**How to read it:** Clusters of tightly connected nodes indicate groups of documents that share similar vocabulary and likely cover related subject matter.
Isolated nodes at the edges of the graph represent documents with more unique content that doesn't overlap heavily with others.
Hover over any node to see the document title, topic, keywords, and a link to open it in Google Drive.

**Why only 150 documents?** Network graphs become computationally expensive and visually unreadable as the number of nodes grows.
With 943 documents, the sheer number of potential connections would render the graph as an unusable tangle of lines.
150 nodes is the practical limit for a readable, interactive visualization in a web browser.
For the best results, filter by a single research topic to see a focused, analytically meaningful sub-network.

**Minimum shared keywords:** This slider controls how many keywords two documents must share before a connecting line is drawn.
Setting it to 1 produces many connections including weak ones. Setting it to 3 or higher shows only the strongest,
most substantively related document pairs — a more analytically rigorous view.
        """)

        st.sidebar.markdown("---")
        st.sidebar.markdown("**Network Filters**")

        all_topics_net = sorted(df_filtered["dominant_topic"].unique().tolist())
        net_topic = st.sidebar.selectbox(
            "Filter by Research Topic",
            ["All topics"] + all_topics_net,
            key="net_topic",
            help="Select a single topic for the most readable and analytically useful graph. 'All topics' shows a cross-domain sample."
        )

        max_nodes = st.sidebar.slider("Max documents to show", 25, 150, 75, 25)
        min_shared = st.sidebar.slider("Min shared keywords to connect", 1, 4, 2, 1)
        st.sidebar.markdown("*Tip: Select a single topic and set min keywords to 2 or higher for the clearest graph.*")

        net_df = df_filtered.copy()
        if net_topic != "All topics":
            net_df = net_df[net_df["dominant_topic"] == net_topic]
        net_df = net_df.head(max_nodes).reset_index(drop=True)

        if len(net_df) < 2:
            st.warning("Not enough documents to build a network. Try broadening your topic filter.")
        else:
            with st.spinner(f"Building network for {len(net_df)} documents..."):
                net = Network(height="880px", width="100%", bgcolor="#0e1117", font_color="white")
                net.barnes_hut(gravity=-3000, central_gravity=0.3, spring_length=150)

                for _, row in net_df.iterrows():
                    color = topic_colors_net.get(row["dominant_topic"], "#7f7f7f")
                    label = row["filename"][:40]
                    drive_url = f"https://drive.google.com/file/d/{row['file_id']}/view"
                    title = (
                        f"<b>{row['filename']}</b><br>"
                        f"Folder: {row['folder']}<br>"
                        f"Topic: {row['dominant_topic']}<br>"
                        f"Keywords: {row['top_keywords']}<br>"
                        f"Sentiment: {row['sentiment']:.2f}<br>"
                        f"<a href='{drive_url}' target='_blank'>📂 Open in Google Drive</a>"
                    )
                    net.add_node(
                        row["file_id"],
                        label=label,
                        title=title,
                        color=color,
                        size=15
                    )

                keyword_map = {}
                for _, row in net_df.iterrows():
                    kws = [k.strip() for k in str(row["top_keywords"]).split(",") if len(k.strip()) > 3]
                    for kw in kws:
                        if kw not in keyword_map:
                            keyword_map[kw] = []
                        keyword_map[kw].append(row["file_id"])

                pair_keywords = {}
                for kw, file_ids in keyword_map.items():
                    if len(file_ids) > 1:
                        for i in range(len(file_ids)):
                            for j in range(i+1, len(file_ids)):
                                edge_key = tuple(sorted([file_ids[i], file_ids[j]]))
                                if edge_key not in pair_keywords:
                                    pair_keywords[edge_key] = []
                                pair_keywords[edge_key].append(kw)

                edges_added = set()
                for edge_key, shared_kws in pair_keywords.items():
                    if len(shared_kws) >= min_shared:
                        label = ", ".join(shared_kws[:3])
                        net.add_edge(edge_key[0], edge_key[1], title=f"shared: {label}", width=len(shared_kws))
                        edges_added.add(edge_key)

                net.save_graph("/tmp/ken_allen_network.html")
                with open("/tmp/ken_allen_network.html", "r", encoding="utf-8") as f:
                    html = f.read()
                components.html(html, height=900, scrolling=False)

            st.markdown("**Topic Color Legend:**")
            legend_cols = st.columns(5)
            for i, (topic, color) in enumerate(topic_colors_net.items()):
                legend_cols[i % 5].markdown(
                    f"<span style='color:{color}; font-size:1.2em;'>●</span> {topic}",
                    unsafe_allow_html=True
                )

            st.divider()
            st.markdown(f"**{len(net_df)} documents** | **{len(edges_added)} connections** based on {min_shared}+ shared keywords")

# --- Footer ---
st.divider()
st.markdown(f"""
<div style='text-align: center; color: grey; font-size: 0.85em; line-height: 2em;'>
<strong>Materials graciously provided by Kenneth W. Allen</strong><br>
For technical issues or information requests, contact us at <strong>sbgfoundation@protonmail.com</strong><br>
<em>Citation Guidance: When referencing materials from this archive, please cite the original document
and author directly. Example: Allen, Kenneth W. [Document Title]. Samuel B. Griffith Foundation
for Chinese Military Studies Archive.</em><br><br>
© {datetime.now().year} Samuel B. Griffith Foundation for Chinese Military Studies. All rights reserved.
</div>
""", unsafe_allow_html=True)
