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
        padding-top: 0.75rem;
        padding-bottom: 1rem;
        padding-left: 0.5rem;
        padding-right: 0.5rem;
        font-size: 16px;
        max-width: 600px;
        margin: 0 auto;
    }

    /* タイトルを文字の半分だけ下に下げる */
    h1 {
        position: relative;
        top: 0.5em;
        text-align: center;
        margin-bottom: 0.8em;
    }

    .flavor-label {
        font-size: 18px;
        font-weight: 600;
        padding-left: 4px;
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

    /* スマホ表示最適化 — ボタンをもっと左に寄せて全体を1行に収める */
    @media (max-width: 600px) {
        div[data-testid="stHorizontalBlock"] {
            display: flex;
            flex-wrap: nowrap;
            align-items: center;
            gap: 0.1rem;
        }
        div[data-testid="stHorizontalBlock"] > div[data-testid="column"]:nth-child(1) {
            flex: 0 0 30% !important; /* ラベル部分を少し短く */
        }
        div[data-testid="stHorizontalBlock"] > div[data-testid="column"]:nth-child(2) {
            flex: 0 0 18% !important; /* 左ボタン */
        }
        div[data-testid="stHorizontalBlock"] > div[data-testid="column"]:nth-child(3) {
            flex: 0 0 12% !important; /* 数字 */
        }
        div[data-testid="stHorizontalBlock"] > div[data-testid="column"]:nth-child(4) {
            flex: 0 0 18% !important; /* 右ボタン */
        }
        .flavor-label {
            font-size: 16px;
        }
        .triangle-button button {
            font-size: 16px;
        }
        .count-display {
            font-size: 18px;
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

# カウントの初期化
if "counts" not in st.session_state:
    st.session_state.counts = {f: 0 for f in flavors}

st.header("ソフテニチュロス注文")

# 各フレーバー行
for flavor in flavors:
    # 全体をより左寄せに（スマホ画面で右ボタンまで見えるように）
    col_label, col_left, col_num, col_right = st.columns([2.8, 1.2, 1.2, 1.2])

    # ラベル
    with col_label:
        if flavor == "チョコ":
            cls = "flavor-label choco"
        elif flavor == "ストロベリー":
            cls = "flavor-label strawberry"
        else:
            cls = "flavor-label"
        st.markdown(f"<div class='{cls}'>{flavor}</div>", unsafe_allow_html=True)

    # 左向きボタン（◀）
    with col_left:
        st.markdown("<div class='triangle-button'>", unsafe_allow_html=True)
        left_clicked = st.button("◀", key=f"{flavor}_left")
        if left_clicked and st.session_state.counts[flavor] > 0:
            st.session_state.counts[flavor] -= 1
        st.markdown("</div>", unsafe_allow_html=True)

    # 数字表示
    with col_num:
        st.markdown(
            f"<div class='count-display'>{st.session_state.counts[flavor]}</div>",
            unsafe_allow_html=True,
        )

    # 右向きボタン（▶）
    with col_right:
        st.markdown("<div class='triangle-button'>", unsafe_allow_html=True)
        right_clicked = st.button("▶", key=f"{flavor}_right")
        if right_clicked:
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
