# app1

import streamlit as st

# ページ設定（スマートフォン利用を想定）
st.set_page_config(
    page_title="フレーバーセレクター",
    layout="centered",
)

# スタイル調整
st.markdown(
    """
    <style>
    .main {
        padding-top: 1rem;
        padding-bottom: 1rem;
        font-size: 16px;
    }
    .flavor-label {
        font-size: 18px;
        font-weight: 600;
        padding-left: 4px;
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
    }
    .triangle-button button {
        width: 100%;
        height: 2.2rem;
        font-size: 18px;
        padding: 0;
    }

    /* スマホで列が縦積みされないように調整 */
    @media (max-width: 600px) {
        div[data-testid="stHorizontalBlock"] {
            display: flex;
            flex-wrap: nowrap;
            align-items: center;
            gap: 0.25rem;
        }
        div[data-testid="column"] {
            flex: 0 0 auto !important;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

flavors = ["プレーン", "チョコ", "ストロベリー"]

# カウントの初期化
if "counts" not in st.session_state:
    st.session_state.counts = {f: 0 for f in flavors}

st.header("フレーバー選択", divider="gray")

# 各フレーバー行
for flavor in flavors:
    col_label, col_left, col_num, col_right = st.columns([3, 1.5, 1.5, 1.5])

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

st.markdown("---")

# 注文ボタン（機能はこれから実装）
order = st.button("注文する")
