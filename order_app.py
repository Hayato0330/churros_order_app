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
    }

    h1 {
        text-align: center;
        margin: 0 0 1rem 0;
    }

    .flavor-label {
        font-size: 18px;
        font-weight: 600;
        white-space: nowrap;
        margin-bottom: 0.2rem;
    }
    .flavor-label.choco {
        color: #8B4513;
    }
    .flavor-label.strawberry {
        color: #E60033;
    }

    .button-row {
        display: flex;
        flex-direction: row;
        align-items: center;
        justify-content: flex-start;
        gap: 0.2rem;
        margin-bottom: 1rem;
    }

    .triangle-button button {
        width: 3em;
        height: 2.2rem;
        font-size: 16px;
        padding: 0;
    }

    .count-display {
        width: 2.5em;
        text-align: center;
        font-size: 18px;
        font-weight: 600;
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

    # ボタン行をMarkdownで直接構成
    st.markdown(
        f"""
        <div class="button-row">
            <div class="triangle-button"><button onclick="window.streamlitRun && window.streamlitRun('left_{flavor}')">◀</button></div>
            <div class="count-display">{st.session_state.counts[flavor]}</div>
            <div class="triangle-button"><button onclick="window.streamlitRun && window.streamlitRun('right_{flavor}')">▶</button></div>
        </div>
        """,
        unsafe_allow_html=True,
    )

# 注文ボタン
st.markdown(
    """
    <div class="order-button-wrap">
        <button class="order-button">注文</button>
    </div>
    """,
    unsafe_allow_html=True,
)
