"""Portfolio BI views built only from stored reports and account snapshots."""
from collections import defaultdict
import html

import altair as alt
import pandas as pd
import streamlit as st

GOLD = '#3B82F6'
TEAL = '#35B99A'
INK = '#4A5870'


def theme():
    """Dashboard palette aligned with the clean pastel StockDash design."""
    st.markdown('''<style>
    .stApp{background:#F5F8FC;color:#17233A}
    [data-testid="stSidebar"]{background:#FFFFFF!important;border-right:1px solid #E4EAF3}
    [data-testid="stVerticalBlockBorderWrapper"]>div{border-color:#E4EAF3!important;border-radius:15px!important;background:#FFFFFF;box-shadow:0 7px 22px rgba(31,53,88,.035)}
    [data-testid="stMetric"]{background:#FFFFFF;border:1px solid #E4EAF3;border-radius:15px;padding:16px 18px;box-shadow:0 7px 22px rgba(31,53,88,.035)}
    [data-testid="stMetricValue"]{font-family:inherit;color:#17233A;font-weight:820}
    .stButton>button[kind="primary"]{background:#3B82F6;border-color:#3B82F6;color:white}
    .px-eyebrow{font-size:11px;letter-spacing:1.5px;color:#3978D9;margin:0 0 5px}
    .px-business{padding:18px 20px;border-left:3px solid #8B72D8;background:#F7F4FF;border-radius:0 12px 12px 0;font-size:15px;line-height:1.75}
    h1,h2,h3{color:#17233A!important;letter-spacing:-.03em}
    </style>''', unsafe_allow_html=True)


def draw(chart):
    st.altair_chart(chart.configure(background='#fffdf9').configure_view(stroke=None)
                    .configure_axis(labelColor=INK,titleColor=INK,gridColor='#eee8dd',labelFontSize=13,titleFontSize=13)
                    .configure_legend(labelColor=INK,titleColor=INK,labelFontSize=13), use_container_width=True)


def overview(details, snapshot):
    """Main StockDash home: KPI row -> allocation/change panels -> comparison."""
    reports = [r for _, r, _, _ in details.values() if r]
    positions = (snapshot or {}).get("positions", [])

    st.markdown("### 오늘의 투자 현황")
    k1, k2, k3, k4 = st.columns(4, gap="medium")
    if positions:
        value = sum(float(p["value"]) for p in positions)
        pnl = sum(float(p["pnl"]) for p in positions)
        invested = value - pnl
        pnl_pct = pnl / invested * 100 if invested else 0
        k1.metric("총 평가금액", f"{value:,.0f}원")
        k2.metric("평가손익", f"{pnl:+,.0f}원", f"{pnl_pct:+.1f}%")
        k3.metric("보유종목", f"{len(positions)}개")
        k4.metric("관심·분석종목", f"{len(details)}개")
        st.caption("한국투자증권 계좌 조회 시점 기준 · 예수금 제외 · " + str(snapshot.get("fetched", "")))
    else:
        k1.metric("관심종목", f"{len(details)}개")
        k2.metric("분석 완료", f"{len(reports)}개")
        k3.metric("추가 확인 필요", f"{len(details) - len(reports)}개")
        k4.metric("계좌 상태", "연결 대기")
        st.caption("계좌를 연결하면 평가금액·손익·보유비중을 이 화면에서 함께 확인할 수 있습니다.")

    left, right = st.columns([1, 1.35], gap="large")

    with left, st.container(border=True):
        st.subheader("내 자산 구성")
        if positions:
            df = pd.DataFrame([{"종목": p["name"], "평가액": float(p["value"])} for p in positions if float(p["value"]) > 0])
            if not df.empty:
                df["비중"] = df["평가액"] / df["평가액"].sum()
                draw(
                    alt.Chart(df).mark_arc(innerRadius=62, outerRadius=105).encode(
                        theta="평가액:Q",
                        color=alt.Color(
                            "종목:N",
                            scale=alt.Scale(range=["#3B82F6", "#35B99A", "#8B72D8", "#F4A340", "#E96B9B", "#7A8AA0"]),
                            legend=alt.Legend(orient="bottom", columns=2),
                        ),
                        tooltip=[
                            "종목",
                            alt.Tooltip("평가액:Q", format=",.0f"),
                            alt.Tooltip("비중:Q", format=".1%"),
                        ],
                    ).properties(height=255)
                )
                st.caption("조회된 국내주식 평가액 기준 · 현금 제외")
        else:
            st.markdown("**계좌를 연결하면 보유 비중을 보여드립니다.**")
            st.write("현재는 관심종목을 등록해도 기업별 실적과 가치 정보를 먼저 확인할 수 있습니다.")
            st.caption("왼쪽 메뉴 → 계좌 연결")
            if details:
                st.write(" · ".join(html.escape(s["name"]) for s, _, _, _ in details.values()))

    with right, st.container(border=True):
        st.subheader("최근 기업 변화")
        if reports:
            rows = []
            for r in reports[:8]:
                f = r.get("financial") or {}
                v = r.get("valuation") or {}
                flow = r.get("flow") or {}
                rows.append({
                    "기업": r.get("name", ""),
                    "매출": f"{f.get('revenue_growth', 0):+.1f}%" if f.get("revenue_growth") is not None else "—",
                    "영업이익": f"{f.get('profit_growth', 0):+.1f}%" if f.get("profit_growth") is not None else "—",
                    "수급": "확인됨" if flow else "—",
                    "가치 참고": f"{v.get('base'):,.0f}원" if v.get("base") else "—",
                })
            st.dataframe(pd.DataFrame(rows), hide_index=True, use_container_width=True, height=270)
            st.caption("저장된 조사 결과 기준 · 실시간 시세/뉴스 전체를 뜻하지 않습니다.")
        else:
            st.markdown("**아직 분석된 기업이 없습니다.**")
            st.write("종목을 추가하고 조사 결과가 들어오면 이 영역에 핵심 변화가 모입니다.")
            st.caption("임의의 수치나 가상 데이터를 표시하지 않습니다.")

    st.subheader("최근 공시")
    notices = []
    for r in reports:
        for n in r.get("disclosures", [])[:4]:
            notices.append((n.get("date", ""), r.get("name", ""), n.get("title", ""), n.get("url", "")))
    notices.sort(reverse=True)
    if notices:
        cols = st.columns(min(3, len(notices)))
        for i, (dt, name, title, url) in enumerate(notices[:3]):
            with cols[i]:
                with st.container(border=True):
                    st.caption(dt + " · " + name)
                    st.write(title)
                    st.link_button("공시 원문", url, use_container_width=True)
    else:
        st.caption("저장된 기업의 최근 공시가 없습니다.")

    st.subheader("실적 비교")
    groups = defaultdict(list)
    for r in reports:
        f = r.get("financial")
        if f:
            key = (f["period"], f["prior_period"], f["basis"], f["currency"], f["unit"])
            groups[key].append((r, f))
    if not groups:
        empty = pd.DataFrame([{"상태": "비교 가능한 동일 기간의 실적 자료가 아직 없습니다."}])
        st.dataframe(empty, hide_index=True, use_container_width=True)
    else:
        keys = list(groups)
        key = (
            st.selectbox(
                "비교 기간·기준",
                keys,
                format_func=lambda k: f"{k[0]} 누적 / 전년 {k[1]} · {k[2]}",
                key="bi_period",
            )
            if len(keys) > 1
            else keys[0]
        )
        bars, special = [], []
        for r, f in groups[key]:
            prior, now = f["prior_operating_profit"], f["operating_profit"]
            if prior > 0:
                bars.append({"종목": r["name"], "증가율": (now / prior - 1) * 100})
            else:
                special.append(r["name"] + " · 전년 이익이 0 이하: 상세 실적 확인")
        if bars:
            df = pd.DataFrame(bars)
            draw(
                alt.Chart(df).mark_bar(cornerRadiusEnd=4).encode(
                    x=alt.X("증가율:Q", title="누적 영업이익 증가율 (%)"),
                    y=alt.Y("종목:N", sort="-x", title=None),
                    tooltip=["종목", alt.Tooltip("증가율:Q", format="+.1f")],
                ).properties(height=245)
            )
        st.caption(f"{key[0]} / {key[1]} · {key[2]} · 같은 기간과 회계기준의 기업만 비교")
        for text in special:
            st.caption(text)


