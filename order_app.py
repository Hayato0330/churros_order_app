# app1

import streamlit as st

# ページ設定
st.set_page_config(page_title="ソフテニチュロス注文", layout="wide")

# タイトル
st.markdown("<h1 style='text-align:center;'>ソフテニチュロス注文</h1>", unsafe_allow_html=True)

# スタイル設定（スマホ対応）
st.markdown("""
    <style>
    /* ページ全体を中央寄せ */
    .main {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
    }

    /* ボタンレイアウトを画面幅に収める */
    .button-container {
        display: flex;
        flex-wrap: wrap;
        justify-content: center;
        gap: 10px;
        width: 100%;
        max-width: 400px;
        margin-bottom: 20px;
    }

    /* 各ボタンの見た目を統一 */
    .button-container button {
        flex: 1 1 45%;
        height: 60px;
        font-size: 18px;
    }

    /* 注文ボタン */
    .order-button button {
        width: 100%;
        height: 60px;
        background-color: #007BFF;
        color: white;
        font-size: 20px;
        border-radius: 10px;
    }

    /* モバイル用の微調整 */
    @media (max-width: 600px) {
        .button-container button {
            flex: 1 1 48%;
            height: 55px;
            font-size: 16px;
        }
        .order-button button {
            height: 55px;
            font-size: 18px;
        }
    }
    </style>
""", unsafe_allow_html=True)

# 商品ボタン群
st.markdown('<div class="button-container">', unsafe_allow_html=True)
col1, col2 = st.columns(2)
with col1:
    if st.button("左向き"):
        st.session_state["direction"] = "left"
with col2:
    if st.button("右向き"):
        st.session_state["direction"] = "right"
st.markdown('</div>', unsafe_allow_html=True)

# 注文ボタン（青色で横長）
st.markdown('<div class="order-button">', unsafe_allow_html=True)
if st.button("注文"):
    st.success("注文が送信されました！")
st.markdown('</div>', unsafe_allow_html=True)
