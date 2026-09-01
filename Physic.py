import random
import time
import streamlit as st

# ตั้งค่าหน้าเว็บ
st.set_page_config(
    page_title="เกมทายสูตรฟิสิกส์ การเคลื่อนที่แนวตรง", page_icon="⚡"
)

# ข้อมูลสูตรฟิสิกส์ 5 ข้อ (พร้อมตัวเลือกหลอก)
QUESTIONS = [
    {
        "title": "1. สูตรหาความเร็วปลาย (เมื่อไม่มีระยะทาง s)",
        "hint": "ความเร็วปลาย = ความเร็วต้น + (ความเร่ง x เวลา)",
        "correct": "v = u + at",
        "choices": ["v = u + at", "v = u - at", "v = u + 2at", "v = at / u"],
    },
    {
        "title": "2. สูตรหาระยะทาง (เมื่อไม่มีความเร่ง a)",
        "hint": "ระยะทาง = [(ความเร็วต้น + ความเร็วปลาย) / 2] x เวลา",
        "correct": "s = ((u + v) / 2) * t",
        "choices": [
            "s = ((u + v) / 2) * t",
            "s = ((u - v) / 2) * t",
            "s = (u + v) * t",
            "s = ((u + v) / t) * 2",
        ],
    },
    {
        "title": "3. สูตรหาระยะทาง (เมื่อไม่มีความเร็วปลาย v)",
        "hint": "ระยะทาง = (ความเร็วต้น x เวลา) + (1/2 x ความเร่ง x เวลายกกำลังสอง)",
        "correct": "s = ut + (1/2)at²",
        "choices": [
            "s = ut + (1/2)at²",
            "s = ut - (1/2)at²",
            "s = vt + (1/2)at²",
            "s = ut + at²",
        ],
    },
    {
        "title": "4. สูตรหาระยะทาง (เมื่อไม่มีความเร็วต้น u)",
        "hint": "ระยะทาง = (ความเร็วปลาย x เวลา) - (1/2 x ความเร่ง x เวลายกกำลังสอง)",
        "correct": "s = vt - (1/2)at²",
        "choices": [
            "s = vt - (1/2)at²",
            "s = vt + (1/2)at²",
            "s = ut - (1/2)at²",
            "s = vt - at²",
        ],
    },
    {
        "title": "5. สูตรหาความเร็วปลายยกกำลังสอง (เมื่อไม่มีเวลา t)",
        "hint": "ความเร็วปลาย² = ความเร็วต้น² + (2 x ความเร่ง x ระยะทาง)",
        "correct": "v² = u² + 2as",
        "choices": [
            "v² = u² + 2as",
            "v² = u² - 2as",
            "v² = u² + as",
            "v = u² + 2as",
        ],
    },
]

TOTAL_TIME = 67  # 1 นาที 7 วินาที

# Initialize State
if "start_time" not in st.session_state:
    st.session_state.start_time = None
if "game_over" not in st.session_state:
    st.session_state.game_over = False
if "shuffled_choices" not in st.session_state:
    # สุ่มลำดับตัวเลือกเก็บไว้
    st.session_state.shuffled_choices = []
    for q in QUESTIONS:
        choices = q["choices"].copy()
        random.shuffle(choices)
        st.session_state.shuffled_choices.append(choices)

st.title("⚡ เกมทายสูตรฟิสิกส์ ม.4")
st.subheader("หัวข้อ: การเคลื่อนที่แนวตรง (กดเลือกตัวเลือกที่ถูกต้อง)")
st.write(
    "เลือกสูตรฟิสิกส์ให้ถูกต้องครบทั้ง 5 ข้อ ภายในเวลา **1 นาที 7 วินาที**!"
)

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
    with st.form("physics_choice_quiz"):
        user_answers = []
        for i, q in enumerate(QUESTIONS):
            st.markdown(f"### {q['title']}")
            st.info(f"💡 คำใบ้: {q['hint']}")

            # ตัวเลือก Radio
            selected = st.radio(
                "เลือกสูตรที่ถูกต้อง:",
                options=st.session_state.shuffled_choices[i],
                key=f"q_{i}",
                index=None,  # ยังไม่ได้เลือก
            )
            user_answers.append(selected)
            st.markdown("---")

        submitted = st.form_submit_button(
            "ส่งคำตอบ 🚀", disabled=st.session_state.game_over
        )

    # ตรวจคำตอบเมื่อกดส่ง
    if submitted and not st.session_state.game_over:
        score = 0
        st.header("📊 ผลคะแนน")

        for i, q in enumerate(QUESTIONS):
            user_ans = user_answers[i]
            correct_ans = q["correct"]

            if user_ans == correct_ans:
                score += 1
                st.success(f"ข้อ {i+1}: ถูกต้อง! 🎉 ({correct_ans})")
            else:
                st.error(
                    f"ข้อ {i+1}: ผิด! ❌ (คุณเลือก: {user_ans if user_ans else 'ไม่ได้เลือก'} | เฉลยที่ถูกคือ: {correct_ans})"
                )

        st.subheader(f"🏆 คุณได้คะแนนทั้งหมด {score} / 5 คะแนน!")

    # ปุ่มเริ่มใหม่
    if st.button("เล่นใหม่อีกครั้ง 🔄"):
        st.session_state.start_time = None
        st.session_state.game_over = False

        # สุ่มตัวเลือกใหม่
        st.session_state.shuffled_choices = []
        for q in QUESTIONS:
            choices = q["choices"].copy()
            random.shuffle(choices)
            st.session_state.shuffled_choices.append(choices)

        st.rerun()
