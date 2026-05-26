
import streamlit as st
import pandas as pd
import os
import random
import html
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

st.markdown("""
    <style>
        #MainMenu {visibility: hidden;}
        header[data-testid="stHeader"] {visibility: hidden;}
        .stDeployButton {display: none;}
        [data-testid="stToolbar"] {display: none;}
    </style>
""", unsafe_allow_html=True)

@st.cache_data(ttl=0)
def load_data():
    if os.path.exists("ken_allen_public.csv"):
        df = pd.read_csv("ken_allen_public.csv")
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
    st.markdown('''<div style="display:flex; justify-content:center; padding-top:8px;"><img src="data:image/webp;base64,REMOVED" style="width:75px;"/></div>''', unsafe_allow_html=True)
st.divider()

# --- Bio Section ---
col_photo, col_bio = st.columns([1, 3], gap="large")
with col_photo:
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown('''<img src="data:image/webp;base64,REMOVED" style="width:100%; border-radius:4px;"/><p style="text-align:center; font-size:0.85em; color:grey;">Kenneth W. Allen</p>''', unsafe_allow_html=True)
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

# --- Filter out drafts if column exists (legacy safety check) ---
if "is_draft" in df.columns:
    df_filtered = df[df["is_draft"] == False].copy()
else:
    df_filtered = df.copy()

df_filtered["year"] = pd.to_numeric(df_filtered["year"], errors="coerce")

# --- Sidebar ---
st.sidebar.markdown(f"**Documents in archive:** {len(df_filtered)}")

# --- Mode ---
mode = st.radio("Select mode:", ["🔍 Search", "📚 Browse", "📊 Insights & Network", "🎯 Quiz"], horizontal=True)
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

