import os
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="무신사 브랜드 리뷰 감성 분석",
    page_icon="👗",
    layout="wide",
)

st.markdown("""
<style>
    .main { background-color: #fafafa; }
    .metric-card {
        background: white; border-radius: 12px;
        padding: 20px 24px; box-shadow: 0 1px 4px rgba(0,0,0,0.08);
        text-align: center;
    }
    .metric-label { font-size: 13px; color: #888; margin-bottom: 6px; }
    .metric-value { font-size: 32px; font-weight: 700; color: #1a1a1a; }
    .metric-sub   { font-size: 12px; color: #aaa; margin-top: 4px; }
</style>
""", unsafe_allow_html=True)

SENTIMENT_COLOR = {"positive": "#4CAF50", "neutral": "#FFC107", "negative": "#F44336"}
BRAND_COLOR     = {"제멋": "#7B68EE", "트래블": "#FF8C69", "필루미네이트": "#66CDAA"}
BRANDS          = ["전체", "제멋", "트래블", "필루미네이트"]

# ── 데이터 로드 ───────────────────────────────────────────────
@st.cache_data
def load_data():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    df = pd.read_parquet(os.path.join(base_dir, "tableau_aspects.parquet"))
    return df

df_all = load_data()
df_classified = df_all[df_all["topic_category"] != "아웃라이어"]
CATEGORIES = sorted(df_classified["topic_category"].dropna().unique())

# ── 공통 함수 ─────────────────────────────────────────────────
def cat_analysis(df):
    col_l, col_r = st.columns([1, 2])
    with col_l:
        st.markdown("#### 감성 분포")
        sent_cnt = df["sentiment"].value_counts().reset_index()
        sent_cnt.columns = ["sentiment", "count"]
        sent_cnt["label"] = sent_cnt["sentiment"].map(
            {"positive": "긍정", "neutral": "중립", "negative": "부정"}
        )
        fig = px.pie(
            sent_cnt, values="count", names="label", color="sentiment",
            color_discrete_map={"positive": "#4CAF50", "neutral": "#FFC107", "negative": "#F44336"},
            hole=0.45,
        )
        fig.update_traces(textposition="outside", textinfo="percent+label")
        fig.update_layout(showlegend=False, height=300, margin=dict(t=10, b=10))
        st.plotly_chart(fig, use_container_width=True)

    with col_r:
        st.markdown("#### 카테고리별 문장 수")
        cat_cnt = (
            df.groupby("topic_category").size()
            .reset_index(name="count").sort_values("count", ascending=True)
        )
        fig2 = px.bar(
            cat_cnt, x="count", y="topic_category", orientation="h",
            color_discrete_sequence=["#7B68EE"],
            labels={"count": "문장 수", "topic_category": ""},
        )
        fig2.update_layout(height=300, margin=dict(t=10, b=10))
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown("#### 카테고리별 감성 비율 (부정 비율 순)")
    cat_sent = df.groupby(["topic_category", "sentiment"]).size().reset_index(name="count")
    cat_total = cat_sent.groupby("topic_category")["count"].transform("sum")
    cat_sent["ratio"] = cat_sent["count"] / cat_total * 100
    neg_order = (
        cat_sent[cat_sent["sentiment"] == "negative"]
        .set_index("topic_category")["ratio"]
        .sort_values(ascending=False).index.tolist()
    )
    fig3 = px.bar(
        cat_sent, x="ratio", y="topic_category", color="sentiment",
        orientation="h", barmode="stack",
        color_discrete_map=SENTIMENT_COLOR,
        labels={"ratio": "비율 (%)", "topic_category": "", "sentiment": "감성"},
        category_orders={"topic_category": neg_order, "sentiment": ["negative", "neutral", "positive"]},
    )
    fig3.update_layout(height=400, margin=dict(t=10, b=10))
    st.plotly_chart(fig3, use_container_width=True)


def sample_viewer(df, key_suffix=""):
    st.markdown("#### 📝 샘플 문장 뷰어")
    col_s1, col_s2 = st.columns(2)
    with col_s1:
        view_cat = st.selectbox("카테고리", options=CATEGORIES, key=f"cat{key_suffix}")
    with col_s2:
        view_sent = st.selectbox(
            "감성", options=["negative", "positive", "neutral"],
            format_func=lambda x: {"positive": "긍정", "neutral": "중립", "negative": "부정"}[x],
            key=f"sent{key_suffix}",
        )
    pool = df[(df["topic_category"] == view_cat) & (df["sentiment"] == view_sent)]
    if len(pool) == 0:
        st.info("해당 조건의 문장이 없어요.")
    else:
        cols = ["sentence", "브랜드", "평점"] if "브랜드" in pool.columns else ["sentence", "평점"]
        sample = pool.sample(min(10, len(pool)), random_state=42)[cols].rename(columns={"sentence": "문장"})
        st.dataframe(sample, use_container_width=True, hide_index=True)


# ── 헤더 ──────────────────────────────────────────────────────
st.markdown("## 👗 무신사 브랜드 리뷰 감성 분석")
st.markdown("KcELECTRA 기반 ABSA — 제멋 · 트래블 · 필루미네이트")
st.divider()

