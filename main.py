import streamlit as st
import pandas as pd
import altair as alt

st.set_page_config(
    page_title="Country Analysis",
    page_icon="🌍",
    layout="wide"
)

st.title("🌍 유형별 국가 분석 대시보드")
st.markdown("""
이 앱은 **국가별 유형 분포 데이터**를 기반으로  
선택한 유형이 **가장 높은 국가 TOP 10**을 시각적으로 보여줍니다.
""")

# --- 데이터 불러오기 ---
uploaded_file = st.file_uploader("📂 CSV 파일을 업로드하세요 (예: countriesMBTI_16types.csv)", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
else:
    st.info("파일이 업로드되지 않았습니다. 예시로 countriesMBTI_16types.csv 파일을 업로드해보세요.")
    st.stop()

# --- 데이터 기본 검사 ---
if "Country" not in df.columns:
    st.error("❌ 'Country' 컬럼이 데이터에 없습니다. 국가명을 나타내는 열 이름을 'Country'로 수정해주세요.")
    st.stop()

# MBTI 유형 목록 추출 (Country 제외)
mbti_cols = [col for col in df.columns if col != "Country"]

# --- 사용자 입력 ---
selected_type = st.selectbox("🔍 분석할 MBTI 유형을 선택하세요", mbti_cols, index=0)

# --- 분석 ---
top10 = (
    df[["Country", selected_type]]
    .sort_values(by=selected_type, ascending=False)
    .head(10)
)

st.subheader(f"🏆 {selected_type} 유형이 높은 국가 TOP 10")
st.dataframe(top10.style.format({selected_type: "{:.2f}"}))

# --- 시각화 (Altair) ---
chart = (
    alt.Chart(top10)
    .mark_bar(cornerRadiusTopLeft=6, cornerRadiusTopRight=6)
    .encode(
        x=alt.X(selected_type, title=f"{selected_type} 비율", sort="descending"),
        y=alt.Y("Country", sort="-x", title="국가"),
        color=alt.Color(selected_type, scale=alt.Scale(scheme="tealblues")),
        tooltip=["Country", alt.Tooltip(selected_type, format=".2f")],
    )
    .properties(
        width=700,
        height=400,
        title=f"{selected_type} 유형 상위 10개국"
    )
    .configure_axis(labelFontSize=12, titleFontSize=14)
    .configure_title(fontSize=18, anchor="start")
    .configure_view(strokeWidth=0)
)

st.altair_chart(chart, use_container_width=True)

# --- 하단 설명 ---
st.markdown("""
---
💡 **Tip:**  
- 다른 MBTI 유형을 선택해보며 국가별 분포 차이를 확인하세요.  
- Altair 그래프는 마우스 오버 시 값이 표시됩니다.
""")
