# 🔢 소인수분해 계산기

숫자를 입력하면 소인수분해 결과를 보여주는 웹 애플리케이션입니다.

## ✨ 주요 기능

- **소인수분해**: 입력한 숫자를 소인수로 분해
- **실시간 통계**: 방문자 수, 계산 횟수 등 실시간 추적
- **사용자 친화적 UI**: 직관적이고 깔끔한 인터페이스
- **상세 분석**: 소수 여부, 약수 개수 등 추가 정보 제공

## 📊 통계 기능

- 총 방문 횟수
- 고유 방문자 수
- 일별/시간별 방문 통계
- 가장 많이 계산된 숫자 순위
- 실시간 방문자 추적

## 🚀 Streamlit Cloud 배포 방법

### 1. GitHub에 코드 업로드
```bash
git init
git add .
git commit -m "Initial commit: 소인수분해 계산기"
git branch -M main
git remote add origin <your-github-repo-url>
git push -u origin main
```

### 2. Streamlit Cloud에서 배포
1. [Streamlit Cloud](https://share.streamlit.io/)에 접속
2. GitHub 계정으로 로그인
3. "New app" 클릭
4. GitHub 저장소 선택
5. 메인 파일 경로: `prime_factor_app_v2.py`
6. "Deploy!" 클릭

### 3. 환경 변수 설정 (선택사항)
- `STATS_FILE`: 통계 파일 저장 경로 (기본값: `app_stats.json`)

## 📁 파일 구조

```
├── prime_factor_app_v2.py    # 메인 애플리케이션
├── requirements.txt          # Python 의존성
├── .streamlit/
│   └── config.toml         # Streamlit 설정
├── app_stats.json          # 통계 데이터 (자동 생성)
└── README.md               # 프로젝트 설명서
```

## 🛠️ 로컬 실행

```bash
# 의존성 설치
pip install -r requirements.txt

# 애플리케이션 실행
streamlit run prime_factor_app_v2.py
```

## 📈 통계 데이터

애플리케이션은 다음 정보를 자동으로 수집합니다:
- 방문자 수 및 방문 시간
- 계산된 숫자별 사용 빈도
- 일별/시간별 트래픽 패턴

## 🔒 개인정보 보호

- IP 주소는 저장하지 않습니다
- 세션 기반의 익명 방문자 추적만 수행
- 모든 데이터는 로컬 JSON 파일에 저장

## 📝 라이선스

MIT License

## 🤝 기여

버그 리포트나 기능 제안은 이슈로 등록해주세요!
