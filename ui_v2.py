from __future__ import annotations

import html
import streamlit as st


NAV_ITEMS = [
    ("홈", "⌂"),
    ("시장 현황", "▥"),
    ("종목 분석", "◫"),
    ("공시 분석", "▤"),
    ("테마 & 섹터", "◇"),
    ("포트폴리오", "▣"),
    ("관심 종목", "☆"),
    ("AI 인사이트", "✦"),
    ("데이터 연결 관리", "⚙"),
]


def apply_theme():
    st.markdown(
        """
<style>
:root {
  --bg:#F5F8FC;
  --surface:#FFFFFF;
  --surface-soft:#F8FAFF;
  --line:#E4EAF3;
  --text:#17233A;
  --muted:#718096;
  --blue:#3B82F6;
  --blue-soft:#EAF2FF;
  --green:#35B99A;
  --purple:#8B72D8;
  --orange:#F4A340;
  --pink:#E96B9B;
  --red:#E84C76;
  --navy:#20385F;
}

html, body, [class*="css"] {
  font-family: Pretendard, "Noto Sans KR", "Apple SD Gothic Neo", sans-serif;
}
.stApp {
  background:var(--bg);
  color:var(--text);
}
.block-container {
  max-width:1500px;
  padding:1.25rem 1.6rem 3.5rem;
}
header[data-testid="stHeader"] {
  background:rgba(245,248,252,.94);
  backdrop-filter:blur(12px);
}
h1,h2,h3,h4 {
  color:var(--text);
  letter-spacing:-.035em;
}
h1 { font-weight:800; }
h2,h3 { font-weight:760; }
p,li { line-height:1.55; }
[data-testid="stCaptionContainer"] { color:var(--muted); }

/* Sidebar — light, compact, dashboard-like */
section[data-testid="stSidebar"] {
  background:#FFFFFF;
  border-right:1px solid var(--line);
}
section[data-testid="stSidebar"] > div {
  padding:.9rem .75rem;
}
[data-testid="stSidebar"] .stRadio > label { display:none; }
[data-testid="stSidebar"] .stRadio div[role="radiogroup"] {
  gap:5px;
}
[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label {
  border-radius:12px;
  padding:.62rem .72rem;
  transition:all .15s ease;
  color:#667085;
}
[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label:hover {
  background:#F4F7FB;
}
[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label:has(input:checked) {
  background:var(--blue-soft);
  color:#2563EB;
  font-weight:750;
  box-shadow:inset 3px 0 var(--blue);
}
[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label p {
  font-size:14px;
}

/* Brand */
.planx-brand {
  display:flex;
  align-items:center;
  gap:11px;
  margin:4px 6px 22px;
}
.planx-brand-mark {
  width:38px;
  height:38px;
  border-radius:12px;
  display:flex;
  align-items:center;
  justify-content:center;
  background:linear-gradient(145deg,#2563EB,#60A5FA);
  color:white;
  font-size:20px;
  font-weight:850;
  box-shadow:0 6px 16px rgba(59,130,246,.20);
}
.planx-brand-title {
  font-size:20px;
  line-height:1.1;
  font-weight:850;
  letter-spacing:-.04em;
  color:#20385F;
}
.planx-brand-sub {
  font-size:10px;
  color:#8A97AA;
  margin-top:3px;
}

/* Hero */
.planx-hero {
  background:linear-gradient(135deg,#FFFFFF 0%,#F7FAFF 58%,#EEF5FF 100%);
  border:1px solid #E1E9F5;
  border-radius:20px;
  padding:23px 27px;
  margin-bottom:17px;
  box-shadow:0 10px 30px rgba(31,53,88,.045);
}
.planx-eyebrow {
  color:#3978D9;
  font-size:11px;
  font-weight:800;
  letter-spacing:.10em;
  margin-bottom:6px;
}
.planx-hero h1 {
  margin:0;
  font-size:31px;
  line-height:1.18;
}
.planx-hero p {
  margin:8px 0 0;
  color:#6E7D92;
  font-size:14px;
  max-width:760px;
}

/* Reusable dashboard cards */
.planx-card {
  background:var(--surface);
  border:1px solid var(--line);
  border-radius:15px;
  padding:17px 18px;
  min-height:108px;
  box-shadow:0 7px 22px rgba(31,53,88,.035);
}
.planx-card-title {
  font-size:12px;
  color:#738197;
  margin-bottom:8px;
  font-weight:700;
}
.planx-card-value {
  font-size:22px;
  color:var(--text);
  font-weight:820;
  letter-spacing:-.035em;
  font-variant-numeric:tabular-nums;
}
.planx-card-note {
  margin-top:6px;
  font-size:11px;
  color:#94A0B2;
}
.planx-card:hover {
  border-color:#C9D8F0;
  box-shadow:0 10px 26px rgba(31,53,88,.06);
}

/* Streamlit containers become soft white dashboard panels */
[data-testid="stVerticalBlockBorderWrapper"] {
  border-color:var(--line) !important;
  border-radius:15px !important;
  background:var(--surface);
  box-shadow:0 7px 22px rgba(31,53,88,.035);
}

/* Metrics */
[data-testid="stMetric"] {
  background:var(--surface);
  border:1px solid var(--line);
  border-radius:15px;
  padding:14px 17px;
  box-shadow:0 7px 22px rgba(31,53,88,.035);
}
[data-testid="stMetricLabel"] { color:#738197; }
[data-testid="stMetricValue"] {
  color:var(--text);
  font-weight:820;
  font-variant-numeric:tabular-nums;
}

/* Controls */
.stButton > button, .stFormSubmitButton > button {
  border-radius:10px;
  min-height:2.55rem;
  font-weight:750;
}
.stButton > button[kind="primary"],
.stFormSubmitButton > button[kind="primary"] {
  background:var(--blue);
  border-color:var(--blue);
}
.stTextInput input,
.stTextArea textarea,
.stSelectbox div[data-baseweb="select"] > div {
  border-radius:11px !important;
  border-color:#DCE4EF;
  background:#FFFFFF;
}
.stTextInput input:focus,
.stTextArea textarea:focus {
  border-color:#8FB5F3 !important;
  box-shadow:0 0 0 2px rgba(59,130,246,.08);
}

/* Tabs */
.stTabs [data-baseweb="tab-list"] { gap:6px; }
.stTabs [data-baseweb="tab"] {
  border-radius:10px;
  padding:8px 12px;
  color:#718096;
}
.stTabs [aria-selected="true"] {
  color:#2563EB !important;
  font-weight:750;
}

/* Data tables */
.stDataFrame {
  border:1px solid var(--line);
  border-radius:13px;
  overflow:hidden;
}

/* Empty / source states */
.planx-empty {
  background:#FFFFFF;
  border:1px dashed #CBD7E7;
  border-radius:14px;
  padding:20px;
  color:#718096;
}
.planx-source {
  display:inline-flex;
  align-items:center;
  gap:5px;
  color:#667085;
  background:#F7F9FC;
  border:1px solid #E1E7EF;
  padding:4px 8px;
  border-radius:999px;
  font-size:10px;
}
.planx-status-ok { color:#078B6D; background:#EAF9F4; border-color:#B9EBDC; }
.planx-status-wait { color:#9A6B12; background:#FFF8E8; border-color:#F6DF9C; }
.planx-status-bad { color:#C2415F; background:#FFF0F3; border-color:#F4C2CE; }

hr { border-color:var(--line) !important; }
[data-testid="stExpander"] {
  background:#FFFFFF;
  border:1px solid var(--line);
  border-radius:13px;
}
[data-testid="stExpander"] summary p { font-size:14px; }

/* Small dashboard accents */
.planx-positive { color:var(--green); }
.planx-negative { color:var(--red); }
.planx-purple { color:var(--purple); }

@media (max-width:900px) {
  .block-container { padding-left:1rem; padding-right:1rem; }
  .planx-hero { padding:20px; }
  .planx-hero h1 { font-size:27px; }
}
@media (max-width:640px) {
  .block-container { padding-top:1rem; }
  .planx-card { min-height:96px; padding:14px; }
  .planx-card-value { font-size:20px; }
}
</style>
""",
        unsafe_allow_html=True,
    )