# ── 사이드바 ──────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 🔧 필터")
    brand_filter = st.selectbox("브랜드", options=BRANDS)
    sentiment_filter = st.multiselect(
        "감성 유형",
        options=["positive", "neutral", "negative"],
        default=["positive", "neutral", "negative"],
        format_func=lambda x: {"positive": "✅ 긍정", "neutral": "😐 중립", "negative": "❌ 부정"}[x],
    )
    category_filter = st.multiselect(
        "카테고리", options=CATEGORIES, default=[], placeholder="전체 카테고리",
    )
    score_min = st.slider("최소 감성 신뢰도", 0.3, 1.0, 0.5, 0.05)
    st.markdown("---")
    st.caption(f"총 문장 수: {len(df_all):,}개")
    st.caption(f"분류된 문장: {len(df_classified):,}개")

# ── 필터 적용 ─────────────────────────────────────────────────
filtered = df_classified.copy()
if brand_filter != "전체":
    filtered = filtered[filtered["브랜드"] == brand_filter]
if sentiment_filter:
    filtered = filtered[filtered["sentiment"].isin(sentiment_filter)]
if category_filter:
    filtered = filtered[filtered["topic_category"].isin(category_filter)]
filtered = filtered[filtered["sent_score"] >= score_min]

# ── KPI 카드 ──────────────────────────────────────────────────
total     = len(filtered)
pos_r     = (filtered["sentiment"] == "positive").sum() / total * 100 if total else 0
neg_r     = (filtered["sentiment"] == "negative").sum() / total * 100 if total else 0
avg_rating = filtered["평점"].mean() if total else 0

c1, c2, c3, c4 = st.columns(4)
for col, label, value, sub in [
    (c1, "분석 문장 수",  f"{total:,}",       "개"),
    (c2, "긍정 비율",    f"{pos_r:.1f}%",    "positive"),
    (c3, "부정 비율",    f"{neg_r:.1f}%",    "negative"),
    (c4, "평균 평점",    f"{avg_rating:.2f}", "/ 5.0"),
]:
    with col:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">{label}</div>
            <div class="metric-value">{value}</div>
            <div class="metric-sub">{sub}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── 탭 ────────────────────────────────────────────────────────
if brand_filter == "전체":
    tab1, tab2, tab3 = st.tabs(["📊 브랜드 비교", "📂 카테고리 분석", "📝 샘플 문장"])

    with tab1:
        col_l, col_r = st.columns(2)
        with col_l:
            st.markdown("#### 브랜드별 감성 비율")
            brand_sent = filtered.groupby(["브랜드", "sentiment"]).size().reset_index(name="count")
            brand_total = brand_sent.groupby("브랜드")["count"].transform("sum")
            brand_sent["ratio"] = brand_sent["count"] / brand_total * 100
            fig = px.bar(
                brand_sent, x="브랜드", y="ratio", color="sentiment",
                color_discrete_map=SENTIMENT_COLOR, barmode="stack",
                labels={"ratio": "비율 (%)", "sentiment": "감성"},
                category_orders={"sentiment": ["negative", "neutral", "positive"]},
            )
            fig.update_layout(height=320, margin=dict(t=10, b=10))
            st.plotly_chart(fig, use_container_width=True)

        with col_r:
            st.markdown("#### 브랜드별 문장 수")
            brand_cnt = filtered.groupby("브랜드").size().reset_index(name="count")
            fig2 = px.bar(
                brand_cnt, x="브랜드", y="count", color="브랜드",
                color_discrete_map=BRAND_COLOR,
                labels={"count": "문장 수"},
            )
            fig2.update_layout(height=320, margin=dict(t=10, b=10), showlegend=False)
            st.plotly_chart(fig2, use_container_width=True)

        st.markdown("#### 브랜드 × 카테고리별 부정 비율")
        cross = filtered.groupby(["브랜드", "topic_category", "sentiment"]).size().reset_index(name="count")
        cross_total = cross.groupby(["브랜드", "topic_category"])["count"].transform("sum")
        cross["ratio"] = cross["count"] / cross_total * 100
        neg_cross = (
            cross[cross["sentiment"] == "negative"]
            .pivot(index="topic_category", columns="브랜드", values="ratio")
            .fillna(0).reset_index()
        )
        fig3 = px.bar(
            neg_cross.melt(id_vars="topic_category", var_name="브랜드", value_name="부정비율"),
            x="부정비율", y="topic_category", color="브랜드",
            orientation="h", barmode="group",
            color_discrete_map=BRAND_COLOR,
            labels={"topic_category": "", "부정비율": "부정 비율 (%)"},
        )
        fig3.update_layout(height=420, margin=dict(t=10, b=10))
        st.plotly_chart(fig3, use_container_width=True)

    with tab2:
        cat_analysis(filtered)

    with tab3:
        sample_viewer(filtered, key_suffix="_all")

else:
    tab1, tab2 = st.tabs(["📂 카테고리 분석", "📝 샘플 문장"])
    with tab1:
        cat_analysis(filtered)
    with tab2:
        sample_viewer(filtered, key_suffix=f"_{brand_filter}")

st.divider()
st.caption("📊 무신사 브랜드 리뷰 감성 분석 | KcELECTRA 기반 ABSA")
