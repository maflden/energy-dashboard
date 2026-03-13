# 📈 KOSPI 대시보드

FinanceDataReader와 Streamlit으로 만든 KOSPI 지수 실시간 대시보드입니다.

## 기능
- KOSPI 현재가, 등락폭, 등락률 표시
- 캔들 차트 및 종가 추이 시각화
- 1개월 ~ 3년 기간 선택
- 5분 단위 자동 캐시 갱신

## 로컬 실행

```bash
git clone https://github.com/<your-username>/kospi-dashboard.git
cd kospi-dashboard
pip install -r requirements.txt
streamlit run app.py
```

## Streamlit Cloud 배포 방법

1. 이 저장소를 GitHub에 push
2. [share.streamlit.io](https://share.streamlit.io) 접속
3. **New app** 클릭
4. GitHub 저장소 선택 → `app.py` 지정 → **Deploy**

배포 완료 후 공개 URL이 자동 생성됩니다.

## 파일 구조

```
kospi-dashboard/
├── app.py            # Streamlit 메인 앱
├── requirements.txt  # 패키지 목록
└── README.md
```
