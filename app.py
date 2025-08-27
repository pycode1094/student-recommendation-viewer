import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
from io import BytesIO
import hashlib

# 페이지 설정
st.set_page_config(
    page_title="학생 추천기업 뷰어",
    page_icon="🎓",
    layout="wide"
)

# 세션 상태 초기화
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'current_student' not in st.session_state:
    st.session_state.current_student = None
if 'show_scores' not in st.session_state:
    st.session_state.show_scores = None

# CSV 파일 로드 및 정제
@st.cache_data
def load_data():
    try:
        # 여러 인코딩과 구분자 시도
        encodings = ['cp949', 'euc-kr', 'utf-8-sig', 'utf-8']
        separators = ['\t', ',', ';']  # 탭, 쉼표, 세미콜론
        
        df = None
        successful_encoding = None
        successful_separator = None
        
        for encoding in encodings:
            for separator in separators:
                try:
                    df = pd.read_csv('student_recommendations.csv', 
                                   encoding=encoding, 
                                   sep=separator,
                                   engine='python')  # python 엔진 사용
                    
                    # 최소 10개 컬럼이 있어야 유효한 데이터로 간주
                    if len(df.columns) >= 10:
                        successful_encoding = encoding
                        successful_separator = separator
                        break
                    else:
                        df = None
                        
                except Exception as e:
                    continue
            
            if df is None:
                break
        
        if df is None:
            st.error("CSV 파일을 읽을 수 없습니다. 파일 형식을 확인해주세요.")
            return None
        
        # 컬럼명 정리
        df.columns = df.columns.str.strip()
        
        # 데이터 정제
        for col in df.columns:
            if df[col].dtype == 'object':
                df[col] = df[col].astype(str).str.strip()
        
        # 숫자 컬럼 변환
        numeric_cols = ['semantic_similarity', 'course_industry_score', 'location_score', 
                       'diversity_score', 'freshness_score', 'final_score']
        
        for col in numeric_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')
        
        return df
        
    except Exception as e:
        st.error(f"데이터 로딩 오류: {e}")
        return None

# job_postings.csv 파일 로드
@st.cache_data
def load_job_postings():
    try:
        # job_postings.csv 파일 로드
        job_df = pd.read_csv('job_postings.csv', encoding='utf-8')
        
        # job_id를 키로 하고 url을 값으로 하는 딕셔너리 생성
        job_links = dict(zip(job_df['job_id'].astype(str), job_df['url']))
        
        return job_links
        
    except Exception as e:
        st.error(f"job_postings.csv 로딩 오류: {e}")
        return {}

# 간단한 사용자 인증 (실제 운영에서는 데이터베이스 사용)
def authenticate_user(student_id, password):
    try:
        # 학생 ID를 문자열로 처리하고 공백 제거
        student_id = str(student_id).strip()
        password = str(password).strip()
        
        # 간단한 비밀번호 검증 (실제로는 보안 강화 필요)
        if password == "1234":
            return True
        return False
    except Exception as e:
        st.error(f"인증 오류: {e}")
        return False

# 로그인 페이지
def show_login_page():
    st.title("🎓 학생 추천기업 정보 뷰어")
    st.markdown("---")
    
    st.markdown("### 🔐 로그인")
    st.markdown("학생 ID와 비밀번호를 입력하여 로그인하세요.")
    st.markdown("**ID**: 본인학번, 비밀번호 1234")
    
    with st.form("login_form"):
        student_id = st.text_input("학생 ID", placeholder="예: 202401020001")
        password = st.text_input("비밀번호", type="password", placeholder="1234")
        
        if st.form_submit_button("로그인"):
            if student_id and password:
                if authenticate_user(student_id, password):
                    st.session_state.authenticated = True
                    st.session_state.current_student = student_id
                    st.success("로그인 성공!")
                    st.rerun()
                else:
                    st.error("학생 ID 또는 비밀번호가 잘못되었습니다.")
            else:
                st.error("학생 ID와 비밀번호를 모두 입력해주세요.")

