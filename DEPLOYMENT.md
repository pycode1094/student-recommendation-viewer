# 🚀 배포 가이드

## 1. Streamlit Cloud (추천 - 무료)

### 단계별 배포 방법

1. **GitHub 저장소 생성**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin https://github.com/yourusername/your-repo-name.git
   git push -u origin main
   ```

2. **Streamlit Cloud 연결**
   - [Streamlit Cloud](https://streamlit.io/cloud)에 가입
   - "New app" 클릭
   - GitHub 저장소 선택
   - `app.py` 파일 경로 지정
   - "Deploy!" 클릭

3. **배포 완료**
   - 자동으로 URL 생성 (예: `https://your-app-name.streamlit.app`)
   - GitHub에 푸시할 때마다 자동 재배포

### 장점
- ✅ 완전 무료
- ✅ 자동 배포
- ✅ HTTPS 자동 설정
- ✅ 사용량 제한 없음

---

## 2. Heroku

### 사전 준비
```bash
# Heroku CLI 설치
# https://devcenter.heroku.com/articles/heroku-cli

# 로그인
heroku login
```

### 배포 방법
```bash
# Heroku 앱 생성
heroku create your-app-name

# 환경변수 설정
heroku config:set STREAMLIT_SERVER_PORT=$PORT
heroku config:set STREAMLIT_SERVER_ADDRESS=0.0.0.0

# 배포
git push heroku main

# 앱 열기
heroku open
```

### 장점
- ✅ 무료 티어 제공
- ✅ Git 기반 배포
- ✅ 자동 HTTPS

---

## 3. Docker

### 로컬 Docker 실행
```bash
# 이미지 빌드
docker build -t student-recommendations .

# 컨테이너 실행
docker run -p 8501:8501 student-recommendations
```

### Docker Hub 배포
```bash
# 이미지 태그
docker tag student-recommendations yourusername/student-recommendations

# Docker Hub 푸시
docker push yourusername/student-recommendations

# 다른 서버에서 실행
docker run -p 8501:8501 yourusername/student-recommendations
```

### 장점
- ✅ 환경 독립성
- ✅ 확장성
- ✅ 다양한 클라우드 지원

---

## 4. Vercel (대안)

### 배포 방법
1. [Vercel](https://vercel.com)에 가입
2. GitHub 저장소 연결
3. Python 런타임 선택
4. 자동 배포

### 장점
- ✅ 빠른 배포
- ✅ 글로벌 CDN
- ✅ 무료 티어

---

## 5. 로컬 테스트

### 개발 환경 실행
```bash
# 의존성 설치
pip install -r requirements.txt

# 앱 실행
streamlit run app.py

# 브라우저에서 확인
# http://localhost:8501
```

### 프로덕션 환경 실행
```bash
# 프로덕션 모드
streamlit run app.py --server.port=8501 --server.address=0.0.0.0
```

---

## 🔧 환경변수 설정

### Streamlit Cloud
- 대시보드 → Settings → Secrets에서 설정

### Heroku
```bash
heroku config:set VARIABLE_NAME=value
```

### Docker
```bash
docker run -e VARIABLE_NAME=value -p 8501:8501 your-image
```

---

## 📊 모니터링

### 로그 확인
```bash
# Streamlit Cloud: 대시보드에서 확인
# Heroku: heroku logs --tail
# Docker: docker logs container_id
```

### 성능 모니터링
- Streamlit Cloud: 자동 제공
- Heroku: New Relic 애드온
- Docker: Prometheus + Grafana

---

## 🚨 문제 해결

### 일반적인 문제들

1. **포트 충돌**
   ```bash
   # 다른 포트 사용
   streamlit run app.py --server.port=8502
   ```

2. **메모리 부족**
   - 데이터 샘플링
   - 캐싱 활용
   - 이미지 압축

3. **의존성 문제**
   ```bash
   # 가상환경 사용
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

---

## 📱 모바일 최적화

### 반응형 디자인
- Streamlit 자동 지원
- 테이블 스크롤
- 차트 크기 조정

### 성능 최적화
- 데이터 캐싱
- 이미지 압축
- 지연 로딩

---

## 🔒 보안 고려사항

### 데이터 보호
- 민감한 정보는 환경변수로 관리
- HTTPS 사용
- 접근 제어 설정

### API 보안
- Rate limiting
- 인증 토큰
- CORS 설정

---

## 📈 확장성

### 트래픽 증가 대응
- 로드 밸런서
- 데이터베이스 최적화
- CDN 활용

### 기능 확장
- 사용자 인증
- 데이터베이스 연동
- 외부 API 연동
