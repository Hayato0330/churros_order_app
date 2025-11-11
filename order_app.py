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
        padding-top: 2.2rem !important;  /* タイトル上部が切れないように */
        padding-bottom: 1rem;
        font-size: 16px;
        max-width: 500px;
        margin: 0 auto;
    }

    /* タイトル位置調整（「少し下」に） */
    h1 {
        text-align: center;
        margin: 0 0 1rem 0;
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

    /* ===== スマホ向け 強制1行レイアウト ===== */
    @media (max-width: 600px) {

        /* 各行（columnsラッパ）を必ず横並びにする */
        div[data-testid="stHorizontalBlock"] {
            display: flex !important;
            flex-direction: row !important;
            flex-wrap: nowrap !important;
            align-items: center !important;
            justify-content: flex-start !important;
            gap: 0.15rem !important;
        }

        /* 各columnの余白を殺す */
        div[data-testid="stHorizontalBlock"] > div[data-testid="column"] {
            padding-left: 0 !important;
            padding-right: 0 !important;
            margin-left: 0 !important;
            margin-right: 0 !important;
            flex: 0 0 auto !important;
        }

        /* ラベル列：必要な分だけ（広く取りすぎない） */
        div[data-testid="stHorizontalBlock"] > div[data-testid="column"]:nth-child(1) {
            max-width: 40% !important;
        }

        /* 左ボタン・数字・右ボタンを詰めて横に並べる */
        div[data-testid="stHorizontalBlock"] > div[data-testid="column"]:nth-child(2) {
            width: 16% !important;
        }
        div[data-testid="stHorizontalBlock"] > div[data-testid="column"]:nth-child(3) {
            width: 12% !important;
        }
        div[data-testid="stHorizontalBlock"] > div[data-testid="column"]:nth-child(4) {
            width: 16% !important;
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

# 各行：テキスト / ◀ / 数字 / ▶ を1行構成にする
for flavor in flavors:
    # PC向け比率（スマホではCSSが上書き）
    col_label, col_left, col_num, col_right = st.columns([2.5, 0.8, 0.6, 0.8])

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
