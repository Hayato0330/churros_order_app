# app1

import streamlit as st

# ページ設定（スマートフォン利用を想定したシンプルなUI）
st.set_page_config(
    page_title="フレーバーセレクター",
    layout="centered",
)

st.markdown(
    """
    <style>
    /* 全体の余白とフォントをスマホ向けに調整 */
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
    </style>
    """,
    unsafe_allow_html=True,
)

flavors = ["プレーン", "チョコ", "ストロベリー"]

# カウントの初期化（すべて0）
if "counts" not in st.session_state:
    st.session_state.counts = {f: 0 for f in flavors}

st.header("フレーバー選択", divider="gray")

# 各フレーバーの行を表示
for flavor in flavors:
    col_label, col_left, col_num, col_right = st.columns([3, 1.5, 1.5, 1.5])

    with col_label:
        st.markdown(f"<div class='flavor-label'>{flavor}</div>", unsafe_allow_html=True)

    # 左向きボタン（◀）
    with col_left:
        st.markdown("<div class='triangle-button'>", unsafe_allow_html=True)
        if st.button("◀", key=f"{flavor}_left"):
            # 0未満にならないように制御
            if st.session_state.counts[flavor] > 0:
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
        if st.button("▶", key=f"{flavor}_right"):
            st.session_state.counts[flavor] += 1
        st.markdown("</div>", unsafe_allow_html=True)
