import time
import tkinter as tk
from tkinter import messagebox
import urllib.request
from PIL import Image, ImageTk

# ข้อมูลควิซ 7 ประเทศ ( URL รูปภาพ และ เฉลย )
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
        "answer": ["อังกฤษ", "สหราชอาณาจักร", "uk"],
    },
]

# ตัวแปรควบคุมเกม
current_question = 0
score = 0
time_left = 67  # 1 นาที 7 วินาที
timer_running = False


# ฟังก์ชันโหลดรูปจาก URL
def load_image_from_url(url):
    req = urllib.request.urlopen(url)
    img_data = req.read()
    from io import BytesIO

    img = Image.open(BytesIO(img_data))
    img = img.resize((200, 120))
    return ImageTk.PhotoImage(img)


# ฟังก์ชันนับเวลาถอยหลัง
def update_timer():
    global time_left, timer_running
    if timer_running and time_left > 0:
        time_left -= 1
        minutes = time_left // 60
        seconds = time_left % 60
        lbl_timer.config(
            text=f"เวลาที่เหลือ: {minutes:02d}:{seconds:02d}"
        )
        root.after(1000, update_timer)
    elif time_left == 0 and timer_running:
        timer_running = False
        messagebox.showinfo("หมดเวลา", "เวลาหมดแล้วครับ!")
        finish_game()


# ฟังก์ชันเริ่มเกม
def start_game():
    global current_question, score, time_left, timer_running
    current_question = 0
    score = 0
    time_left = 67
    timer_running = True

    btn_start.pack_forget()
    frame_game.pack(pady=10)

    show_question()
    update_timer()


# ฟังก์ชันแสดงข้อสอบ
def show_question():
    global img_holder
    q = QUESTIONS[current_question]

    lbl_num.config(
        text=f"ข้อที่ {current_question + 1} / {len(QUESTIONS)}"
    )

    # โหลดรูปธง
    img_holder = load_image_from_url(q["flag"])
    lbl_flag.config(image=img_holder)

    ent_answer.delete(0, tk.END)
    ent_answer.focus()


# ฟังก์ชันตรวจคำตอบ
def check_answer(event=None):
    global current_question, score

    if not timer_running:
        return

    user_ans = ent_answer.get().strip().lower()
    correct_answers = QUESTIONS[current_question]["answer"]

    if user_ans in correct_answers:
        score += 1

    current_question += 1

    if current_question < len(QUESTIONS):
        show_question()
    else:
        finish_game()


# ฟังก์ชันจบเกม
def finish_game():
    global timer_running
    timer_running = False
    frame_game.pack_forget()

    lbl_timer.config(text="จบการแข่งขัน!")
    messagebox.showinfo(
        "สรุปผลคะแนน", f"คุณได้คะแนนทั้งหมด {score} / 7 คะแนน"
    )
    btn_start.config(text="เล่นใหม่อีกครั้ง")
    btn_start.pack(pady=20)


# สร้างหน้าต่างโปรแกรม
root = tk.Tk()
root.title("เกมทายธงชาติ (ม.4)")
root.geometry("400x450")

# หัวข้อ
lbl_title = tk.Label(
    root, text="เกมทายชื่อประเทศจากธงชาติ", font=("Tahoma", 16, "bold")
)
lbl_title.pack(pady=10)

# แสดงเวลา
lbl_timer = tk.Label(
    root, text="เวลาที่เหลือ: 01:07", font=("Tahoma", 14), fg="red"
)
lbl_timer.pack(pady=5)

# ปุ่มเริ่มเล่น
btn_start = tk.Button(
    root,
    text="เริ่มเล่นเกม",
    font=("Tahoma", 14),
    bg="#4CAF50",
    fg="white",
    command=start_game,
)
btn_start.pack(pady=20)

# เฟรมเก็บองค์ประกอบเกม
frame_game = tk.Frame(root)

lbl_num = tk.Label(frame_game, font=("Tahoma", 12))
lbl_num.pack(pady=5)

lbl_flag = tk.Label(frame_game)
lbl_flag.pack(pady=10)

lbl_prompt = tk.Label(
    frame_game, text="พิมพ์ชื่อประเทศ:", font=("Tahoma", 11)
)
lbl_prompt.pack(pady=5)

ent_answer = tk.Entry(frame_game, font=("Tahoma", 12), justify="center")
ent_answer.pack(pady=5)
ent_answer.bind("<Return>", check_answer)  # กด Enter เพื่อตอบได้

btn_submit = tk.Button(
    frame_game, text="ตอบข้อนี้", font=("Tahoma", 11), command=check_answer
)
btn_submit.pack(pady=10)

# เริ่มรันแอปพลิเคชัน
root.mainloop()
