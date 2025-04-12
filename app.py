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

        return f"<h2>{name}님의 운세 ({today})</h2><p>{score}점: {msg}</p>"

    return '''
<!DOCTYPE html>
<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body { font-family: sans-serif; max-width: 400px; margin: auto; padding: 20px; }
        input, select, button { width: 100%; padding: 8px; margin-top: 10px; font-size: 16px; }
    </style>
</head>
<body>
    <h2>오늘의 운세</h2>
    <form id="fortuneForm" method="post">
        이름: <input name="name" id="name"><br>
        생년월일: <input name="birth" id="birth" type="date"><br>
        성별:
        <select name="gender" id="gender">
            <option>남성</option><option>여성</option>
        </select><br>
        양력/음력:
        <select name="calendar" id="calendar">
            <option>양력</option><option>음력</option>
        </select><br>
        <button type="submit">운세 확인</button>
    </form>

    <script>
        const form = document.getElementById('fortuneForm');
        const today = new Date().toISOString().split('T')[0];

        // 1. 저장된 정보로 자동 채우기
        window.onload = () => {
            const saved = JSON.parse(localStorage.getItem("userData"));
            const lastDate = localStorage.getItem("lastFortuneDate");

            if (saved) {
                document.getElementById("name").value = saved.name;
                document.getElementById("birth").value = saved.birth;
                document.getElementById("gender").value = saved.gender;
                document.getElementById("calendar").value = saved.calendar;

                // 2. 오늘 이미 운세를 봤는지 확인
                if (lastDate === today) {
                    alert("오늘의 운세는 이미 확인하셨습니다.");
                    form.style.display = "none";
                }
            }
        };

        // 3. 운세 요청 시 정보 저장 + 날짜 저장
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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
