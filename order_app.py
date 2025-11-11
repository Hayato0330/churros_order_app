# app1

import streamlit as st

# ページ設定
st.set_page_config(
    page_title="ソフテニチュロス注文",
    layout="centered",
)

# スタイル（レイアウトを壊さない範囲に限定）
st.markdown(
    """
    <style>
    .block-container {
        padding-top: 2.2rem !important;  /* タイトルが切れない程度に下げる */
        padding-bottom: 1rem;
        font-size: 16px;
        max-width: 480px;
        margin: 0 auto;
    }

    h1 {
        text-align: center;
        margin: 0 0 1.2rem 0;
    }

    .flavor-label {
        font-size: 18px;
        font-weight: 600;
        margin-bottom: 0.2rem;
    }
    .flavor-label.choco {
        color: #8B4513;
    }
    .flavor-label.strawberry {
        color: #E60033;
    }

    .count-display {
        text-align: center;
        font-size: 18px;
        font-weight: 600;
        line-height: 2rem;
    }

    .triangle-button button {
        width: 100%;
        height: 2rem;
        font-size: 16px;
        padding: 0;
    }

    .order-button-wrap {
        margin-top: 1.5rem;
    }
    .order-button {
        width: 100%;
        padding: 0.9rem 1rem;
        font-size: 18px;
        font-weight: 600;
        background-color: #007BFF;
        color: #FFFFFF;
        border: none;
        border-radius: 8px;
        cursor: pointer;
    }
    .order-button:active {
        transform: scale(0.98);
    }
    </style>
    """,
    unsafe_allow_html=True,
)

flavors = ["プレーン", "チョコ", "ストロベリー"]

# カウント初期化
if "counts" not in st.session_state:
    st.session_state.counts = {f: 0 for f in flavors}

st.header("ソフテニチュロス注文")

for flavor in flavors:
    # 1行目：テキストのみ
    if flavor == "チョコ":
        cls = "flavor-label choco"
    elif flavor == "ストロベリー":
        cls = "flavor-label strawberry"
    else:
        cls = "flavor-label"
    st.markdown(f"<div class='{cls}'>{flavor}</div>", unsafe_allow_html=True)

    # 2行目：◀ 数 ▶ を横一列で
    col_left, col_num, col_right = st.columns([1, 1, 1])

    with col_left:
        st.markdown("<div class='triangle-button'>", unsafe_allow_html=True)
        if st.button("◀", key=f"{flavor}_left") and st.session_state.counts[flavor] > 0:
            st.session_state.counts[flavor] -= 1
        st.markdown("</div>", unsafe_allow_html=True)

    with col_num:
        st.markdown(
            f"<div class='count-display'>{st.session_state.counts[flavor]}</div>",
            unsafe_allow_html=True,
        )

    with col_right:
        st.markdown("<div class='triangle-button'>", unsafe_allow_html=True)
        if st.button("▶", key=f"{flavor}_right"):
            st.session_state.counts[flavor] += 1
        st.markdown("</div>", unsafe_allow_html=True)

# 注文ボタン
st.markdown(
    """
    <div class="order-button-wrap">
        <button class="order-button">注文</button>
    </div>
    """,
    unsafe_allow_html=True,
)
