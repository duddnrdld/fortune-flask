from flask import Flask, request
from datetime import date
import random

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        name = request.form.get("name")
        birth = request.form.get("birth")
        gender = request.form.get("gender")
        calendar = request.form.get("calendar")
        today = str(date.today())

        score = random.randint(1, 100)

        if score <= 20:
            msg = "오늘은 조심이 필요해요."
        elif score <= 50:
            msg = "보통의 하루가 예상돼요."
        elif score <= 80:
            msg = "좋은 기운이 들어오고 있어요!"
        else:
            msg = "행운이 가득한 하루가 될 거예요!"

        return f'''
        <h2>{name}님의 운세 ({today})</h2>
        <p>{score}점: {msg}</p>
        <a href="/">돌아가기</a>
        '''

    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            body {
                background-color: #ffeef2;
                font-family: 'Arial', sans-serif;
                margin: 0;
                padding: 0;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
            }
            .wrapper {
                background-color: #eaffea;
                border-radius: 30px;
                padding: 30px 20px;
                width: 300px;
                box-shadow: 0 4px 10px rgba(0,0,0,0.1);
                text-align: center;
            }
            .wrapper h2 {
                margin-bottom: 20px;
                font-size: 24px;
                color: #444;
            }
            input, select {
                width: 100%;
                padding: 10px;
                margin-top: 10px;
                font-size: 16px;
                border: none;
                border-radius: 20px;
                background-color: #fff;
                text-align: center;
            }
            .row {
                display: flex;
                justify-content: space-between;
                margin-top: 10px;
            }
            .row button {
                flex: 1;
                margin: 0 5px;
                padding: 10px;
                border-radius: 20px;
                border: none;
                background-color: #fff;
                font-size: 16px;
                color: #555;
            }
            .submit-btn {
                margin-top: 20px;
                background-color: #ff8ea3;
                color: white;
                font-weight: bold;
            }
        </style>
    </head>
    <body>
        <div class="wrapper">
            <h2>돈돈즈</h2>
            <form method="post" id="fortuneForm">
                <input name="name" id="name" placeholder="이름 입력">
                <input type="date" name="birth" id="birth">

                <div class="row">
                    <button type="button" onclick="selectRadio('calendar', '양력')">양력</button>
                    <button type="button" onclick="selectRadio('calendar', '음력')">음력</button>
                </div>

                <div class="row">
                    <button type="button" onclick="selectRadio('gender', '여성')">여성</button>
                    <button type="button" onclick="selectRadio('gender', '남성')">남성</button>
                </div>

                <input type="hidden" name="gender" id="gender">
                <input type="hidden" name="calendar" id="calendar">

                <button type="submit" class="submit-btn">입력 완료</button>
            </form>
        </div>

        <script>
            const form = document.getElementById('fortuneForm');
            const today = new Date().toISOString().split('T')[0];

            // 1. 저장된 정보 불러오기
            window.onload = () => {
                const saved = JSON.parse(localStorage.getItem("userData"));
                const lastDate = localStorage.getItem("lastFortuneDate");

                if (saved) {
                    document.getElementById("name").value = saved.name;
                    document.getElementById("birth").value = saved.birth;
                    document.getElementById("gender").value = saved.gender;
                    document.getElementById("calendar").value = saved.calendar;

                    if (lastDate === today) {
                        alert("오늘의 운세는 이미 확인하셨습니다.");
                        form.style.display = "none";
                    }
                }
            };

            // 2. 선택 버튼 누르면 값 저장
            function selectRadio(id, value) {
                document.getElementById(id).value = value;
            }

            // 3. 제출 시 사용자 정보 저장
            form.addEventListener("submit", () => {
                const data = {
                    name: document.getElementById("name").value,
                    birth: document.getElementById("birth").value,
                    gender: document.getElementById("gender").value,
                    calendar: document.getElementById("calendar").value,
                };
                localStorage.setItem("userData", JSON.stringify(data));
                localStorage.setItem("lastFortuneDate", today);
            });
        </script>
    </body>
    </html>
    '''