# 메인 대시보드
def show_dashboard():
    # 데이터 로드
    df = load_data()
    job_links = load_job_postings()
    
    if df is None:
        st.error("데이터를 로드할 수 없습니다.")
        return
    
    # 현재 로그인한 학생의 정보만 필터링
    current_student = st.session_state.current_student
    
    # 학생 ID 정제 (공백 제거)
    df['student_id'] = df['student_id'].astype(str).str.strip()
    current_student = str(current_student).strip()
    
    # 학생 데이터 필터링
    student_data = df[df['student_id'] == current_student]
    
    if student_data.empty:
        st.error("해당 학생의 데이터를 찾을 수 없습니다.")
        st.markdown("### 📋 사용 가능한 학생 ID 목록")
        available_students = sorted(df['student_id'].unique())
        st.write(f"총 {len(available_students)}명의 학생:")
        st.write(available_students[:10])  # 처음 10개만 표시
        if len(available_students) > 10:
            st.write(f"... 및 {len(available_students) - 10}명 더")
        return
    
    student_name = student_data['name'].iloc[0]
    
    # 헤더
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        st.title(f"🎓 {current_student} - {student_name}")
        st.markdown("### 개인 추천기업 정보")
    
    with col2:
        if st.button("로그아웃"):
            st.session_state.authenticated = False
            st.session_state.current_student = None
            st.rerun()
    
    with col3:
        st.metric("총 추천 건수", len(student_data))
    
    st.markdown("---")
    
    # 추천기업 정보 카드 형식으로 표시
    recommendations = student_data.sort_values('recommendation_rank')
    
    st.markdown("### 📋 추천기업 목록")
    
    # 카드 형식으로 표시
    for idx, row in recommendations.iterrows():
        with st.container():
            col1, col2 = st.columns([3, 1])
            
            with col1:
                # 메인 카드 내용
                st.markdown(f"""
                <div style="
                    border: 2px solid #e0e0e0;
                    border-radius: 10px;
                    padding: 20px;
                    margin: 10px 0;
                    background: linear-gradient(135deg, #f8f9fa 0%, #ffffff 100%);
                    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
                ">
                    <h3 style="color: #2c3e50; margin-bottom: 15px;">
                        🏆 {row['recommendation_rank']}순위 - {row['recommended_title']}
                    </h3>
                    <div style="margin-bottom: 15px;">
                        <strong>🏢 기업명:</strong> {row['recommended_company']}<br>
                        <strong>🏭 산업:</strong> {row['recommended_industry']}<br>
                        <strong>📍 지역:</strong> {row['recommended_location']}<br>
                        <strong>💼 직무유형:</strong> {row['recommended_job_type']}
                    </div>
                    <div style="
                        background: #e8f4fd;
                        padding: 10px;
                        border-radius: 5px;
                        border-left: 4px solid #3498db;
                    ">
                        <strong>📊 최종 점수:</strong> <span style="color: #e74c3c; font-size: 18px;">{row['final_score']:.3f}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                # 우측 버튼들
                st.markdown("<br><br>", unsafe_allow_html=True)
                
                # 상세 점수 버튼
                if st.button(f"📊 점수 상세", key=f"score_{idx}"):
                    st.session_state.show_scores = idx
                
                # 지원 링크 버튼
                job_id = str(row['recommended_job_id']).strip()
                job_link = job_links.get(job_id, "#")
                
                if job_link != "#":
                    st.markdown(f"""
                    <a href="{job_link}" target="_blank" style="
                        display: inline-block;
                        background: #27ae60;
                        color: white;
                        padding: 10px 20px;
                        text-decoration: none;
                        border-radius: 5px;
                        font-weight: bold;
                        text-align: center;
                        width: 100%;
                    ">
                        🚀 지원하기
                    </a>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div style="
                        display: inline-block;
                        background: #95a5a6;
                        color: white;
                        padding: 10px 20px;
                        text-align: center;
                        width: 100%;
                        border-radius: 5px;
                        font-weight: bold;
                    ">
                        🔗 링크 없음
                    </div>
                    """, unsafe_allow_html=True)
                
                # 상세 점수 표시
                if st.session_state.get('show_scores') == idx:
                    st.markdown("### 📊 상세 점수")
                    score_data = {
                        '의미적 유사도': row['semantic_similarity'],
                        '과정-산업 점수': row['course_industry_score'],
                        '지역 점수': row['location_score'],
                        '다양성 점수': row['diversity_score'],
                        '신선도 점수': row['freshness_score']
                    }
                    
                    for score_name, score_value in score_data.items():
                        st.metric(score_name, f"{score_value:.3f}")
            
            st.markdown("---")
    
    # 점수 분석 차트
    st.markdown("### 📊 전체 점수 분석")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # 최종 점수 차트
        fig_score = px.bar(
            recommendations,
            x='recommendation_rank',
            y='final_score',
            title='추천 순위별 최종 점수',
            labels={'recommendation_rank': '추천 순위', 'final_score': '최종 점수'},
            color='final_score',
            color_continuous_scale='viridis'
        )
        fig_score.update_layout(showlegend=False)
        st.plotly_chart(fig_score, use_container_width=True)
    
    with col2:
        # 세부 점수 비교
        score_cols = ['semantic_similarity', 'course_industry_score', 'location_score', 'diversity_score', 'freshness_score']
        score_labels = ['의미적 유사도', '과정-산업 점수', '지역 점수', '다양성 점수', '신선도 점수']
        
        # 점수 데이터 준비
        score_data = []
        for i, (col, label) in enumerate(zip(score_cols, score_labels)):
            if col in recommendations.columns:
                values = recommendations[col].dropna().tolist()
                if values:
                    score_data.append({
                        '점수유형': label,
                        '값': values[0],  # 첫 번째 추천의 점수
                        '순위': f'순위 {i+1}'
                    })
        
        if score_data:
            score_df = pd.DataFrame(score_data)
            fig_radar = px.line_polar(
                score_df, 
                r='값', 
                theta='점수유형', 
                line_close=True,
                title="세부 점수 분석"
            )
            fig_radar.update_traces(fill='toself')
            fig_radar.update_layout(
                polar=dict(
                    radialaxis=dict(
                        visible=True,
                        range=[0, 1]
                    )
                )
            )
            st.plotly_chart(fig_radar, use_container_width=True)
        else:
            st.info("세부 점수 데이터를 표시할 수 없습니다.")
    
    # 개인 통계
    st.markdown("---")
    st.markdown("### 📈 개인 통계")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        avg_score = recommendations['final_score'].mean()
        st.metric("평균 최종 점수", f"{avg_score:.3f}")
    
    with col2:
        top_industry = recommendations['recommended_industry'].mode().iloc[0] if not recommendations['recommended_industry'].mode().empty else "N/A"
        st.metric("가장 많이 추천된 산업", top_industry[:20] + "..." if len(str(top_industry)) > 20 else top_industry)
    
    with col3:
        top_location = recommendations['recommended_location'].mode().iloc[0] if not recommendations['recommended_location'].mode().empty else "N/A"
        st.metric("가장 많이 추천된 지역", top_location[:20] + "..." if len(str(top_location)) > 20 else top_location)
    
    # 데이터 다운로드 (개인 데이터만)
    st.markdown("---")
    st.markdown("### 💾 개인 데이터 다운로드")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("개인 추천 데이터 다운로드 (CSV)"):
            csv = student_data.to_csv(index=False, encoding='utf-8-sig')
            st.download_button(
                label="CSV 파일 다운로드",
                data=csv,
                file_name=f"student_{current_student}_recommendations.csv",
                mime="text/csv"
            )
    
    with col2:
        if st.button("개인 추천 데이터 다운로드 (Excel)"):
            output = BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                student_data.to_excel(writer, index=False, sheet_name='추천기업정보')
            output.seek(0)
            
            st.download_button(
                label="Excel 파일 다운로드",
                data=output.getvalue(),
                file_name=f"student_{current_student}_recommendations.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

# 사이드바 정보
def show_sidebar():
    with st.sidebar:
        st.markdown("## ℹ️ 사용법")
        st.markdown("""
        1. **로그인**: 학생 ID와 비밀번호로 로그인
        2. **개인 정보 확인**: 본인의 추천기업 정보만 확인
        3. **점수 분석**: 차트를 통해 점수 패턴 분석
        4. **데이터 다운로드**: 개인 데이터 다운로드
        """)
        
        if st.session_state.authenticated:
            st.markdown("## 👤 현재 로그인")
            st.markdown(f"**학생 ID**: {st.session_state.current_student}")
            
            df = load_data()
            if df is not None:
                student_data = df[df['student_id'] == st.session_state.current_student]
                if not student_data.empty:
                    st.markdown(f"**이름**: {student_data['name'].iloc[0]}")
                    st.markdown(f"**추천 건수**: {len(student_data)}건")
        
        st.markdown("---")
        st.markdown("**개발**: Streamlit")
        st.markdown("**버전**: 2.0.0 (로그인 기능 추가)")

# 메인 앱
def main():
    if not st.session_state.authenticated:
        show_login_page()
    else:
        show_dashboard()
    
    show_sidebar()

if __name__ == "__main__":
    main()