def render_result(row, show_relevance=False, relevance=None):
    category = row.get('public_category') or row.get('dominant_topic') or 'Uncategorized'
    header = f"📄 {row['filename']}  |  {category}"
    if show_relevance and relevance:
        header += f"  |  relevance: {relevance}"
    with st.expander(header):
        col1, col2, col3 = st.columns(3)
        col1.markdown(f"**Topic:** {row['dominant_topic']}")
        col2.markdown(f"**Sentiment:** {row['sentiment']:.2f}")
        col3.markdown(f"**Keywords:** {row['top_keywords']}")
        st.markdown("**Snippet:**")
        st.markdown(f"> {html.escape(str(row['text_snippet'])[:500])}")
        st.markdown("---")
        if row.get("drive_url"):
            st.link_button("📂 View original in Google Drive", row["drive_url"])

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
QUIZ_DATA = [

    # ── ORGANIZATIONAL STRUCTURE ──────────────────────────────
    {
        "section": "Organizational Structure",
        "question": "Which CMC organization, along with its grade, appears first in protocol order among the 15 CMC organizations?",
        "options": {
            "A": "The Political Work Department, Theater Command Leader grade",
            "B": "Joint Staff Department, Theater Command Leader grade",
            "C": "General Office, Theater Command Deputy Leader grade",
        },
        "answer": "C",
        "explanation": (
            "The 15 CMC organizations in protocol order:\n\n"
            "1. General Office (TC Deputy Leader)\n"
            "2. Joint Staff Department (TC Leader)\n"
            "3. Political Work Department (TC Leader)\n"
            "4. Logistic Support Department (TC Leader)\n"
            "5. Equipment Development Department (TC Leader)\n"
            "6. Training Management Department (TC Deputy Leader)\n"
            "7. National Defense Mobilization Department (TC Deputy Leader)\n"
            "8. Discipline Inspection Commission (TC Leader)\n"
            "9. Politics and Law Commission (TC Deputy Leader)\n"
            "10. Science and Technology Commission (TC Deputy Leader)\n"
            "11. Office for Strategic Planning (Corps Leader)\n"
            "12. Office for Reform and Organizational Structure (Corps Leader)\n"
            "13. Office for International Military Cooperation (Corps Leader)\n"
            "14. Audit Office (Corps Leader)\n"
            "15. Agency for Offices Administration (Corps Leader)\n\n"
            "The CMC General Office is always listed first in protocol order. It processes all CMC "
            "communications and documents, coordinates meetings, and conveys orders and directives "
            "to other CMC subordinate functional sections. The General Office is the CMC's lead "
            "administrative organization and is routinely involved in issuing policies and other "
            "documents that dictate how the PLA should function. Tangentially, the CMC General "
            "Office also pursues counter-espionage efforts with the PRC's Ministry of Public Security. "
            "CMC General Office leaders also accompany other PLA leaders in domestic inspections and "
            "key leader engagements with foreign leaders. Of deep significance, the CMC General "
            "Office is also led by one of Xi Jinping's closest confidants."
        ),
    },
    {
        "section": "Organizational Structure",
        "question": "How many Theater Commands (TCs) are there, and what is their protocol order?",
        "options": {
            "A": "5 TCs: Eastern, Southern, Western, Northern, and Central",
            "B": "7 TCs: Shenyang, Beijing, Lanzhou, Jinan, Nanjing, Guangzhou, and Chengdu",
            "C": "3 TCs: Northern, Eastern, and Southern",
        },
        "answer": "A",
        "explanation": (
            "In February 2016, as part of the 'Deepen National Defense and Military Reforms' "
            "(深化国防和军队改革), the PLA transitioned from seven Military Regions (in protocol order: "
            "Shenyang, Beijing, Lanzhou, Jinan, Nanjing, Guangzhou, and Chengdu) into five Theater "
            "Commands listed in protocol order as: Eastern Theater Command (ETC) (东部战区), Southern "
            "Theater Command (STC) (南部战区), Western Theater Command (WTC) (西部战区), Northern Theater "
            "Command (NTC) (北部战区), and Central Theater Command (CTC) (中部战区). The Lanzhou Military "
            "Region's headquarters was downgraded and transitioned onto the WTC Army's headquarters. "
            "The Jinan Military Region's headquarters was also downgraded and transitioned into the "
            "NTC Army's headquarters."
        ),
    },
    {
        "section": "Organizational Structure",
        "question": "Do the PLA's Ministry of National Defense (MND) and the U.S. Department of Defense have the same basic responsibilities?",
        "options": {
            "A": "Yes",
            "B": "No",
        },
        "answer": "B",
        "explanation": (
            "No. The MND's primary responsibilities are to implement foreign relations, coordinate "
            "mobilization efforts, and help manage conscription. Prior to the 2016 reorganization, "
            "every organization within the MND had its own name but each one was dual-hatted with a "
            "CMC organization and may have had a different name. However, under the reorganization, "
            "most of the organizations moved completely from the MND to the CMC, so there are "
            "virtually no dual-hatted organizations. The key MND organizations today are the General "
            "Office, the MND Information Office, and the MND Spokesperson. The MND also works closely "
            "with the CMC's Office of International Military Cooperation (OIMC), which used to be "
            "dual-hatted with the MND.\n\n"
            "The first step in understanding the roles of China's Defense Minister and the Ministry "
            "of National Defense is to recognize that they do not equate in any respect to the United "
            "States' Secretary of Defense and Department of Defense in terms of making defense policy "
            "or commanding the military. In China, the Chinese Communist Party's (CCP's) Central "
            "Military Commission (CMC/中央军委), which has had a mirror image State CMC since 1982, "
            "are responsible for making defense policy and commanding the military. The Defense "
            "Minister is the public face of MND. Although previous Defense Ministers served as a CMC "
            "member and a State Councilor, the current Defense Minister, Admiral Dong Jun, has not "
            "been added as a CMC Member or as a State Councilor as of August 2024. Therefore, the "
            "ministry, itself, is essentially an entity that exists in name only."
        ),
    },

    # ── LEADERSHIP ────────────────────────────────────────────
    {
        "section": "Leadership",
        "question": "Are commanders and political officers still co-equals if they do not have the same rank?",
        "options": {
            "A": "Yes",
            "B": "No",
        },
        "answer": "A",
        "explanation": (
            "Yes, because they have the same grade. Under the current system since 1988, every PLA "
            "organization and officer is assigned one of 15 grades from platoon level to CMC to "
            "designate their position in the military hierarchy. As part of the PLA's 11th force "
            "reduction that began in 2016, the MR leader and MR deputy leader grades were renamed TC "
            "leader and deputy leader grades, respectively. Of particular note, every PLA organization "
            "is assigned a corresponding grade. Each grade from TC deputy leader down has two assigned "
            "ranks, while some ranks, such as major general, can be assigned to up to four grades. "
            "Unlike the U.S. military, which assigns numbers to grades such as O-1 to O-10, the PLA "
            "does not assign numbers to its grades except for special technical officers. On average, "
            "officers up to the rank of senior colonel are promoted in grade every three years, while "
            "they are promoted in rank approximately every four years. Rarely do personnel receive a "
            "rank and grade promotion at the same time; however, that system is slowly changing."
        ),
    },
    {
        "section": "Leadership",
        "question": "What types of Party Committees exist in the PLA?",
        "options": {
            "A": "Strategic Party Committees and Operational Party Committees",
            "B": "Unit Party Committees and Administrative/Functional Department Party Committees",
            "C": "Central Party Committees and Regional Party Committees",
        },
        "answer": "B",
        "explanation": (
            "Unit Party Committees and Administrative/Functional Department Party Committees, meaning "
            "that every department, such as the Operations Bureau and Intelligence Bureau within the "
            "Joint Staff or Staff Department, down to the regiment level has its own Party Committee."
        ),
    },
    {
        "section": "Leadership",
        "question": "Who is the secretary and deputy secretary in a Party Standing Committee?",
        "options": {
            "A": "The commander is the secretary, the chief of staff is the deputy secretary",
            "B": "The political officer is the secretary, the commander is the deputy secretary",
            "C": "The chief of staff is the secretary, the political officer is the deputy secretary",
        },
        "answer": "B",
        "explanation": (
            "The political officer is the secretary, the commander is the deputy secretary, and the "
            "deputy commanders, deputy political commissars, chief of staff, director of the Political "
            "Work Department, Secretary of the Discipline Inspection Commission, and Director of the "
            "Support Department are members. Note that the political commissar for the Support "
            "Department is not on the unit Standing Committee. Although the PLA created an enlisted "
            "Master Chief program for companies to brigades, none of them serve on a Party Standing "
            "Committee. There are no enlisted force advisors to commanders above the brigade level."
        ),
    },

    # ── LOGISTICS AND MAINTENANCE ─────────────────────────────
    {
        "section": "Logistics and Maintenance",
        "question": "What organization is the newly-created Joint Logistics Support Force (JLSF) subordinate to?",
        "options": {
            "A": "The CMC",
            "B": "The CMC Logistic Support Department",
            "C": "The Theater Command Headquarters",
        },
        "answer": "A",
        "explanation": (
            "The Support Department is replacing the two departments at the Theater Command Service "
            "HQ and below levels. As early as 2013, corps leader-grade Army Group Armies began "
            "merging their Logistics Department and Equipment Department into a single Support "
            "Department. As part of the 2016 reorganization, the PLA renamed the CMC General "
            "Logistics Department as the Logistic Support Department and renamed the General Armament "
            "Department as the Equipment Development Department. In September 2016, the CMC created "
            "the Joint Logistics Support Force to unify logistic forces at the strategic level and to "
            "improve logistics support to the PLA's five Theater Commands (TCs). As part of the "
            "reorganization, the PLA merged its Logistics Departments and Equipment Departments into "
            "a single Support Department in each of the service headquarters down to the regiment "
            "level. Although information was found for Support Departments in Army, Air Force, Rocket "
            "Force, Military District, and Garrison corps-, division, and brigade-level headquarters, "
            "no information was found concerning the PLA Navy's headquarters at those levels. The "
            "current Support Departments now provide the equipment and maintain the equipment."
        ),
    },
    {
        "section": "Logistics and Maintenance",
        "question": "How many Corps Deputy Leader-grade Joint Logistics Support Centers are subordinate to the JLSF?",
        "options": {
            "A": "1 in each Theater Command",
            "B": "2 in each Theater Command",
            "C": "3 in each Theater Command",
        },
        "answer": "A",
        "explanation": (
            "The Joint Logistics Support Force (JLSF) is a TC Deputy Leader (TCDL)-grade [副战区] "
            "organization headquartered at the Wuhan Joint Logistics Support Base [武汉联勤保障基地] and "
            "consists of a number of directly subordinate units and five Corps Deputy Leader-grade "
            "[副军级] Joint Logistics Support Centers [JLSC, 联勤保障中心], aligned to support each of "
            "the PLA's Theater Commands."
        ),
    },
    {
        "section": "Logistics and Maintenance",
        "question": "What organization is replacing the former Logistics Department and Equipment Department at the Theater Command Service HQ and below?",
        "options": {
            "A": "Support Department",
            "B": "Operations Department",
            "C": "Management Department",
        },
        "answer": "A",
        "explanation": (
            "As part of the PLA's 11th force reduction and major reorganization that began in 2016, "
            "the PLA continued to make some major changes to the logistics and equipment structures "
            "that began around 2012, when some Logistics Departments and Equipment Departments were "
            "merged into a Support Department. Since 2016, besides creating the Joint Logistics "
            "Support Force at the Theater Command level, all Logistics Departments and Equipment "
            "Departments in the service (Navy, Air Force, and Rocket Force) headquarters were merged "
            "into a single Support Department at the three Theater Command Service Army, Navy, and "
            "Air Force Headquarters and below for all of the services and branches."
        ),
    },

    # ── EDUCATION AND TRAINING ────────────────────────────────
    {
        "section": "Education and Training",
        "question": "How many officer academic institutions have there been since 2017 (as of August 2024)?",
        "options": {
            "A": "34 institutions",
            "B": "37 institutions",
            "C": "67 institutions",
        },
        "answer": "A",
        "explanation": (
            "In 2017, the PLA reduced the number of academic institutions from 67 to 37 (34 officer "
            "universities and colleges/academies and 3 NCO schools), which included abolishing the "
            "Air Force Airborne Troop College and the Marine Corps College — the cadets now attend "
            "the Army Special Operations Academy. Several officer academic institutions have "
            "subordinate NCO schools. Non-commanding officers in all tracks receive both their cadet "
            "education and training and then return to the same institution for their post-cadet "
            "cultivation and training, where they can get a graduate degree. Commanding Officers in "
            "all tracks receive their post-cadet cultivation and training at their service Command "
            "College where they only receive a certificate. The only full-time joint cultivation and "
            "training course occurs at the National Defense University, where they also only receive "
            "a certificate, not a graduate degree."
        ),
    },
    {
        "section": "Education and Training",
        "question": "How many PLA Non-commissioned Officer (NCO) academic institutions are there?",
        "options": {
            "A": "3 institutions",
            "B": "4 institutions",
            "C": "5 institutions",
        },
        "answer": "A",
        "explanation": (
            "Concerning NCO academic institutions, the PLA did not have any NCO schools until 1986. "
            "Since then, the number has changed multiple times. Today, there are only three standalone "
            "NCO schools and several schools that are subordinate to officer academic institutions. "
            "Each NCO school is dedicated to a particular specialty. NCO schools offer only two-year "
            "secondary professional education programs/diplomas and two- to three-year post-secondary "
            "education programs/diplomas, which are roughly equivalent to a U.S. associate's degree. "
            "No NCO schools offer a bachelor's degree. The current three standalone NCO academic "
            "institutions are: 1) Naval NCO School; 2) Air Force Communication NCO Academy; and "
            "3) Rocket Force NCO School. Of note, there is no standalone Army NCO School; however, "
            "there is a Wuhan Ordnance NCO School subordinate to the Army Engineering University, "
            "an NCO school subordinate to the Army Academy of Artillery and Air Defense, and an NCO "
            "school subordinate to the Army Medical University. The Air Force has a subordinate NCO "
            "school subordinate to its Early Warning Academy, and the Rocket Force University of "
            "Engineering has a subordinate NCO school. Several officer academic institutions also "
            "offer NCO training classes."
        ),
    },
    {
        "section": "Education and Training",
        "question": "At what level do PLA academic institutions begin providing joint education for officers in different services?",
        "options": {
            "A": "Command College (company-grade officers)",
            "B": "Command College (field-grade officers)",
            "C": "National Defense University (flag officer)",
        },
        "answer": "C",
        "explanation": (
            "The National Defense University is identified as the only comprehensive joint command "
            "university for senior-level professional education in the Chinese military "
            "(中国军队高级任职教育的一所综合性联合指挥大学). As such, NDU is the PLA's only joint commanding "
            "officer academic institution, which begins at the corps level (major general)."
        ),
    },

    # ── OFFICER CORPS ─────────────────────────────────────────
    {
        "section": "Officer Corps",
        "question": "How many officer ranks and grades are there?",
        "options": {
            "A": "8 ranks and 18 grades",
            "B": "12 ranks and 10 grades",
            "C": "10 ranks and 15 grades",
        },
        "answer": "C",
        "explanation": (
            "10 ranks and 15 grades. As such, each grade has 2 ranks and some ranks can be assigned "
            "to 3-4 grades. In the PLA, ranks don't matter. Personnel do not call each other by their "
            "rank. They call them by their surname and billet — as in 'Wang Deputy Commander.' "
            "Promotions are based on the grade structure. Officers up to regiment leader grade get "
            "promoted every 3 years and receive rank promotions every 4 years."
        ),
    },
    {
        "section": "Officer Corps",
        "question": "What are the different officer career tracks?",
        "options": {
            "A": "Military/Operational Officers, Political Officers, Logistics Officers, Equipment Officers, Technical Officers",
            "B": "Command and Administrative Officers, Special Technical Officers, Staff Officers",
            "C": "Strategic Officers, Tactical Officers, Operational Officers, Support Officers, Technical Officers",
        },
        "answer": "B",
        "explanation": (
            "Prior to 2021, the PLA's officer corps, which it calls active-duty officers/cadres, was "
            "organized into five career tracks: military/operational officer, political officer, "
            "logistics officer, equipment/armament officer, and special technical officer. The PLA "
            "later combined the first four career tracks together and identified them as non-special "
            "technical officers, and in 2021 renamed them 'command and administrative officers.' It "
            "still has the special technical officer track as a separate track. Unlike the U.S. "
            "military, the PLA does not have alpha-numeric codes like the Military Occupational "
            "Specialty (MOS) for its officers or enlisted personnel.\n\n"
            "The PLA further organizes its officers into three categories, each of which receive "
            "different types of education and training as they move up the career ladder:\n\n"
            "Commanding officers (指挥军官): includes the Commander, Political Commissar, Deputy "
            "Commanders and Political Commissars, the Director and Deputy Director for all first-, "
            "second-, and third-level departments within each service headquarters, Theater Command, "
            "and subordinate units, and the leaders in each of the 15 CMC organizations.\n\n"
            "Staff officers (参谋/干事): serve in each of the four first-level departments and their "
            "subordinate second- and third-level departments, as well as the 15 CMC organizations.\n\n"
            "Special technical (专业技术) officers."
        ),
    },
    {
        "section": "Officer Corps",
        "question": "How many deputy commanders do units have?",
        "options": {
            "A": "1",
            "B": "2 to 4",
            "C": "Always 3",
        },
        "answer": "B",
        "explanation": (
            "From 2 to 4, depending on the level. Never say 'the deputy commander' — always say "
            "'one of the deputy commanders.'\n\n"
            "\"Each MR commander shares responsibility with a political commissar (both are military "
            "region leader grade officers). The commander is assisted by three to five Army deputy "
            "commanders (who are military region deputy leader grade officers), the regional air "
            "force commander (dual-hatted as an MR deputy commander), and a naval fleet commander "
            "in the Jinan, Nanjing, and Guangzhou MRs (also dual-hatted as an MR deputy commander). "
            "Army deputy commanders each are assigned individual portfolios, such as operations, "
            "logistics, or armament. The MR political commissar is assisted by two or three deputy "
            "political commissars. These personnel form the nucleus of the MR-level party committee "
            "with the political commissar normally acting as first secretary.\"\n\n"
            "\"The TC headquarters' leadership consists of a commander, a political commissar, "
            "multiple deputy commanders (often two to four), and multiple deputy political commissars "
            "(DPC). Deputy commanders can serve in a single-hatted or dual-hatted capacity. "
            "Typically, there are permanent PLAA, PLAN and PLAAF deputy commanders who serve as a "
            "deputy commander in a single-hatted capacity within TC headquarters. Each TC service "
            "component (e.g. TC Army, TC Navy, TC Air Force) commander is also concurrently a TC "
            "deputy commander.\""
        ),
    },

    # ── DOCTRINE ──────────────────────────────────────────────
    {
        "section": "Doctrine",
        "question": "When was the last version of the publication Science of Military Strategy published?",
        "options": {
            "A": "2001",
            "B": "2013",
            "C": "2020",
        },
        "answer": "C",
        "explanation": (
            "The August 2020 version of The Science of Military Strategy is a revision of the "
            "previous 2017 version. The PLA's National Defense University publication is a core "
            "textbook for senior officers on how wars should be planned and conducted at the strategic "
            "level. In 2005, the PLA published an English translation of the 2001 Chinese version. "
            "In January 2022, the China Aerospace Studies Institute published an English translation "
            "of the August 2020 version using an automated translation engine. That version is "
            "available at CASI's website."
        ),
    },
    {
        "section": "Doctrine",
        "question": "What concept is the basis for China's military strategy?",
        "options": {
            "A": "The PRC's military strategy is based on the concept of 'active defense'",
            "B": "The concept of 'Peoples' War' is the basis for China's military strategy",
            "C": "The basis of the PRC's military strategy is to 'Fight Wars Under Informationized Conditions'",
        },
        "answer": "A",
        "explanation": (
            "Since 2022, the PRC's stated defense policy has been oriented toward safeguarding its "
            "sovereignty, security, and development interests, while emphasizing a greater global "
            "role for itself. The PRC's military strategy remains based on the concept of "
            "'active defense.'"
        ),
    },
    {
        "section": "Doctrine",
        "question": "The authoritative text the PLA uses to define military terms — which also includes an English translation of each Chinese term — is:",
        "options": {
            "A": "Junyu (军语 / Military Terminology)",
            "B": "Han-Ying/Ying-Han Junshi Dazidian (汉英英汉军事大字典)",
            "C": "Wubeizhi (武备字 / Chinese Military Encyclopedia)",
        },
        "answer": "A",
        "explanation": (
            "Junyu is the official military dictionary of the PLA, approved by the Central Military "
            "Commission. It is organized in 26 categories, plus 9 secondary categories under the "
            "category Army (陆军). It has 8,587 entries and 195 pictures or charts. Each entry has "
            "an English translation of the headword. It has an index of entries organized by pinyin "
            "and an English index as well. This book is the authoritative source for the current "
            "Chinese definition of military terms in the PLA. Wubeizhi is an encyclopedia of ancient "
            "Chinese military terms. Han-Ying/Ying-Han Junshi Dazidian (Chinese-English/English-"
            "Chinese Military Dictionary) is not an official publication of the PLA and does not "
            "include definitions of military terms."
        ),
    },
    {
        "section": "Doctrine",
        "question": "What is the national strategy of the People's Republic of China?",
        "options": {
            "A": "To adopt Xi Jinping's thoughts for China to resume its rightful place in the world",
            "B": "To achieve 'the great rejuvenation of the Chinese nation' by 2049",
            "C": "To 'hide capabilities and bide time' (韬光养晦 / Tao Guang Yang Hui)",
        },
        "answer": "B",
        "explanation": (
            "The strategy to achieve 'the great rejuvenation of the Chinese nation' is a determined "
            "pursuit of political, social, and military modernity to expand the PRC's national power, "
            "perfect its governance, and revise the international order in support of the PRC's "
            "system of governance and national interests. 'Hide capabilities and bide time' "
            "(Tao Guang Yang Hui) is a component of China's previous strategy."
        ),
    },

    # ── ENLISTED FORCE ────────────────────────────────────────
    {
        "section": "Enlisted Force",
        "question": "How many years do enlisted conscripts/new recruits serve at least?",
        "options": {
            "A": "2 years",
            "B": "3 years",
            "C": "4 years",
        },
        "answer": "A",
        "explanation": (
            "Prior to 1999, Army conscripts served for 3 years, while Navy, Air Force, and Second "
            "Artillery conscripts served for 4 years. After that period, they could remain on active "
            "duty for a total of 16 years before they were demobilized and sent back to their "
            "hometown. Since 1999, all conscripts serve for 2 years with the option for serving as "
            "an NCO through six grades for a total of 30 years depending on their specialty. For "
            "example, cooks and drivers have a 12-year limit. NCOs can only retire when they have "
            "served a full 30 years or reach age 55; otherwise, they are demobilized and sent home."
        ),
    },
    {
        "section": "Enlisted Force",
        "question": "How many NCO grade levels and ranks are there in the PLA?",
        "options": {
            "A": "4 grade levels and 6 ranks",
            "B": "5 grade levels and 5 ranks",
            "C": "3 grade levels and 8 ranks",
        },
        "answer": "C",
        "explanation": (
            "NCOs are organized into 3 grade levels (junior, intermediate, and senior) and 8 ranks.\n\n"
            "\"In December 2009, the CMC implemented a new 'Plan for Reforming the NCO System' along "
            "with three revised regulations which covered NCO active-duty service periods, management, "
            "and education and training. The 2009 plan and revised regulations also changed the name "
            "for each of the ranks, as well as adding a third rank at the senior NCO grade level. "
            "The plan and revised regulations allow NCOs to serve for more than a total of 14 years "
            "in the senior NCO grade level. However, the exact number of years for each rank in the "
            "senior grade level is still not clear. Unlike the officer corps, which has 15 grades and "
            "10 ranks, the enlisted force has only three NCO grade levels and a total of eight NCO "
            "ranks as shown in the table below. It is important to note that, unlike officers who "
            "wear ribbons that identify their grade and number of years served, NCOs do not wear any "
            "ribbons. In 2022, the PLA made further adjustments to the rank structure by changing "
            "the name for two ranks.\""
        ),
    },
    {
        "section": "Enlisted Force",
        "question": "Is there a central promotion board for all personnel?",
        "options": {
            "A": "Yes",
            "B": "No",
        },
        "answer": "B",
        "explanation": (
            "No. All officer and enlisted promotions below the corps level are done locally by the "
            "next higher level Party Committee. Specifically, platoon, company, and battalion "
            "promotions are done by the regiment Party Committee; regiment promotions by the division "
            "Party Committee; and division and brigade promotions by the corps Party Committee."
        ),
    },

    # ── FOREIGN RELATIONS ─────────────────────────────────────
    {
        "section": "Foreign Relations",
        "question": "What organization manages the PLA's foreign relations (military diplomacy)?",
        "options": {
            "A": "The Ministry of National Defense",
            "B": "The CMC Joint Staff Department's Office of International Military Cooperation",
            "C": "Both the Ministry of National Defense and the CMC Joint Staff Department's Office of International Military Cooperation",
        },
        "answer": "C",
        "explanation": (
            "The Office for International Military Coordination (OIMC / 国际军事合作办公室) was established "
            "in its current form with the 2016 reforms and is listed 13th in protocol order within "
            "the Central Military Commission (CMC). Its predecessor, the Foreign Affairs Office "
            "(FAO / 外事办公室 / 外办), was shared with the General Staff Department (GSD / 参谋总部), "
            "reflecting its dual mission of foreign representation and foreign operations, primarily "
            "intelligence and information operations. This dual alignment continued after the reforms, "
            "with the OIMC being elevated to a direct subordinate of the CMC, maintaining its 13th "
            "place in protocol order and receiving the grade of corps leader, along with its own "
            "shoulder patch. Currently, the OIMC is tasked with developing and executing military "
            "cooperation in the New Era, guided by the 'Regulations on International Military "
            "Cooperation' (国际军事合作工作条例), which came into force on March 1, 2021, and informed "
            "by the 2019 White Paper, 'China's National Defense in the New Era.' The official "
            "Ministry of National Defense (MND) website defines the OIMC as, 'The office ... mainly "
            "responsible for foreign military exchanges and cooperation, and for managing and "
            "coordinating the foreign affairs work of the whole military.'"
        ),
    },
    {
        "section": "Foreign Relations",
        "question": "How often has the PLA Navy sent 3-ship escort task forces to the Gulf of Aden since 2008 for anti-piracy missions?",
        "options": {
            "A": "2 per year",
            "B": "3 per year",
            "C": "4 per year",
        },
        "answer": "C",
        "explanation": (
            "According to China's Ministry of National Defense, as of December 2023, the PLAN had "
            "dispatched more than 150 ships and over 35,000 troops in 45 anti-piracy escort task "
            "forces (ETF) to the Gulf of Aden and adjacent waters since 2008 — approximately 4 per "
            "year. According to Global Times, 'After an escort task force completes an escort mission "
            "in the Gulf of Aden, it usually conducts a two-month foreign visit, during which it "
            "will conduct joint exercises with foreign navies. Through this way, the PLA Navy "
            "displays its image of being a civilized and peaceful force.'"
        ),
    },
    {
        "section": "Foreign Relations",
        "question": "Which service has conducted the most military exercises with foreign countries since 2018 (as of June 2024)?",
        "options": {
            "A": "Army",
            "B": "Navy",
            "C": "Air Force",
        },
        "answer": "A",
        "explanation": (
            "In 2023, China participated in 24 joint military exercises, a significant increase from "
            "the COVID period, yet still below 2018 and 2019 levels.\n\n"
            "Joint Military Exercises by Service, 2018-2023:\n"
            "Navy:       13 | 12 | 1 | 6 | 4 | 10  (Total: 46)\n"
            "Army:       16 | 22 | 5 | 7 | 2 |  7  (Total: 59)\n"
            "Air Force:   3 |  4 | 2 | 1 | 3 |  4  (Total: 17)\n\n"
            "In 2023, the Navy witnessed a resurgence in exercise participation, increasing from 4 "
            "to 10 exercises and surpassing the Army in that year, showcasing a revitalized focus "
            "on maritime operations. However, the Army leads the full 2018-2023 period overall. "
            "There was a notable increase in joint exercises in Southeast Asia in 2023 (14 exercises "
            "vs. 2 the prior year). Engagement with Russia remained consistent at 5 exercises. "
            "Exercises with South Asia declined due to China-India tensions, leaving Pakistan as the "
            "only South Asian partner since 2020."
        ),
    },

    # ── QUALITY OF LIFE ───────────────────────────────────────
    {
        "section": "Quality of Life",
        "question": "At what age can military male and female personnel get married?",
        "options": {
            "A": "Anytime",
            "B": "Age 21 for both males and females",
            "C": "Age 25 for males and age 23 for females",
        },
        "answer": "C",
        "explanation": (
            "Males must be at least 25 years old and females 23. Unmarried personnel cannot live "
            "together. Late marriage is encouraged. Two-year conscripts/enlistees are not allowed "
            "to marry. Personnel who are 30 years or older can receive help from the unit in "
            "matchmaking."
        ),
    },
    {
        "section": "Quality of Life",
        "question": "What personnel do units provide matchmaking ceremonies for if they are 30 years old and not married?",
        "options": {
            "A": "Males",
            "B": "Females",
            "C": "Males and Females",
        },
        "answer": "A",
        "explanation": (
            "The PLA works tirelessly to organize matchmaking events and group weddings to help "
            "military personnel find spouses, because not being able to find wives has become a "
            "major concern and has prompted more marriage-age military members to leave the military "
            "or not want to join in the first place."
        ),
    },
    {
        "section": "Quality of Life",
        "question": "Can two-year conscripts live off base?",
        "options": {
            "A": "Yes",
            "B": "No",
        },
        "answer": "B",
        "explanation": (
            "The PLA requires all two-year conscripts/enlistees to live in on-base military barracks. "
            "As conscripts cannot get married, they are not allowed to live off base. NCOs who were "
            "below Master Sergeant Class Four (less than 10 years of service) are also required to "
            "live in barracks. Senior Grade NCOs, upon approval for their family to accompany the "
            "military member, will be provided housing with the military member paying a monthly "
            "rent. Active-duty NCOs also receive rent allowance."
        ),
    },

    # ── WEAPON SYSTEMS AND EQUIPMENT ──────────────────────────
    {
        "section": "Weapon Systems and Equipment",
        "question": "The PRC's Military-Civil Fusion (MCF) strategy includes objectives to:",
        "options": {
            "A": "Increase the lethality and precision of current key weapons systems, particularly tactical delivery systems and munitions",
            "B": "Develop and acquire advanced multiservice-use technology for military and civilian purposes and deepen reform of national civilian and defense educational institutions",
            "C": "Develop and acquire advanced dual-use technology for military purposes and deepen reform of the national defense science and technology industries",
        },
        "answer": "C",
        "explanation": (
            "The PRC's MCF development strategy encompasses six interrelated efforts: (1) fusing "
            "China's defense industrial base to its civilian technology and industrial base; "
            "(2) integrating and leveraging science and technology innovations across military and "
            "civilian sectors; (3) cultivating talent and blending military and civilian expertise "
            "and knowledge; (4) building military requirements into civilian infrastructure and "
            "leveraging civilian construction for military purposes; (5) leveraging civilian service "
            "and logistics capabilities for military purposes; and (6) expanding and deepening "
            "China's national defense mobilization system to include all relevant aspects of its "
            "society and economy for use in competition and war."
        ),
    },
    {
        "section": "Weapon Systems and Equipment",
        "question": "The PRC's goals for modernizing its armed forces in the 'New Era' are:",
        "options": {
            "A": "By 2027: accelerate integrated development of mechanization, informatization, and intelligentization; By 2035: basically complete modernization of national defense; By 2049: fully transform into world-class forces",
            "B": "By 2027: develop, test, and field sufficient weapons to liberate Taiwan; By 2035: basically complete modernization; By 2049: world-class forces",
            "C": "By 2027: develop weapons for Taiwan; By 2040: complete modernization; By 2059: world-class forces",
        },
        "answer": "A",
        "explanation": (
            "In a March 2021 speech, Xi Jinping detailed that the 2027 modernization goal is the "
            "first step in a broader modernization effort. PLA writings note the 'three-step' "
            "modernization plan connects 'near-, medium-, and long-term goals in 2027, 2035, and "
            "2049' respectively.\n\n"
            "By 2027: 'Accelerate the integrated development of mechanization, informatization, and "
            "intelligentization,' while boosting the speed of modernization in military theories, "
            "organizations, personnel, and weapons and equipment.\n\n"
            "By 2035: 'To comprehensively advance the modernization of military theory, "
            "organizational structure, military personnel, and weaponry and equipment in step with "
            "the modernization of the country and basically complete the modernization of national "
            "defense and the military.'\n\n"
            "By 2049: 'To fully transform the people's armed forces into world-class forces.'"
        ),
    },
    {
        "section": "Weapon Systems and Equipment",
        "question": "Which of the following statements about PLAAF and PLAN Aviation aircraft is true?",
        "options": {
            "A": "PLAAF and PLAN Aviation continue to field greater numbers of fifth-generation aircraft and probably will become a majority fifth-generation force within the next several years",
            "B": "PLAAF, PLAA, and PLAN Aviation continue to field greater numbers of fourth-generation aircraft and probably will become a majority fifth-generation force within the next decade",
            "C": "PLAAF and PLAN Aviation continue to field greater numbers of fourth-generation aircraft and probably will become a majority fourth-generation force within the next several years",
        },
        "answer": "C",
        "explanation": (
            "As of 2023, more than 1,300 of 1,900 total fighters (not including trainers) are "
            "fourth-generation. For fifth-generation fighters, the PLAAF has operationally fielded "
            "its new J-20 fifth-generation stealth fighter, and PRC social media revealed a new "
            "2-seat variant of the J-20 in October 2021. However, the overall force remains "
            "predominantly fourth-generation and is trending toward becoming a majority "
            "fourth-generation force within the next several years — not fifth-generation."
        ),
    },
]


