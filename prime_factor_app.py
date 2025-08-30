import streamlit as st
import math

def prime_factors(n):
    """주어진 숫자를 소인수분해하는 함수"""
    factors = []
    d = 2
    while d * d <= n:
        while n % d == 0:
            factors.append(d)
            n //= d
        d += 1
    if n > 1:
        factors.append(n)
    return factors

def format_prime_factors(factors):
    """소인수분해 결과를 보기 좋게 포맷팅하는 함수"""
    if not factors:
        return "1"
    
    # 각 소인수의 개수를 세기
    factor_count = {}
    for factor in factors:
        factor_count[factor] = factor_count.get(factor, 0) + 1
    
    # 결과 문자열 생성
    result_parts = []
    for factor in sorted(factor_count.keys()):
        count = factor_count[factor]
        if count == 1:
            result_parts.append(str(factor))
        else:
            result_parts.append(f"{factor}^{count}")
    
    return " × ".join(result_parts)

# Streamlit 앱 설정
st.set_page_config(
    page_title="소인수분해 계산기",
    page_icon="🔢",
    layout="wide"
)

# 제목과 설명
st.title("🔢 소인수분해 계산기")
st.markdown("---")
st.write("숫자를 입력하면 소인수분해 결과를 보여줍니다.")

# 사이드바에 정보 표시
with st.sidebar:
    st.header("ℹ️ 사용법")
    st.write("1. 아래 입력창에 숫자를 입력하세요")
    st.write("2. Enter를 누르거나 계산 버튼을 클릭하세요")
    st.write("3. 소인수분해 결과를 확인하세요")
    
    st.markdown("---")
    st.header("📚 소인수란?")
    st.write("소인수는 1보다 큰 자연수 중에서 1과 자기 자신만을 약수로 가지는 수입니다.")
    st.write("예: 2, 3, 5, 7, 11, 13, ...")

# 메인 입력 영역
col1, col2 = st.columns([3, 1])

with col1:
    # 숫자 입력
    number_input = st.text_input(
        "분해할 숫자를 입력하세요:",
        placeholder="예: 100, 1234, 999999",
        help="양의 정수를 입력해주세요"
    )

with col2:
    st.write("")
    st.write("")
    calculate_button = st.button("🔍 계산하기", type="primary")

# 계산 및 결과 표시
if calculate_button or (number_input and number_input.strip()):
    try:
        # 입력값 검증
        if not number_input.strip():
            st.warning("숫자를 입력해주세요.")
        else:
            number = int(number_input.strip())
            
            if number <= 0:
                st.error("양의 정수를 입력해주세요.")
            elif number == 1:
                st.info("1은 소수가 아닙니다.")
                st.write("**소인수분해 결과:** 1")
            else:
                # 소인수분해 수행
                factors = prime_factors(number)
                
                # 결과 표시
                st.success(f"✅ {number}의 소인수분해가 완료되었습니다!")
                
                # 결과를 카드 형태로 표시
                col_result1, col_result2 = st.columns(2)
                
                with col_result1:
                    st.markdown("### 📊 소인수분해 결과")
                    st.markdown(f"**{number} = {format_prime_factors(factors)}**")
                    
                    # 개별 소인수 표시
                    if len(factors) > 1:
                        st.write("**개별 소인수:**")
                        for i, factor in enumerate(factors, 1):
                            st.write(f"{i}. {factor}")
                
                with col_result2:
                    st.markdown("### 📈 통계 정보")
                    st.write(f"**총 소인수 개수:** {len(factors)}")
                    
                    # 고유한 소인수 개수
                    unique_factors = len(set(factors))
                    st.write(f"**고유 소인수 개수:** {unique_factors}")
                    
                    # 가장 큰 소인수
                    max_factor = max(factors)
                    st.write(f"**가장 큰 소인수:** {max_factor}")
                
                # 추가 정보
                st.markdown("---")
                st.markdown("### 🔍 상세 분석")
                
                # 소수 여부 확인
                if len(factors) == 1 and factors[0] == number:
                    st.info(f"🎉 {number}은(는) 소수입니다!")
                else:
                    st.write(f"**소수 여부:** {number}은(는) 소수가 아닙니다.")
                
                # 약수 개수 계산
                def count_divisors(factors):
                    factor_count = {}
                    for factor in factors:
                        factor_count[factor] = factor_count.get(factor, 0) + 1
                    
                    total_divisors = 1
                    for count in factor_count.values():
                        total_divisors *= (count + 1)
                    return total_divisors
                
                divisor_count = count_divisors(factors)
                st.write(f"**약수 개수:** {divisor_count}개")
                
    except ValueError:
        st.error("올바른 숫자를 입력해주세요. (예: 123, 456)")
    except Exception as e:
        st.error(f"오류가 발생했습니다: {str(e)}")

# 예시 표시
st.markdown("---")
st.markdown("### 💡 예시")
example_cols = st.columns(3)

with example_cols[0]:
    st.markdown("**작은 수 예시**")
    st.write("12 = 2² × 3")
    st.write("15 = 3 × 5")
    st.write("20 = 2² × 5")

with example_cols[1]:
    st.markdown("**중간 수 예시**")
    st.write("100 = 2² × 5²")
    st.write("144 = 2⁴ × 3²")
    st.write("200 = 2³ × 5²")

with example_cols[2]:
    st.markdown("**큰 수 예시**")
    st.write("1000 = 2³ × 5³")
    st.write("2024 = 2³ × 11 × 23")
    st.write("9999 = 3² × 11 × 101")

# 푸터
st.markdown("---")
st.markdown("🔢 **소인수분해 계산기** - Streamlit으로 제작되었습니다.")