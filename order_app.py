# app1

import streamlit as st

# ページ設定
st.set_page_config(
    page_title="ソフテニチュロス注文",
    layout="wide",
)

st.markdown(
    """
    <style>
    .block-container {
        padding-top: 2.2rem !important;
        padding-bottom: 1rem;
        font-size: 16px;
        max-width: 500px;
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
        text-align: left;
        margin-bottom: 0.3rem; /* ボタン行との間隔 */
    }
    .flavor-label.choco { color: #8B4513; }
    .flavor-label.strawberry { color: #E60033; }

    .count-display {
        text-align: center;
        font-size: 18px;
        font-weight: 600;
        line-height: 2rem;
        white-space: nowrap;
    }

    .triangle-button button {
        width: 100%;
        min-width: 0;
        height: 2rem;
        font-size: 16px;
        padding: 0;
    }

    /* スマホ向け1行ボタン配置（2段構成：上にテキスト，下に◀ 0 ▶） */
    @media (max-width: 600px) {
        .flavor-row {
            display: flex;
            flex-direction: column;
            align-items: flex-start;
            margin-bottom: 0.8rem;
        }

        .button-row {
            display: flex;
            flex-direction: row;
            align-items: center;
            justify-content: flex-start;
            gap: 0.2rem;
            width: 100%;
        }

        .button-row > div {
            flex: 0 0 auto;
        }

        .button-row .triangle-button { width: 16%; }
        .button-row .count-display { width: 12%; text-align: center; }
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
    .order-button:active { transform: scale(0.98); }
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
    # 各フレーバーを「テキスト行＋ボタン行」の2段構成にする
    st.markdown('<div class="flavor-row">', unsafe_allow_html=True)

    # テキスト
    cls = "flavor-label"
    if flavor == "チョコ":
        cls += " choco"
    elif flavor == "ストロベリー":
        cls += " strawberry"
    st.markdown(f"<div class='{cls}'>{flavor}</div>", unsafe_allow_html=True)

    # ボタン行（横並び）
    st.markdown('<div class="button-row">', unsafe_allow_html=True)
    # 左ボタン
    st.markdown("<div class='triangle-button'>", unsafe_allow_html=True)
    if st.button("◀", key=f"{flavor}_left") and st.session_state.counts[flavor] > 0:
        st.session_state.counts[flavor] -= 1
    st.markdown("</div>", unsafe_allow_html=True)
    # 数字
    st.markdown(f"<div class='count-display'>{st.session_state.counts[flavor]}</div>", unsafe_allow_html=True)
    # 右ボタン
    st.markdown("<div class='triangle-button'>", unsafe_allow_html=True)
    if st.button("▶", key=f"{flavor}_right"):
        st.session_state.counts[flavor] += 1
    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)  # button-row閉じ
    st.markdown('</div>', unsafe_allow_html=True)  # flavor-row閉じ

# 注文ボタン
st.markdown(
    """
    <div class="order-button-wrap">
        <button class="order-button">注文</button>
    </div>
    """,
    unsafe_allow_html=True,
)
