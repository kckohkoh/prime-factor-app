import streamlit as st
import math
import json
import os
from datetime import datetime, date
import time
import hashlib

# 접속 통계를 저장할 파일 경로
STATS_FILE = "app_stats.json"

def load_stats():
    """통계 데이터를 로드하는 함수"""
    try:
        if os.path.exists(STATS_FILE):
            with open(STATS_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
    except Exception:
        pass
    
    # 기본 통계 구조
    return {
        "total_visits": 0,
        "unique_visitors": 0,
        "daily_visits": {},
        "hourly_visits": {},
        "visitor_ips": {},
        "last_visit": "",
        "calculation_count": 0,
        "most_calculated_numbers": {}
    }

def save_stats(stats):
    """통계 데이터를 저장하는 함수"""
    try:
        with open(STATS_FILE, 'w', encoding='utf-8') as f:
            json.dump(stats, f, ensure_ascii=False, indent=2)
    except Exception as e:
        st.error(f"통계 저장 중 오류: {e}")

def update_visit_stats():
    """방문자 통계를 업데이트하는 함수"""
    stats = load_stats()
    
    # 현재 시간 정보
    now = datetime.now()
    today = now.strftime("%Y-%m-%d")
    current_hour = now.strftime("%H")
    
    # 총 방문 횟수 증가
    stats["total_visits"] += 1
    
    # 일별 방문 통계
    if today not in stats["daily_visits"]:
        stats["daily_visits"][today] = 0
    stats["daily_visits"][today] += 1
    
    # 시간별 방문 통계
    if current_hour not in stats["hourly_visits"]:
        stats["hourly_visits"][current_hour] = 0
    stats["hourly_visits"][current_hour] += 1
    
    # 마지막 방문 시간 업데이트
    stats["last_visit"] = now.strftime("%Y-%m-%d %H:%M:%S")
    
    # 고유 방문자 추적 (세션 기반)
    if "visitor_id" not in st.session_state:
        # 간단한 방문자 ID 생성 (실제로는 더 정교한 방법 사용)
        visitor_id = hashlib.md5(f"{time.time()}_{os.getpid()}".encode()).hexdigest()[:8]
        st.session_state.visitor_id = visitor_id
        
        if visitor_id not in stats["visitor_ips"]:
            stats["visitor_ips"][visitor_id] = {
                "first_visit": now.strftime("%Y-%m-%d %H:%M:%S"),
                "visit_count": 0
            }
            stats["unique_visitors"] += 1
        
        stats["visitor_ips"][visitor_id]["visit_count"] += 1
        stats["visitor_ips"][visitor_id]["last_visit"] = now.strftime("%Y-%m-%d %H:%M:%S")
    
    save_stats(stats)
    return stats

def update_calculation_stats(number):
    """계산 통계를 업데이트하는 함수"""
    stats = load_stats()
    
    # 총 계산 횟수 증가
    stats["calculation_count"] += 1
    
    # 가장 많이 계산된 숫자 추적
    number_str = str(number)
    if number_str not in stats["most_calculated_numbers"]:
        stats["most_calculated_numbers"][number_str] = 0
    stats["most_calculated_numbers"][number_str] += 1
    
    save_stats(stats)

def display_stats(stats):
    """통계를 표시하는 함수"""
    st.markdown("### 📊 접속 통계")
    
    # 기본 통계
    col1, col2 = st.columns(2)
    with col1:
        st.metric("총 방문 횟수", f"{stats['total_visits']:,}")
        st.metric("고유 방문자", f"{stats['unique_visitors']:,}")
    
    with col2:
        st.metric("총 계산 횟수", f"{stats['calculation_count']:,}")
        if stats['last_visit']:
            st.metric("마지막 방문", stats['last_visit'][:16])
    
    # 일별 방문 통계
    if stats['daily_visits']:
        st.markdown("#### 📅 일별 방문 통계")
        daily_data = dict(sorted(stats['daily_visits'].items(), key=lambda x: x[0], reverse=True)[:7])
        
        daily_cols = st.columns(len(daily_data))
        for i, (day, count) in enumerate(daily_data.items()):
            with daily_cols[i]:
                st.metric(day[5:], count)  # MM-DD 형식으로 표시
    
    # 시간별 방문 통계
    if stats['hourly_visits']:
        st.markdown("#### 🕐 시간별 방문 통계")
        hourly_data = dict(sorted(stats['hourly_visits'].items()))
        
        hourly_cols = st.columns(6)
        for i in range(6):
            with hourly_cols[i]:
                start_hour = i * 4
                end_hour = start_hour + 3
                total_count = sum(stats['hourly_visits'].get(str(h).zfill(2), 0) 
                                for h in range(start_hour, end_hour + 1))
                st.metric(f"{start_hour:02d}-{end_hour:02d}시", total_count)
    
    # 가장 많이 계산된 숫자
    if stats['most_calculated_numbers']:
        st.markdown("#### 🔢 가장 많이 계산된 숫자")
        top_numbers = sorted(stats['most_calculated_numbers'].items(), 
                           key=lambda x: x[1], reverse=True)[:5]
        
        for number, count in top_numbers:
            st.write(f"**{number}**: {count}회")

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

# 페이지 로드 시 방문 통계 업데이트
if "page_loaded" not in st.session_state:
    update_visit_stats()
    st.session_state.page_loaded = True

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
    
    st.markdown("---")
    st.header("📈 실시간 통계")
    
    # 실시간 통계 표시
    stats = load_stats()
    
    # 간단한 통계 요약
    col1, col2 = st.columns(2)
    with col1:
        st.metric("총 방문", f"{stats['total_visits']:,}")
        st.metric("고유 방문자", f"{stats['unique_visitors']:,}")
    
    with col2:
        st.metric("총 계산", f"{stats['calculation_count']:,}")
        if stats['last_visit']:
            st.caption(f"마지막: {stats['last_visit'][:16]}")
    
    # 오늘 방문자 수
    today = datetime.now().strftime("%Y-%m-%d")
    today_visits = stats['daily_visits'].get(today, 0)
    st.metric("오늘 방문", f"{today_visits:,}")
    
    # 통계 상세보기 버튼
    if st.button("📊 상세 통계 보기", type="secondary"):
        st.session_state.show_detailed_stats = not st.session_state.get('show_detailed_stats', False)
    
    # 상세 통계 표시
    if st.session_state.get('show_detailed_stats', False):
        st.markdown("#### 📅 최근 7일")
        recent_days = dict(sorted(stats['daily_visits'].items(), key=lambda x: x[0], reverse=True)[:7])
        for day, count in recent_days.items():
            st.write(f"**{day[5:]}**: {count}회")
        
        st.markdown("#### 🔢 인기 숫자")
        top_numbers = sorted(stats['most_calculated_numbers'].items(), 
                           key=lambda x: x[1], reverse=True)[:3]
        for number, count in top_numbers:
            st.write(f"**{number}**: {count}회")

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
                
                # 계산 통계 업데이트
                update_calculation_stats(number)
                
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

# 접속 통계 표시
st.markdown("---")
st.markdown("### 📊 접속 통계")
display_stats(load_stats())