# =============================================================
# QUIZ MODE
# =============================================================


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
    col2.metric("Categories Covered", results["public_category"].nunique() if len(results) > 0 else 0)
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

    all_categories = sorted(df_filtered["public_category"].unique().tolist())
    selected_category = st.sidebar.selectbox("Subject Category", ["All categories"] + all_categories)

    all_topics = sorted(df_filtered["dominant_topic"].unique().tolist())
    selected_topic = st.sidebar.selectbox("PLA Topic", ["All topics"] + all_topics)

    st.sidebar.markdown("**Publication Year**")
    st.sidebar.markdown("*Year is extracted from the document filename where available. For documents covering a range of years, the most recent year is used.*")
    year_range = st.sidebar.slider("Year range", 1981, 2024, (1981, 2024), 1)
    filter_by_year = st.sidebar.toggle("Apply year filter", value=False)

    browsed = df_filtered.copy()
    browsed["year"] = pd.to_numeric(browsed["year"], errors="coerce")

    if selected_category != "All categories":
        browsed = browsed[browsed["public_category"] == selected_category]
    if selected_topic != "All topics":
        browsed = browsed[browsed["dominant_topic"] == selected_topic]
    if filter_by_year:
        browsed = browsed[
            (browsed["year"].isna()) |
            ((browsed["year"] >= year_range[0]) & (browsed["year"] <= year_range[1]))
        ]

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Documents", len(browsed))
    col2.metric("Categories", browsed["public_category"].nunique())
    col3.metric("Avg Sentiment", f"{browsed['sentiment'].mean():.2f}" if len(browsed) > 0 else "N/A")
    col4.metric("Top Topic", browsed["dominant_topic"].mode()[0] if len(browsed) > 0 else "N/A")
    st.divider()

    if len(browsed) > 0:
        st.subheader("Topic Distribution")
        topic_counts = browsed["dominant_topic"].value_counts().reset_index()
        topic_counts.columns = ["Topic", "Count"]
        st.bar_chart(topic_counts.set_index("Topic"))
        st.divider()

    if selected_category == "All categories" and len(browsed) > 0:
        st.subheader("Documents by Category")
        category_counts = browsed["public_category"].value_counts().reset_index()
        category_counts.columns = ["Category", "Count"]
        st.dataframe(category_counts, width="stretch", hide_index=True)
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
            st.plotly_chart(fig_area, width="stretch")

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
                st.plotly_chart(fig_kw, width="stretch")
        else:
            with kw_col2:
                st.info("Not enough keyword data for this topic.")

        st.divider()

        # ---- CHART 3: Heatmap ----
        st.markdown("### 🔥 Topic Concentration by Subject Category")
        st.markdown("""
This heatmap shows how research topics are distributed across Kenneth Allen's subject categories.
Each row is a subject category; each column is one of the ten PLA research topics.
The number in each cell represents what percentage of that category's documents fall under that topic.
Darker blue cells indicate stronger topic concentration — meaning that category is heavily focused on one subject area.
        """)

        heat_df = df_analytics.groupby(["public_category", "dominant_topic"]).size().reset_index(name="count")
        heat_pivot = heat_df.pivot(index="public_category", columns="dominant_topic", values="count").fillna(0)
        heat_norm = heat_pivot.div(heat_pivot.sum(axis=1), axis=0) * 100
        category_totals = df_analytics["public_category"].value_counts()
        sorted_categories = [c for c in category_totals.index if c in heat_norm.index]
        heat_norm = heat_norm.loc[sorted_categories]

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
                title=dict(text="Subject Category", font=dict(color="white", size=13)),
                color="white",
                tickfont=dict(size=11, color="white")
            ),
            coloraxis_colorbar=dict(
                title="% of Category",
                tickfont=dict(color="white"),
            ),
            title=dict(
                text="Topic Concentration Heatmap — Subject Category × Research Topic",
                font=dict(color="white", size=14)
            )
        )
        fig_heat.update_traces(textfont=dict(color="white", size=10))
        st.plotly_chart(fig_heat, width="stretch")

        st.divider()

        # ---- CHART 4: Treemap ----
        st.markdown("### 🗺️ Archive Structure — Treemap")
        st.markdown("""
This treemap gives you a bird's-eye view of the entire archive — all 943 publicly available documents — organized by category and research topic simultaneously.
Each large outer rectangle represents one subject category. Inside each category, smaller rectangles show how documents are
distributed across PLA research topics, with size proportional to document count. Colors match the topic color legend used throughout this app.
        """)

        tree_df = df_analytics.groupby(["public_category", "dominant_topic"]).size().reset_index(name="count")

        fig_tree = px.treemap(
            tree_df,
            path=["public_category", "dominant_topic"],
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
                text="Ken Allen Archive — Full Structure by Category and Topic",
                font=dict(color="white", size=14)
            ),
            margin=dict(t=50, l=10, r=10, b=10)
        )
        st.plotly_chart(fig_tree, width="stretch")

        st.divider()

        # ---- CHART 5: Leadership Mentions Over Time ----
        st.markdown("### 👤 PLA Leadership Mentions Over Time")
        st.markdown("""
This chart tracks how frequently the names of key PLA and Chinese political leaders appear across Kenneth Allen\'s
dated documents, year by year. Each line represents one leader. A spike in a given year means Allen was writing
about or referencing that leader frequently — often coinciding with a promotion, policy announcement, military reform,
or significant event associated with that figure.
        """)

        leaders = {
            "Jiang Zemin":    ["Jiang Zemin", "Jiang"],
            "Hu Jintao":      ["Hu Jintao", "Hu Jintao"],
            "Xi Jinping":     ["Xi Jinping", "Xi Jinping"],
            "Liu Huaqing":    ["Liu Huaqing"],
            "Chi Haotian":    ["Chi Haotian"],
            "Xu Caihou":      ["Xu Caihou"],
            "Guo Boxiong":    ["Guo Boxiong"],
            "Fan Changlong":  ["Fan Changlong"],
            "Zhang Youxia":   ["Zhang Youxia"],
            "He Weidong":     ["He Weidong"],
            "Xu Qiliang":     ["Xu Qiliang"],
            "Ma Xiaotian":    ["Ma Xiaotian"],
            "Yi Xiaoguang":   ["Yi Xiaoguang"],
            "Chang Dingqiu":  ["Chang Dingqiu"],
            "Wang Hai":       ["Wang Hai"],
        }

        default_leaders = ["Xi Jinping", "Hu Jintao", "Jiang Zemin", "Xu Qiliang", "Ma Xiaotian", "Xu Caihou"]

        selected_leaders = st.multiselect(
            "Select leaders to display:",
            options=list(leaders.keys()),
            default=default_leaders,
            key="leader_select"
        )

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
                st.plotly_chart(fig_lead, width="stretch")

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
**Each line (edge)** connects two documents that share a minimum number of keywords in common.
Hover over any node to see the document title, topic, keywords, and a link to open it in Google Drive.
        """)

        st.sidebar.markdown("---")
        st.sidebar.markdown("**Network Filters**")

        all_topics_net = sorted(df_filtered["dominant_topic"].unique().tolist())
        net_topic = st.sidebar.selectbox(
            "Filter by Research Topic",
            ["All topics"] + all_topics_net,
            key="net_topic",
            help="Select a single topic for the most readable and analytically useful graph."
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

                for node_idx, row in net_df.iterrows():
                    color = topic_colors_net.get(row["dominant_topic"], "#7f7f7f")
                    label = row["filename"][:40]
                    doc_drive_url = row.get("drive_url", "")
                    category = row.get("public_category", row.get("dominant_topic", ""))
                    title = (
                        f"<b>{html.escape(str(row['filename']))}</b><br>"
                        f"Category: {html.escape(str(category))}<br>"
                        f"Topic: {html.escape(str(row['dominant_topic']))}<br>"
                        f"Keywords: {html.escape(str(row['top_keywords']))}<br>"
                        f"Sentiment: {row['sentiment']:.2f}<br>"
                    )
                    if doc_drive_url:
                        title += f"<a href='{doc_drive_url}' target='_blank'>📂 Open in Google Drive</a>"
                    net.add_node(
                        node_idx,
                        label=label,
                        title=title,
                        color=color,
                        size=15
                    )

                keyword_map = {}
                for node_idx, row in net_df.iterrows():
                    kws = [k.strip() for k in str(row["top_keywords"]).split(",") if len(k.strip()) > 3]
                    for kw in kws:
                        if kw not in keyword_map:
                            keyword_map[kw] = []
                        keyword_map[kw].append(node_idx)

                pair_keywords = {}
                for kw, node_ids in keyword_map.items():
                    if len(node_ids) > 1:
                        for i in range(len(node_ids)):
                            for j in range(i+1, len(node_ids)):
                                edge_key = tuple(sorted([node_ids[i], node_ids[j]]))
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
                    html_content = f.read()
                components.html(html_content, height=900, scrolling=False)

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


if mode == "🎯 Quiz":
    st.subheader("PLA Knowledge Assessment")
    st.markdown(
        "Test your understanding of the People's Liberation Army across eight subject areas. "
        "Questions were developed in collaboration with **Kenneth W. Allen**. "
        "Current as of **May 2026**."
    )
    st.divider()

    if "quiz_section"   not in st.session_state: st.session_state.quiz_section   = "All Sections"
    if "quiz_questions" not in st.session_state: st.session_state.quiz_questions = []
    if "quiz_index"     not in st.session_state: st.session_state.quiz_index     = 0
    if "quiz_score"     not in st.session_state: st.session_state.quiz_score     = 0
    if "quiz_answered"  not in st.session_state: st.session_state.quiz_answered  = False
    if "quiz_selected"  not in st.session_state: st.session_state.quiz_selected  = None
    if "quiz_started"   not in st.session_state: st.session_state.quiz_started   = False
    if "quiz_complete"  not in st.session_state: st.session_state.quiz_complete  = False
    if "quiz_history"   not in st.session_state: st.session_state.quiz_history   = []

    SECTIONS = ["All Sections"] + sorted(set(q["section"] for q in QUIZ_DATA))

    def start_quiz(section):
        pool = QUIZ_DATA if section == "All Sections" else [q for q in QUIZ_DATA if q["section"] == section]
        shuffled = pool.copy()
        random.shuffle(shuffled)
        st.session_state.quiz_questions = shuffled
        st.session_state.quiz_index     = 0
        st.session_state.quiz_score     = 0
        st.session_state.quiz_answered  = False
        st.session_state.quiz_selected  = None
        st.session_state.quiz_started   = True
        st.session_state.quiz_complete  = False
        st.session_state.quiz_history   = []
        st.session_state.quiz_section   = section

    if not st.session_state.quiz_started:
        col_sel, col_btn = st.columns([2, 1])
        with col_sel:
            section_choice = st.selectbox("Choose a section (or take the full quiz):", SECTIONS, key="section_selector")
        with col_btn:
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("▶  Start Quiz", use_container_width=True):
                start_quiz(section_choice)
                st.rerun()
        st.divider()
        st.markdown("**Quiz sections:**")
        section_counts = {}
        for q in QUIZ_DATA:
            section_counts[q["section"]] = section_counts.get(q["section"], 0) + 1
        cols = st.columns(4)
        for i, (sec, count) in enumerate(section_counts.items()):
            with cols[i % 4]:
                st.markdown(f"<p style='font-size:1.05rem; font-weight:600; margin-bottom:2px;'>{sec}</p><p style='font-size:0.85rem; color:grey; margin-top:0;'>{count} questions</p>", unsafe_allow_html=True)

    elif st.session_state.quiz_complete:
        total = len(st.session_state.quiz_questions)
        score = st.session_state.quiz_score
        pct   = round(score / total * 100) if total else 0
        if pct == 100:  grade_msg = "🏆 Perfect score — Ken Allen would be proud."
        elif pct >= 80: grade_msg = "⭐ Strong result. You know your PLA."
        elif pct >= 60: grade_msg = "📚 Good foundation. A few areas to review."
        else:           grade_msg = "🔄 Keep studying — the PLA is complex."
        st.markdown(f"### Quiz Complete — {grade_msg}")
        st.divider()
        r1, r2, r3 = st.columns(3)
        r1.metric("Final Score", f"{score} / {total}")
        r2.metric("Percentage",  f"{pct}%")
        r3.metric("Section",     st.session_state.quiz_section)
        st.divider()
        if st.session_state.quiz_history:
            st.markdown("**Results by section:**")
            sec_results = {}
            for item in st.session_state.quiz_history:
                s = item["section"]
                if s not in sec_results:
                    sec_results[s] = {"correct": 0, "total": 0}
                sec_results[s]["total"]   += 1
                sec_results[s]["correct"] += 1 if item["correct"] else 0
            breakdown_cols = st.columns(min(len(sec_results), 4))
            for i, (sec, res) in enumerate(sec_results.items()):
                breakdown_cols[i % 4].metric(sec, f"{res['correct']}/{res['total']}", delta=f"{round(res['correct']/res['total']*100)}%")
            st.divider()
            missed = [item for item in st.session_state.quiz_history if not item["correct"]]
            if missed:
                st.markdown(f"**Review — {len(missed)} missed question(s):**")
                for item in missed:
                    with st.expander(f"❌  {item['question'][:80]}..."):
                        st.markdown(f"**Your answer:** {item['selected']} — {item['options'][item['selected']]}")
                        st.markdown(f"**Correct answer:** {item['answer']} — {item['options'][item['answer']]}")
                        st.markdown("---")
                        st.markdown(f"**Explanation:** {item['explanation']}")
                st.divider()
        col_restart, col_new = st.columns(2)
        with col_restart:
            if st.button("🔄  Retry Same Section", use_container_width=True):
                start_quiz(st.session_state.quiz_section)
                st.rerun()
        with col_new:
            if st.button("🏠  Choose New Section", use_container_width=True):
                st.session_state.quiz_started  = False
                st.session_state.quiz_complete = False
                st.rerun()

    else:
        questions = st.session_state.quiz_questions
        idx       = st.session_state.quiz_index
        total_q   = len(questions)
        if idx >= total_q:
            st.session_state.quiz_complete = True
            st.rerun()
        q = questions[idx]
        prog_col, score_col, section_col = st.columns([4, 1, 1])
        with prog_col:
            st.progress((idx) / total_q, text=f"Question {idx + 1} of {total_q}")
        score_col.metric("Score", f"{st.session_state.quiz_score}/{idx}")
        section_col.metric("Section", q["section"].split()[0])
        if st.button("↩  Restart Quiz", key="restart_mid"):
            st.session_state.quiz_started  = False
            st.session_state.quiz_complete = False
            st.rerun()
        st.divider()
        st.markdown(f"### {q['question']}")
        st.markdown("")
        answered = st.session_state.quiz_answered
        selected = st.session_state.quiz_selected
        for key, text in q["options"].items():
            if answered:
                if key == q["answer"]:
                    label = f"✅  {key})  {text}"
                elif key == selected and selected != q["answer"]:
                    label = f"❌  {key})  {text}"
                else:
                    label = f"　  {key})  {text}"
            else:
                label = f"{key})  {text}"
            if st.button(label, key=f"opt_{idx}_{key}", disabled=answered, use_container_width=True):
                st.session_state.quiz_selected = key
                st.session_state.quiz_answered = True
                if key == q["answer"]:
                    st.session_state.quiz_score += 1
                st.session_state.quiz_history.append({
                    "section":     q["section"],
                    "question":    q["question"],
                    "options":     q["options"],
                    "answer":      q["answer"],
                    "selected":    key,
                    "correct":     key == q["answer"],
                    "explanation": q["explanation"],
                })
                st.rerun()
        if answered:
            st.divider()
            if selected == q["answer"]:
                st.success("✅  Correct!")
            else:
                st.error(f"❌  Incorrect — the correct answer is **{q['answer']}**: {q['options'][q['answer']]}")
            with st.expander("📖  Ken Allen's Explanation", expanded=True):
                st.markdown(q["explanation"])
            st.divider()
            is_last   = (idx + 1 >= total_q)
            btn_label = "🏁  Finish Quiz" if is_last else "Next Question ▶"
            if st.button(btn_label, use_container_width=True, type="primary"):
                st.session_state.quiz_index   += 1
                st.session_state.quiz_answered = False
                st.session_state.quiz_selected = None
                if idx + 1 >= total_q:
                    st.session_state.quiz_complete = True
                st.rerun()
