import time
import streamlit as st

# ตั้งค่าหน้าเว็บ
st.set_page_config(
    page_title="เกมทายสูตรฟิสิกส์ การเคลื่อนที่แนวตรง", page_icon="⚡"
)

# ข้อมูล 5 สูตรหลักการเคลื่อนที่แนวตรง (ความเร่งคงที่)
QUESTIONS = [
    {
        "title": "สูตรหาความเร็วปลาย (ไม่มีระยะทาง s)",
        "hint": "ความเร็วปลาย = ความเร็วต้น + (ความเร่ง x เวลา)",
        "answers": ["v=u+at", "v = u + at", "v=u+(a*t)"],
    },
    {
        "title": "สูตรหาระยะทาง (ไม่มีความเร่ง a)",
        "hint": "ระยะทาง = [(ความเร็วต้น + ความเร็วปลาย) / 2] x เวลา",
        "answers": [
            "s=((u+v)/2)*t",
            "s = ((u+v)/2)t",
            "s=((u+v)/2)t",
            "s = ((u + v) / 2) * t",
            "s = (u+v)t/2",
        ],
    },
    {
        "title": "สูตรหาระยะทาง (ไม่มีความเร็วปลาย v)",
        "hint": "ระยะทาง = (ความเร็วต้น x เวลา) + (1/2 x ความเร่ง x เวลายกกำลังสอง)",
        "answers": [
            "s=ut+1/2at^2",
            "s = ut + 1/2at^2",
            "s=ut+(1/2)at^2",
            "s = ut + 0.5at^2",
            "s = ut + 1/2 a t^2",
        ],
    },
    {
        "title": "สูตรหาระยะทาง (ไม่มีความเร็วต้น u)",
        "hint": "ระยะทาง = (ความเร็วปลาย x เวลา) - (1/2 x ความเร่ง x เวลายกกำลังสอง)",
        "answers": [
            "s=vt-1/2at^2",
            "s = vt - 1/2at^2",
            "s=vt-(1/2)at^2",
            "s = vt - 0.5at^2",
            "s = vt - 1/2 a t^2",
        ],
    },
    {
        "title": "สูตรหาความเร็วปลายยกกำลังสอง (ไม่มีเวลา t)",
        "hint": "ความเร็วปลายยกกำลังสอง = ความเร็วต้นยกกำลังสอง + (2 x ความเร่ง x ระยะทาง)",
        "answers": [
            "v^2=u^2+2as",
            "v^2 = u^2 + 2as",
            "v^2=u^2+2*a*s",
            "v^2 = u^2 + 2 a s",
        ],
    },
]

TOTAL_TIME = 67  # 1 นาที 7 วินาที

# Initialize State
if "start_time" not in st.session_state:
    st.session_state.start_time = None
if "game_over" not in st.session_state:
    st.session_state.game_over = False

st.title("⚡ เกมทายสูตรฟิสิกส์ ม.4")
st.subheader("หัวข้อ: การเคลื่อนที่แนวตรง 5 สูตรหลัก")
st.write(
    "พิมพ์สูตรฟิสิกส์ให้ถูกต้องครบทั้ง 5 ข้อ ภายในเวลา **1 นาที 7 วินาที**!"
)
st.caption(
    "📌 ตัวอย่างการพิมพ์: `v = u + at`, `s = ut + 1/2at^2`, `v^2 = u^2 + 2as` (ใช้สัญลักษณ์ ^ สำหรับกำลังสอง)"
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
    with st.form("physics_quiz_form"):
        user_answers = []
        for i, q in enumerate(QUESTIONS):
            st.markdown(f"### ข้อที่ {i+1}: {q['title']}")
            st.info(f"💡 คำใบ้: {q['hint']}")
            ans = st.text_input(
                f"ตอบสูตรข้อที่ {i+1}:", key=f"q_{i}", placeholder="เช่น v = u + at"
            )
            # เคลียร์ช่องว่างและแปลงเป็นตัวพิมพ์เล็กเพื่อเทียบคำตอบง่ายขึ้น
            clean_ans = ans.strip().lower().replace(" ", "")
            user_answers.append(clean_ans)

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
            # แปลงเฉลยทุกรูปแบบให้ไม่มีช่องว่าง
            valid_answers = [
                a.strip().lower().replace(" ", "") for a in q["answers"]
            ]

            if user_ans in valid_answers:
                score += 1
                st.success(
                    f"ข้อ {i+1}: ถูกต้อง! 🎉 (เฉลย: {q['answers'][0]})"
                )
            else:
                st.error(
                    f"ข้อ {i+1}: ผิด! ❌ (เฉลยที่ถูกคือ: {q['answers'][0]})"
                )

        st.subheader(f"🏆 คุณได้คะแนนทั้งหมด {score} / 5 คะแนน!")

    # ปุ่มเริ่มใหม่
    if st.button("เล่นใหม่อีกครั้ง 🔄"):
        st.session_state.start_time = None
        st.session_state.game_over = False
        st.rerun()