def detail(r):
    a,b,c=st.columns([1.15,1,1],gap='large')
    with a,st.container(border=True):
        st.subheader('주력사업과 기업 특징')
        business=r.get('business') or r.get('summary')
        if business:st.markdown('<div class="px-business">'+html.escape(business['text'])+'</div>',unsafe_allow_html=True)
        else:st.info('사업 내용 조사 필요')
    with b,st.container(border=True):
        st.subheader('영업이익 변화')
        f=r.get('financial')
        if f:
            df=pd.DataFrame([{'기간':f['prior_period'],'영업이익':f['prior_operating_profit']},{'기간':f['period'],'영업이익':f['operating_profit']}])
            draw(alt.Chart(df).mark_bar(size=45,cornerRadiusTopLeft=4,cornerRadiusTopRight=4).encode(
                x=alt.X('기간:O',title=None,axis=alt.Axis(labelAngle=0)),y=alt.Y('영업이익:Q',title=f['unit']),
                color=alt.Color('기간:N',scale=alt.Scale(range=['#d8c8a7',GOLD]),legend=None),tooltip=['기간',alt.Tooltip('영업이익:Q',format=',.1f')]).properties(height=210))
            margin=f['operating_profit']/f['revenue']*100 if f['revenue']>0 else None
            st.caption(f"{f['basis']} · {f['currency']} {f['unit']}"+(f' · 영업이익률 {margin:.1f}%' if margin is not None else ''))
        else:st.info('같은 기간의 전년·당년 실적이 필요합니다.')
    with c,st.container(border=True):
        st.subheader('가격과 가치의 거리')
        v=r.get('valuation')
        if v:
            df=pd.DataFrame([{'구분':label,'가격':v[k]} for k,label in [('low','낮은 참고가'),('base','기본 참고가'),('high','높은 참고가'),('current_price','비교 주가')]])
            draw(alt.Chart(df).mark_point(filled=True,size=130).encode(x=alt.X('가격:Q',title='원',scale=alt.Scale(zero=False)),y=alt.Y('구분:N',title=None),color=alt.value(TEAL),tooltip=['구분','가격']).properties(height=160))
            st.metric('기본 참고가',f"{v['base']:,.0f}원")
            st.caption(f"가격 기준일 {v['price_date']} · 평가 가정은 상세 탭에서 확인")
        else:
            st.write('**평가 근거를 기다리고 있습니다.**')
            st.caption('현재 주가와 실적 전망, 적용 배수의 근거가 모이면 참고가 범위를 표시합니다.')


def peers_chart(peers):
    df=pd.DataFrame(peers['rows']).rename(columns={'name':'기업','operating_profit':'영업이익'})
    draw(alt.Chart(df).mark_bar(color=TEAL,cornerRadiusEnd=4).encode(x=alt.X('영업이익:Q',title=peers['unit']),y=alt.Y('기업:N',sort='-x',title=None),tooltip=['기업',alt.Tooltip('영업이익:Q',format=',.1f')]).properties(height=max(150,min(400,len(df)*45))))
