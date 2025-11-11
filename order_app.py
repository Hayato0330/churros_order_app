# app1

import streamlit as st

# ページ設定
st.set_page_config(
    page_title="ソフテニチュロス注文",
    layout="centered",
)

st.markdown(
    """
    <style>
    .block-container {
        padding-top: 2.2rem !important;  /* タイトルが切れないように */
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
        font-size: 20px;
        font-weight: 700;
        white-space: nowrap;
        margin-bottom: 0.3rem;
        text-align: center;
    }
    .flavor-label.choco {
        color: #8B4513;
    }
    .flavor-label.strawberry {
        color: #E60033;
    }

    /* ▼ 各フレーバーの「◀ 数 ▶」行のラッパ */
    .button-row-wrap > div[data-testid="stHorizontalBlock"] {
        display: flex !important;
        flex-direction: row !important;
        flex-wrap: nowrap !important;
        align-items: center !important;
        justify-content: center !important;  /* 中央寄せ */
        gap: 0.6rem !important;
        width: 100%;
    }

    .button-row-wrap > div[data-testid="stHorizontalBlock"] > div[data-testid="column"] {
        flex: 0 0 auto !important;
        padding: 0 !important;
        margin: 0 !important;
    }

    /* ボタンの見た目とサイズ */
    .triangle-button button {
        width: 3rem;
        height: 3rem;
        font-size: 20px;
        font-weight: bold;
        border-radius: 12px;
        border: 1px solid #ddd;
        background-color: #f8f9fa;
    }
    .triangle-button button:active {
        background-color: #e0e0e0;
        transform: scale(0.97);
    }

    .count-display {
        width: 3rem;
        text-align: center;
        font-size: 22px;
        font-weight: 700;
    }

    /* 注文ボタン */
    .order-button-wrap {
        margin-top: 1.8rem;
    }
    .order-button {
        width: 100%;
        padding: 1rem 1.2rem;
        font-size: 20px;
        font-weight: 700;
        background-color: #007BFF;
        color: #FFFFFF;
        border: none;
        border-radius: 10px;
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
    # テキスト行
    cls = "flavor-label"
    if flavor == "チョコ":
        cls += " choco"
    elif flavor == "ストロベリー":
        cls += " strawberry"
    st.markdown(f"<div class='{cls}'>{flavor}</div>", unsafe_allow_html=True)

    # 「◀ 数 ▶」行（必ず1行 & 中央揃え）
    st.markdown("<div class='button-row-wrap'>", unsafe_allow_html=True)
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

    st.markdown("</div>", unsafe_allow_html=True)  # button-row-wrap を閉じる

# 注文ボタン（見た目のみ）
st.markdown(
    """
    <div class="order-button-wrap">
        <button class="order-button">注文</button>
    </div>
    """,
    unsafe_allow_html=True,
)
