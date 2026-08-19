import streamlit as st
import numpy as np

# 1. 페이지 기본 설정
st.set_page_config(
    page_title="2형 당뇨병 발병 예측 CDSS",
    page_icon="🩺",
    layout="centered"
)

st.title("🩺 2형 당뇨병 발병 위험 예측 CDSS")
st.caption("본 시스템은 입력된 임상 인자를 바탕으로 2형 당뇨병 위험도를 평가하는 임상결정지원시스템(CDSS) 프로토타입입니다.")
st.markdown("---")

# 2. 사용자 입력 폼 (UI)
st.subheader("📋 환자 정보 입력")

col1, col2 = st.columns(2)

with col1:
    age = st.number_input("나이 (세)", min_value=1, max_value=120, value=45, step=1)
    family_history = st.radio("당뇨병 가족력 (직계)", options=["무", "유"], index=0)

with col2:
    fpg = st.number_input("공복 혈당 (FPG, mg/dL)", min_value=50, max_value=300, value=95, step=1)
    hba1c = st.number_input("당화혈색소 (HbA1c, %)", min_value=3.0, max_value=15.0, value=5.4, step=0.1)

has_family_history = 1 if family_history == "유" else 0

# 3. 위험도 계산 함수
def predict_diabetes_risk(age, family_history, fpg, hba1c):
    is_diabetic = (fpg >= 126) or (hba1c >= 6.5)
    is_prediabetes = (100 <= fpg < 126) or (5.7 <= hba1c < 6.5)
    
    score = -6.0 
    score += age * 0.035
    score += family_history * 0.8
    score += (fpg - 90) * 0.05
    score += (hba1c - 5.0) * 1.5
    
    prob = 1 / (1 + np.exp(-score))
    return is_diabetic, is_prediabetes, prob

st.markdown("---")

# 4. 결과 출력 (use_container_width 옵션 제거됨)
if st.button("🔍 당뇨병 위험도 분석 실행"):
    is_diabetic, is_prediabetes, risk_prob = predict_diabetes_risk(age, has_family_history, fpg, hba1c)
    
    st.subheader("📊 분석 결과 및 CDSS 권고사항")
    
    if is_diabetic:
        st.error("🚨 **당뇨병 유소견 (High Risk / Diabetic Range)**")
        st.write("입력된 혈당 수치가 당뇨병 진단 기준(공복혈당 126 mg/dL 이상 또는 HbA1c 6.5% 이상)에 도달했습니다.")
    elif is_prediabetes:
        st.warning("⚠️ **당뇨병 전단계 (Prediabetes)**")
        st.write("현재 당뇨병 전단계 수치에 해당하며, 향후 2형 당뇨병으로 진행될 위험이 높습니다.")
    else:
        st.success("✅ **정상 범위 (Normal Range)**")
        st.write("현재 주요 혈당 수치는 정상 범위 내에 있습니다.")
        
    st.metric(label="2형 당뇨병 예측 발병 위험 확률", value=f"{risk_prob * 100:.1f} %")
    st.progress(float(risk_prob))

    with st.expander("💡 임상 가이드라인 기반 권고사항 보기"):
        if is_diabetic:
            st.markdown("- 전문의 상담 및 정밀 검사(재검사 또는 75g OGTT) 권장\n- 생활습관 교정 및 약물 치료 검토 필요")
        elif is_prediabetes or risk_prob > 0.4:
            st.markdown("- 체중 5~7% 감량 및 주 150분 이상 중강도 유산소 운동 권장\n- 6개월~1년 주기 혈당 추적 관찰")
        else:
            st.markdown("- 균형 잡힌 식단과 규칙적인 운동 유지\n- 연 1회 정기 검진 권장")
