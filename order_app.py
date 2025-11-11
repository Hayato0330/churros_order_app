# app1
import streamlit as st

# ページ設定
st.set_page_config(page_title="ソフテニチュロス注文", layout="wide")

# CSSでタイトル位置とカラム間隔を強制調整
st.markdown(
    """
    <style>
    /* ページ全体の調整 */
    .block-container {
        padding-top: 1.5rem !important;  /* タイトルが切れないように余白を多めに */
        padding-bottom: 1rem;
        font-size: 16px;
        max-width: 480px;
        margin: 0 auto;
    }

    /* タイトルを文字の半分だけ下げる */
    h1 {
        margin-top: 1.2em !important; /* 上半分が見切れないように調整 */
        text-align: center;
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
        font-size: 20px;
        font-weight: 600;
        line-height: 2.2rem;
        white-space: nowrap;
    }

    .triangle-button button {
        width: 100%;
        height: 2.2rem;
        font-size: 18px;
        padding: 0;
    }

    /* スマホ最適化 */
    @media (max-width: 600px) {
        /* カラム幅を極限まで詰めて1行に */
        div[data-testid="stHorizontalBlock"] {
            display: flex !important;
            flex-wrap: nowrap !important;
            justify-content: flex-start !important;
            gap: 0.05rem !important;
        }

        div[data-testid="stHorizontalBlock"] > div[data-testid="column"]:nth-child(1) {
            flex: 0 0 22% !important; /* ラベル短め */
        }
        div[data-testid="stHorizontalBlock"] > div[data-testid="column"]:nth-child(2) {
            flex: 0 0 16% !important; /* 左ボタン */
        }
        div[data-testid="stHorizontalBlock"] > div[data-testid="column"]:nth-child(3) {
            flex: 0 0 12% !important; /* 数字 */
        }
        div[data-testid="stHorizontalBlock"] > div[data-testid="column"]:nth-child(4) {
            flex: 0 0 16% !important; /* 右ボタン */
        }

        /* 余白を消して中央寄せ */
        div[data-testid="column"] {
            padding: 0 !important;
            margin: 0 !important;
        }
        .flavor-label { font-size: 16px; }
        .triangle-button button { font-size: 16px; height: 2rem; }
        .count-display { font-size: 18px; line-height: 2rem; }
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

if "counts" not in st.session_state:
    st.session_state.counts = {f: 0 for f in flavors}

st.header("ソフテニチュロス注文")

for flavor in flavors:
    col_label, col_left, col_num, col_right = st.columns([2.2, 1.2, 1.0, 1.2])
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

st.markdown(
    """
    <div class="order-button-wrap">
        <button class="order-button">注文</button>
    </div>
    """,
    unsafe_allow_html=True,
)
