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
        padding-top: 2.2rem !important;  /* タイトル上半分が切れないように調整 */
        padding-bottom: 1rem;
        font-size: 16px;
        max-width: 500px;
        margin: 0 auto;
    }

    h1 {
        text-align: center;
        margin: 0 0 1.0rem 0;
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

    /* ===== スマホ向けレイアウト強制 ===== */
    @media (max-width: 600px) {

        /* 各行（columnsのラッパ）を横並びに強制 */
        div[data-testid="stHorizontalBlock"] {
            display: flex !important;
            flex-wrap: nowrap !important;
            align-items: center !important;
            justify-content: flex-start !important;
            gap: 0.1rem !important;
        }

        /* カラムの余白を削る */
        div[data-testid="stHorizontalBlock"] > div[data-testid="column"] {
            padding-left: 0 !important;
            padding-right: 0 !important;
            margin-left: 0 !important;
            margin-right: 0 !important;
        }

        /* ラベルは内容ぶんだけ。取りすぎない */
        div[data-testid="stHorizontalBlock"] > div[data-testid="column"]:nth-child(1) {
            flex: 0 0 auto !important;
            max-width: 40% !important;
        }

        /* 左ボタン・数字・右ボタンを横に詰める */
        div[data-testid="stHorizontalBlock"] > div[data-testid="column"]:nth-child(2) {
            flex: 0 0 14% !important;
        }
        div[data-testid="stHorizontalBlock"] > div[data-testid="column"]:nth-child(3) {
            flex: 0 0 10% !important;
        }
        div[data-testid="stHorizontalBlock"] > div[data-testid="column"]:nth-child(4) {
            flex: 0 0 14% !important;
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

# 1行 = テキスト + ◀ + 数字 + ▶
for flavor in flavors:
    # PC向けの比率（スマホではCSSで上書きされる）
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
