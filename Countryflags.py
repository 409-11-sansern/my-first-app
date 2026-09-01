import time
import streamlit as st

# ตั้งค่าหน้าเว็บ
st.set_page_config(page_title="เกมทายธงชาติ", page_icon="🚩")

# ข้อมูลควิซ 7 ประเทศ (รูปภาพธงชาติ URL และเฉลยภาษาไทย)
QUESTIONS = [
    {
        "flag": "https://flagcdn.com/w320/th.png",
        "answer": ["ไทย", "ประเทศไทย", "thailand"],
    },
    {
        "flag": "https://flagcdn.com/w320/jp.png",
        "answer": ["ญี่ปุ่น", "japan"],
    },
    {
        "flag": "https://flagcdn.com/w320/kr.png",
        "answer": ["เกาหลีใต้", "south korea"],
    },
    {
        "flag": "https://flagcdn.com/w320/fr.png",
        "answer": ["ฝรั่งเศส", "france"],
    },
    {
        "flag": "https://flagcdn.com/w320/br.png",
        "answer": ["บราซิล", "brazil"],
    },
    {
        "flag": "https://flagcdn.com/w320/ca.png",
        "answer": ["แคนาดา", "canada"],
    },
    {
        "flag": "https://flagcdn.com/w320/gb.png",
        "answer": ["อังกฤษ", "สหราชอาณาจักร", "uk", "united kingdom"],
    },
]

TOTAL_TIME = 67  # 1 นาที 7 วินาที

# Initialize State
if "start_time" not in st.session_state:
    st.session_state.start_time = None
if "game_over" not in st.session_state:
    st.session_state.game_over = False

st.title("🚩 เกมทายชื่อประเทศจากธงชาติ")
st.write("ทายชื่อประเทศ 7 ประเทศให้ครบภายในเวลา **1 นาที 7 วินาที**!")

# ปุ่มเริ่มเกม
if st.session_state.start_time is None:
    if st.button("เริ่มเล่นเกม! ⏱️", type="primary"):
        st.session_state.start_time = time.time()
        st.session_state.game_over = False
        st.rerun()

else:
    # คำนวณเวลาที่เหลือ
    elapsed_time = time.time() - st.session_state.start_time
    remaining_time = max(0, int(TOTAL_TIME - elapsed_time))

    # แสดงตัวนับเวลา
    time_display = st.empty()
    minutes = remaining_time // 60
    seconds = remaining_time % 60
    time_display.metric(
        "⏱️ เวลาที่เหลือ", f"{minutes:02d}:{seconds:02d}"
    )

    if remaining_time == 0:
        st.session_state.game_over = True
        st.error("⏰ หมดเวลาแล้ว!")

    # ฟอร์มใส่คำตอบ
    with st.form("flag_quiz_form"):
        user_answers = []
        for i, q in enumerate(QUESTIONS):
            st.subheader(f"ข้อที่ {i+1}")
            st.image(q["flag"], width=200)
            ans = st.text_input(
                f"ประเทศอะไรเอ่ย? (ข้อ {i+1})", key=f"q_{i}"
            )
            user_answers.append(ans.strip().lower())

        submitted = st.form_submit_button(
            "ส่งคำตอบ 🚀", disabled=st.session_state.game_over
        )

    # ตรวจคำตอบเมื่อกดส่ง
    if submitted and not st.session_state.game_over:
        score = 0
        st.markdown("---")
        st.header("📊 ผลคะแนน")

        for i, q in enumerate(QUESTIONS):
            user_ans = user_answers[i]
            correct_answers = [a.lower() for a in q["answer"]]

            if user_ans in correct_answers:
                score += 1
                st.success(
                    f"ข้อ {i+1}: ถูกต้อง! 🎉 (คำตอบ: {q['answer'][0]})"
                )
            else:
                st.error(
                    f"ข้อ {i+1}: ผิด! ❌ (ตอบ: '{user_ans}' | เฉลย: {q['answer'][0]})"
                )

        st.balloons()
        st.subheader(f"🏆 คุณได้คะแนนทั้งหมด {score} / 7 คะแนน!")

    # ปุ่มเริ่มใหม่
    if st.button("เล่นใหม่อีกครั้ง 🔄"):
        st.session_state.start_time = None
        st.session_state.game_over = False
        st.rerun()
