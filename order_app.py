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
        padding-top: 2.5rem !important;  /* タイトル上部が切れないよう多めに確保 */
        padding-bottom: 1rem;
        font-size: 16px;
        width: 100%;
        max-width: 500px;
        margin: 0 auto;
    }

    /* タイトル：自然な位置で下げる（切れない＆下がりすぎない） */
    h1 {
        text-align: center;
        margin-top: 0;        /* paddingで調整しているのでここは0 */
        margin-bottom: 1rem;
    }

    .flavor-label {
        font-size: 18px;
        font-weight: 600;
        white-space: nowrap;
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
        white-space: nowrap;
    }

    .triangle-button button {
        width: 100%;
        min-width: 0;
        height: 2rem;
        font-size: 16px;
        padding: 0;
    }

    /* スマホ向け：無駄な余白を削って必ず1行に収める */
    @media (max-width: 600px) {
        div[data-testid="stHorizontalBlock"] {
            gap: 0.1rem !important;
        }
        div[data-testid="column"] {
            padding-left: 0 !important;
            padding-right: 0 !important;
            margin-left: 0 !important;
            margin-right: 0 !important;
        }
    }

    /* 注文ボタン */
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
    # ラベル列を小さく、ボタン群を詰める比率（スマホでも1行に入るよう調整）
    col_label, col_left, col_num, col_right = st.columns([1.2, 0.6, 0.4, 0.6])

    with col_label:
        cls = "flavor-label"
        if flavor == "チョコ":
            cls += " choco"
        elif flavor == "ストロベリー":
            cls += " strawberry"
        st.markdown(f"<div class='{cls}'>{flavor}</div>", unsafe_allow_html=True)

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

# 注文ボタン（見た目のみ）
st.markdown(
    """
    <div class="order-button-wrap">
        <button class="order-button">注文</button>
    </div>
    """,
    unsafe_allow_html=True,
)
