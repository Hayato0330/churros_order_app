# app1

import streamlit as st

# ページ設定（スマートフォン利用を想定）
st.set_page_config(
    page_title="ソフテニチュロス注文",
    layout="wide",
)

# スタイル調整
st.markdown(
    """
    <style>
    .block-container {
        padding-top: 1.5rem !important;  /* タイトルが切れないよう十分な余白 */
        padding-bottom: 1rem;
        font-size: 16px;
        max-width: 480px;
        margin: 0 auto;
    }

    /* タイトル：文字の半分くらい下げるイメージで余白調整 */
    h1 {
        margin-top: 1.0em !important;
        margin-bottom: 0.8em;
        text-align: center;
    }

    .flavor-label {
        font-size: 18px;
        font-weight: 600;
        white-space: nowrap;
        margin-right: 4px;
        padding-left: 0;  /* 余白削除 */
    }
    .flavor-label.choco {
        color: #8B4513;
    }
    .flavor-label.strawberry {
        color: #E60033;
    }

    .count-display {
        text-align: center;
        font-size: 20px;
        font-weight: 600;
        line-height: 2.0rem;
        white-space: nowrap;
    }

    .triangle-button button {
        width: 100%;
        height: 2.0rem;
        font-size: 18px;
        padding: 0;
    }

    /* --- スマホ向けレイアウト最適化 --- */
    @media (max-width: 600px) {

        /* 行全体をフレックスに、隙間をほぼゼロに */
        div[data-testid="stHorizontalBlock"] {
            display: flex !important;
            flex-wrap: nowrap !important;
            align-items: center !important;
            justify-content: flex-start !important;
            gap: 0 !important;
        }

        /* 全カラムの左右余白を削る */
        div[data-testid="stHorizontalBlock"] > div[data-testid="column"] {
            padding-left: 0 !important;
            padding-right: 0 !important;
            margin-left: 0 !important;
            margin-right: 0 !important;
        }

        /* ラベル列は「内容に合わせる」＝無駄な空白を作らない */
        div[data-testid="stHorizontalBlock"] > div[data-testid="column"]:nth-child(1) {
            flex: 0 0 auto !important;
            max-width: 35% !important;  /* 長くてもここまで */
        }

        /* 左ボタン、数字、右ボタンは固定幅で詰める */
        div[data-testid="stHorizontalBlock"] > div[data-testid="column"]:nth-child(2) {
            flex: 0 0 18% !important;
        }
        div[data-testid="stHorizontalBlock"] > div[data-testid="column"]:nth-child(3) {
            flex: 0 0 14% !important;
        }
        div[data-testid="stHorizontalBlock"] > div[data-testid="column"]:nth-child(4) {
            flex: 0 0 18% !important;
        }

        .flavor-label {
            font-size: 16px;
        }
        .triangle-button button {
            font-size: 16px;
            height: 1.9rem;
        }
        .count-display {
            font-size: 18px;
            line-height: 1.9rem;
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

# 各フレーバー行
for flavor in flavors:
    # 基本比率（スマホではCSSで上書き）
    col_label, col_left, col_num, col_right = st.columns([2, 1, 1, 1])

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
