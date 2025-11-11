# app1

import streamlit as st

# タイトル
st.markdown("<h1 style='text-align:center;'>ソフテニチュロス注文</h1>", unsafe_allow_html=True)

# レイアウト
col1, col2, col3 = st.columns([1, 2, 1], gap="small")

# 三角ボタン（左・右）
with col1:
    left = st.button("◀", use_container_width=True)
with col3:
    right = st.button("▶", use_container_width=True)

# 中央に画像や数量表示などを配置（例）
with col2:
    st.markdown("<p style='text-align:center; font-size:22px;'>数量: 1</p>", unsafe_allow_html=True)

# 注文ボタン（青・横長）
st.markdown("""
    <style>
        /* 全体レスポンシブ対応 */
        @media (max-width: 600px) {
            .stButton > button {
                font-size: 20px !important;
                padding: 0.8em 0 !important;
            }
        }
        /* 注文ボタンのデザイン */
        .order-button button {
            background-color: #007BFF;
            color: white;
            font-size: 22px;
            border-radius: 10px;
            width: 100%;
            height: 60px;
        }
        .order-button button:hover {
            background-color: #0056b3;
        }
    </style>
""", unsafe_allow_html=True)

# 横長の青い「注文」ボタン
st.markdown('<div class="order-button">', unsafe_allow_html=True)
order = st.button("注文", use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

# 注文処理の例
if order:
    st.success("ご注文ありがとうございます！")