def brand():
    st.markdown(
        """
<div class="planx-brand">
  <div class="planx-brand-mark">↗</div>
  <div>
    <div class="planx-brand-title">내 주식 대시보드</div>
    <div class="planx-brand-sub">오늘도 조금씩, 더 나은 내일을 위해</div>
  </div>
</div>
""",
        unsafe_allow_html=True,
    )


def hero(title: str, subtitle: str, eyebrow: str = "PLANX INVESTMENT OS"):
    st.markdown(
        f"""
<div class="planx-hero">
  <div class="planx-eyebrow">{html.escape(eyebrow)}</div>
  <h1>{html.escape(title)}</h1>
  <p>{html.escape(subtitle)}</p>
</div>
""",
        unsafe_allow_html=True,
    )


def card(title: str, value: str, note: str = "", status: str = ""):
    status_html = f'<div class="planx-card-note">{html.escape(status)}</div>' if status else ""
    st.markdown(
        f"""
<div class="planx-card">
  <div class="planx-card-title">{html.escape(title)}</div>
  <div class="planx-card-value">{html.escape(value)}</div>
  <div class="planx-card-note">{html.escape(note)}</div>
  {status_html}
</div>
""",
        unsafe_allow_html=True,
    )


def empty_state(title: str, message: str):
    st.markdown(
        f"""
<div class="planx-empty">
  <strong style="color:#334155">{html.escape(title)}</strong><br>
  <span>{html.escape(message)}</span>
</div>
""",
        unsafe_allow_html=True,
    )


def source_badge(label: str, state: str = "wait"):
    cls = {"ok": "planx-status-ok", "bad": "planx-status-bad"}.get(state, "planx-status-wait")
    st.markdown(
        f'<span class="planx-source {cls}">{html.escape(label)}</span>',
        unsafe_allow_html=True,
    )
