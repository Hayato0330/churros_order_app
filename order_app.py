# app1

import streamlit as st

st.set_page_config(
    page_title="ソフテニチュロス注文",
    layout="centered",
)

st.markdown(
    """
    <style>
    .block-container {
        padding-top: 2.2rem !important;
        padding-bottom: 1rem;
        font-size: 16px;
        max-width: 480px;
        margin: 0 auto;
        text-align: center; /* 全体を中央寄せ */
    }

    h1 {
        text-align: center;
        margin: 0 0 1rem 0;
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

    /* ボタン行のレイアウト */
    .button-row {
        display: flex;
        flex-direction: row;
        align-items: center;
        justify-content: center; /* 中央揃え */
        gap: 0.6rem;
        margin-bottom: 1.2rem;
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
        width: 2.8rem;
        text-align: center;
        font-size: 20px;
        font-weight: 700;
    }

    .order-button-wrap {
        margin-top: 1.5rem;
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

    /* スマホで特に中央バランスが崩れないよう調整 */
    @media (max-width: 600px) {
        .button-row {
            gap: 0.8rem;
        }
        .triangle-button button {
            width: 3.2rem;
            height: 3.2rem;
            font-size: 22px;
        }
        .count-display {
            font-size: 22px;
            width: 3rem;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

flavors = ["プレーン", "チョコ", "ストロベリー"]

if "counts" not in st.session_state:
    st.session_state.counts = {f: 0 for f in flavors}

st.header("ソフテニチュロス注文")

for flavor in flavors:
    cls = "flavor-label"
    if flavor == "チョコ":
        cls += " choco"
    elif flavor == "ストロベリー":
        cls += " strawberry"
    st.markdown(f"<div class='{cls}'>{flavor}</div>", unsafe_allow_html=True)

    # ボタン行（Flexboxで中央揃え）
    col_left, col_num, col_right = st.columns([1, 1, 1])
    with col_left:
        if st.button("◀", key=f"{flavor}_left") and st.session_state.counts[flavor] > 0:
            st.session_state.counts[flavor] -= 1
    with col_num:
        st.markdown(
            f"<div class='count-display'>{st.session_state.counts[flavor]}</div>",
            unsafe_allow_html=True,
        )
    with col_right:
        if st.button("▶", key=f"{flavor}_right"):
            st.session_state.counts[flavor] += 1

st.markdown(
    """
    <div class="order-button-wrap">
        <button class="order-button">注文</button>
    </div>
    """,
    unsafe_allow_html=True,
)
