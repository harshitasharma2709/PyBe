import streamlit as st
from lessons import LESSONS
from scenarios import SCENARIOS

st.set_page_config(page_title="PyBe – Python Learning Lab", page_icon="🐍", layout="wide")

st.markdown("""
<style>
.main-title {font-size: 42px; font-weight: 800; margin-bottom: 0;}
.subtitle {font-size: 18px; color: #666;}
.card {padding: 18px; border: 1px solid #ddd; border-radius: 14px; margin: 8px 0;}
.badge {display:inline-block; padding:5px 10px; border-radius:20px; background:#eee;}
</style>
""", unsafe_allow_html=True)

if "completed" not in st.session_state:
    st.session_state.completed = set()
if "score" not in st.session_state:
    st.session_state.score = 0

st.sidebar.title("🐍 PyBe")
page = st.sidebar.radio("Navigate", ["Home", "Learn", "Scenario Lab", "Progress"])

if page == "Home":
    st.markdown('<p class="main-title">PyBe</p>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">A scenario-driven Python learning prototype.</p>', unsafe_allow_html=True)
    st.write("")
    c1, c2, c3 = st.columns(3)
    c1.metric("Lessons", len(LESSONS))
    c2.metric("Scenarios", len(SCENARIOS))
    c3.metric("Completed", len(st.session_state.completed))
    st.info("Learn a concept, apply it to a practical situation, and track your progress.")
    st.subheader("How it works")
    st.markdown("""
    1. **Learn** a small Python concept.
    2. **Apply** it through a real-world scenario.
    3. **Check** your answer and earn points.
    4. **Track** your learning progress.
    """)

elif page == "Learn":
    st.title("📚 Learn Python")
    for lesson in LESSONS:
        with st.expander(f"{lesson['id']}. {lesson['title']}"):
            st.write(lesson["explanation"])
            st.code(lesson["example"], language="python")
            if st.button(f"Mark '{lesson['title']}' complete", key=f"lesson_{lesson['id']}"):
                st.session_state.completed.add(f"L{lesson['id']}")
                st.success("Lesson completed!")

elif page == "Scenario Lab":
    st.title("🧩 Scenario Lab")
    st.caption("Choose the best Python solution for each practical situation.")
    for item in SCENARIOS:
        with st.container(border=True):
            st.subheader(item["title"])
            st.write(item["scenario"])
            choice = st.radio("Choose an approach:", item["options"], key=f"q_{item['id']}")
            if st.button("Check answer", key=f"check_{item['id']}"):
                if choice == item["answer"]:
                    if f"S{item['id']}" not in st.session_state.completed:
                        st.session_state.score += 10
                        st.session_state.completed.add(f"S{item['id']}")
                    st.success("Correct! +10 points")
                else:
                    st.error("Not quite. Read the explanation and try the next one.")
                st.info(item["explanation"])

elif page == "Progress":
    st.title("📈 Your Progress")
    total = len(LESSONS) + len(SCENARIOS)
    done = len(st.session_state.completed)
    progress = done / total if total else 0
    st.progress(progress)
    st.write(f"Completed: **{done}/{total}**")
    st.write(f"Scenario points: **{st.session_state.score}**")
    if progress == 1:
        st.balloons()
        st.success("Great work — you completed the prototype learning path!")
    else:
        st.info("Keep going. Complete lessons and scenario challenges to increase your progress.")
