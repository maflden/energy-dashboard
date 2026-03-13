import streamlit as st
import FinanceDataReader as fdr
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta

st.set_page_config(
    page_title="KOSPI 대시보드",
    page_icon="📈",
    layout="wide"
)

# 스타일
st.markdown("""
<style>
    .metric-card {
        background-color: #f9f9f9;
        border: 1px solid #ddd;
        border-radius: 10px;
        padding: 20px;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
    }
    .up { color: #e74c3c; }
    .down { color: #3498db; }
</style>
""", unsafe_allow_html=True)

@st.cache_data(ttl=300)  # 5분 캐시
def load_data(period_days=365):
    end = datetime.today()
    start = end - timedelta(days=period_days)
    df = fdr.DataReader('KS11', start=start.strftime('%Y-%m-%d'))
    return df

def main():
    st.title("📈 KOSPI 지수 대시보드")
    st.caption(f"최종 업데이트: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    # 기간 선택
    period_map = {"1개월": 30, "3개월": 90, "6개월": 180, "1년": 365, "3년": 1095}
    period_label = st.selectbox("조회 기간", list(period_map.keys()), index=3)
    period_days = period_map[period_label]

    with st.spinner("데이터 불러오는 중..."):
        df = load_data(period_days)

    if df.empty:
        st.error("데이터를 불러올 수 없습니다.")
        return

    current = df.iloc[-1]
    prev = df.iloc[-2]

    current_price = current['Close']
    change = current_price - prev['Close']
    change_rate = (change / prev['Close']) * 100
    color = "#e74c3c" if change >= 0 else "#3498db"
    symbol = "▲" if change >= 0 else "▼"

    # 상단 지표 카드
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <h4 style="margin:0;color:#333;">KOSPI 현재가</h4>
            <p style="font-size:26px;font-weight:bold;margin:8px 0 4px;">{current_price:,.2f}</p>
            <p style="font-size:16px;color:{color};margin:0;">{symbol} {abs(change):,.2f} ({change_rate:+.2f}%)</p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.metric("거래량", f"{int(current['Volume']):,}")
    with col3:
        st.metric("고가", f"{current['High']:,.2f}")
    with col4:
        st.metric("저가", f"{current['Low']:,.2f}")

    st.divider()

    # 차트
    fig = go.Figure()
    fig.add_trace(go.Candlestick(
        x=df.index,
        open=df['Open'],
        high=df['High'],
        low=df['Low'],
        close=df['Close'],
        name='KOSPI',
        increasing_line_color='#e74c3c',
        decreasing_line_color='#3498db'
    ))
    fig.update_layout(
        title=f"KOSPI 캔들 차트 ({period_label})",
        xaxis_title="날짜",
        yaxis_title="지수",
        xaxis_rangeslider_visible=False,
        height=500,
        template="plotly_white"
    )
    st.plotly_chart(fig, use_container_width=True)

    # 종가 추이
    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(
        x=df.index, y=df['Close'],
        mode='lines',
        name='종가',
        line=dict(color='#e74c3c' if change >= 0 else '#3498db', width=2),
        fill='tozeroy',
        fillcolor='rgba(231,76,60,0.1)' if change >= 0 else 'rgba(52,152,219,0.1)'
    ))
    fig2.update_layout(
        title="종가 추이",
        xaxis_title="날짜",
        yaxis_title="지수",
        height=350,
        template="plotly_white"
    )
    st.plotly_chart(fig2, use_container_width=True)

    # 데이터 테이블
    with st.expander("📋 원시 데이터 보기"):
        st.dataframe(
            df[['Open', 'High', 'Low', 'Close', 'Volume']].sort_index(ascending=False).head(30),
            use_container_width=True
        )

if __name__ == "__main__":
    main()
