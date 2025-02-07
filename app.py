import streamlit as st
import pandas as pd
import openpyxl

# 🔹 1. 데이터 불러오기
file_path = "경찰테스트_결과.xlsx"

try:
    data = pd.read_excel(file_path)
except FileNotFoundError:
    st.error(f"❌ '{file_path}' 파일을 찾을 수 없습니다. 먼저 예측 모델을 실행하세요.")
    st.stop()

# 🔹 2. 컬럼명 정리
data.columns = data.columns.str.strip()  # 공백 제거

# 🔹 3. 지역 컬럼 복원 (get_dummies 변환된 형식 처리)
지역컬럼들 = [col for col in data.columns if col.startswith("지역_")]

if 지역컬럼들:
    # 🔹 "지역_" 접두사를 제거하고, 값이 1인 컬럼의 이름을 가져옴
    data["지역"] = data[지역컬럼들].idxmax(axis=1).str.replace("지역_", "")

    # 🔹 불필요한 원-핫 인코딩 컬럼 삭제
    data.drop(columns=지역컬럼들, inplace=True)

# 🔹 4. "지역" 컬럼 확인
if "지역" not in data.columns:
    st.error("❌ '지역' 컬럼을 찾을 수 없습니다. 엑셀 파일을 확인하세요.")
    st.stop()

# 🔹 5. UI 구성
st.subheader("🚔 경찰 공채 필기시험 합격 점수 예측")
st.write("지역을 선택하면 예상 합격 점수를 확인할 수 있습니다!")

# 🔹 6. 드롭다운으로 지역 선택
지역목록 = sorted(data["지역"].unique())  # 가나다순 정렬
선택지역 = st.selectbox("📍 지역을 선택하세요", 지역목록)

# 🔹 7. 선택한 지역의 예측 점수 표시
예측점수 = data.loc[data["지역"] == 선택지역, "합격예측점수"].values

if len(예측점수) > 0:
    st.subheader(f"📌 {선택지역} 예상 합격 점수: **{예측점수[0]:.2f}** 점")
else:
    st.error("해당 지역의 데이터가 없습니다.")

# 🔹 8. 데이터 다운로드 버튼
st.download_button(
    label="📥 예측 결과 다운로드",
    data=data.to_csv(index=False).encode("utf-8"),
    file_name="경찰테스트_결과.csv",
    mime="text/csv"
)
