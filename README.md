# 🎓 학생 추천기업 정보 뷰어

학생들이 개인별로 추천받은 기업 정보를 확인할 수 있는 웹 애플리케이션입니다.

## ✨ 주요 기능

- **🔐 로그인 시스템**: 학생 ID와 비밀번호로 개인 정보 보호
- **📋 추천기업 목록**: 카드 형식으로 깔끔하게 표시
- **🚀 지원 링크**: 실제 채용 페이지로 바로 이동
- **📊 점수 분석**: 시각적 차트로 점수 패턴 분석
- **💾 데이터 다운로드**: 개인 데이터를 CSV/Excel로 다운로드

## 🚀 배포된 앱

**🌐 접속 URL**: [Streamlit Cloud에서 확인 가능]

## 📁 프로젝트 구조

```
Beta/
├── app.py                          # 메인 Streamlit 애플리케이션
├── requirements.txt                # Python 의존성
├── .streamlit/                     # Streamlit 설정
│   └── config.toml
├── student_recommendations.csv     # 학생 추천 데이터
├── job_postings.csv               # 채용 정보 및 링크
├── README.md                      # 프로젝트 설명서
└── .gitignore                     # Git 제외 파일
```

## 🛠️ 기술 스택

- **Frontend**: Streamlit
- **Data Processing**: Pandas
- **Visualization**: Plotly
- **Authentication**: Session State
- **Deployment**: Streamlit Cloud

## 📊 데이터 구조

### student_recommendations.csv
- `student_id`: 학생 ID
- `name`: 학생 이름
- `recommendation_rank`: 추천 순위
- `recommended_title`: 추천 직무명
- `recommended_company`: 추천 기업명
- `recommended_industry`: 산업 분야
- `recommended_location`: 지역
- `final_score`: 최종 점수

### job_postings.csv
- `job_id`: 채용 공고 ID
- `url`: 실제 지원 링크
- `company_name`: 기업명
- `title`: 채용 직무명

## 🔐 로그인 정보

- **학생 ID**: 본인 학번 (예: 202401020001)
- **비밀번호**: 1234

## 🚀 배포 방법

### 1. GitHub에 코드 업로드
```bash
git add .
git commit -m "Initial commit: Student recommendation viewer"
git branch -M main
git remote add origin [YOUR_GITHUB_REPO_URL]
git push -u origin main
```

### 2. Streamlit Cloud 배포
1. [Streamlit Cloud](https://streamlit.io/cloud) 접속
2. GitHub 계정으로 로그인
3. "New app" 클릭
4. 저장소 선택 및 설정:
   - **Main file path**: `app.py`
   - **Python version**: 3.10
5. "Deploy!" 클릭

### 3. 환경 변수 설정 (필요시)
- Streamlit Cloud 대시보드에서 설정 가능
- 민감한 정보는 `.streamlit/secrets.toml`에 저장

## 📱 사용법

1. **로그인**: 학생 ID와 비밀번호 입력
2. **개인 정보 확인**: 본인의 추천기업 정보만 표시
3. **상세 점수**: 📊 점수 상세 버튼으로 세부 점수 확인
4. **지원하기**: 🚀 지원하기 버튼으로 채용 페이지 이동
5. **데이터 다운로드**: 개인 데이터를 CSV/Excel로 다운로드

## 🔧 로컬 개발

```bash
# 의존성 설치
pip install -r requirements.txt

# 앱 실행
streamlit run app.py
```

## 📈 향후 개선 계획

- [ ] 데이터베이스 연동
- [ ] 보안 강화 (JWT 토큰)
- [ ] 관리자 페이지
- [ ] 실시간 알림 기능
- [ ] 모바일 최적화

## 🤝 기여하기

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다.

## 📞 문의

프로젝트에 대한 문의사항이 있으시면 이슈를 생성해주세요.

---

**개발**: Streamlit  
**버전**: 2.0.0 (로그인 기능 추가)  
**최종 업데이트**: 2025년 1월
