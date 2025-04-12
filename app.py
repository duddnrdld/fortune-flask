from flask import Flask, request, send_from_directory
from datetime import date
import random

app = Flask(__name__)

@app.route("/image.png")
def serve_image():
    return send_from_directory(".", "image.png")

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
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <title>오늘의 운세</title>
            <link href="https://fonts.googleapis.com/css2?family=Jua&family=Poor+Story&display=swap" rel="stylesheet">
            <script src="https://developers.kakao.com/sdk/js/kakao.js"></script>
            <script>
                Kakao.init("f29ff24b0feeb75f41f51f0c939c0f9f");
                function kakaoShare() {{
                    Kakao.Link.sendDefault({{
                        objectType: 'text',
                        text: '{name}님의 운세는 {score}점이에요! 💖 {msg}',
                        link: {{
                            mobileWebUrl: window.location.href,
                            webUrl: window.location.href
                        }}
                    }});
                }}
                function copyURL() {{
                    navigator.clipboard.writeText(window.location.href);
                    alert("링크가 복사되었어요! 인스타에 공유해보세요 💌");
                }}
            </script>
            <style>
                body {{
                    margin: 0;
                    padding: 0;
                    overflow: hidden;
                    font-family: 'Poor Story', 'Jua', sans-serif;
                    background: #fff7ed;
                    height: 100vh;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    position: relative;
                }}
                .fortune-box {{
                    background: rgba(255,255,255,0.95);
                    padding: 30px 20px;
                    border-radius: 30px;
                    box-shadow: 0 4px 20px rgba(0,0,0,0.1);
                    text-align: center;
                    width: 80%;
                    max-width: 320px;
                    z-index: 10;
                }}
                .fortune-box h2 {{
                    font-size: 24px;
                    color: #aa5c5c;
                    margin-bottom: 10px;
                }}
                .fortune-box p {{
                    font-size: 18px;
                    color: #5c5c5c;
                    margin: 8px 0;
                }}
                .btn {{
                    margin: 10px 5px;
                    display: inline-block;
                    padding: 10px 16px;
                    background-color: #ff9caa;
                    color: white;
                    border-radius: 20px;
                    text-decoration: none;
                    font-weight: bold;
                }}
                .floating {{
                    position: absolute;
                    width: 60px;
                    animation: floatUp 20s linear infinite;
                    opacity: 0.8;
                }}
                @keyframes floatUp {{
                    0% {{ transform: translateY(100vh); }}
                    100% {{ transform: translateY(-150px); }}
                }}
            </style>
        </head>
        <body>
            <div class="fortune-box">
                <h2>✨ {name}님의 운세 ✨</h2>
                <p>{today}</p>
                <p><strong>{score}점</strong></p>
                <p>{msg}</p>
                <a href="/" class="btn">돌아가기</a>
                <a class="btn" href="javascript:kakaoShare()">카카오톡 공유</a>
                <a class="btn" onclick="copyURL()">링크복사</a>
            </div>
            <img class="floating" src="/image.png" style="left:5%; animation-delay: 0s;">
            <img class="floating" src="/image.png" style="left:25%; animation-delay: 4s;">
            <img class="floating" src="/image.png" style="left:45%; animation-delay: 2s;">
            <img class="floating" src="/image.png" style="left:65%; animation-delay: 6s;">
            <img class="floating" src="/image.png" style="left:85%; animation-delay: 3s;">
        </body>
        </html>
        '''

    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <link href="https://fonts.googleapis.com/css2?family=Jua&family=Poor+Story&display=swap" rel="stylesheet">
        <style>
            body {
                background-color: #ffeef2;
                font-family: 'Poor Story', 'Jua', sans-serif;
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
            input {
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
            <h2>복토리</h2>
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
            window.onload = () => {
                const saved = JSON.parse(localStorage.getItem("userData"));
                const lastDate = localStorage.getItem("lastFortuneDate");
                if (saved) {
                    document.getElementById("name").value = saved.name;
                    document.getElementById("birth").value = saved.birth;
                    document.getElementById("gender").value = saved.gender;
                    document.getElementById("calendar").value = saved.calendar;
                    if (lastDate === today) {
                        alert(`${saved.name}님의 오늘의 운세는 이미 확인하셨어요!\n점수: ${saved.score}점`);
                        form.style.display = "none";
                        const result = document.createElement("div");
                        result.innerHTML = `
                            <h3>✨ ${saved.name}님의 운세 ✨</h3>
                            <p>${today}</p>
                            <p><strong>${saved.score}점</strong></p>
                            <a href="/">새로고침</a>
                            <a class="btn" href="javascript:kakaoShare()">카카오톡 공유</a>
                        `;
                        document.body.appendChild(result);
                    }
                }
            };
            function selectRadio(id, value) {
                document.getElementById(id).value = value;
            }
            form.addEventListener("submit", () => {
                const data = {
                    name: document.getElementById("name").value,
                    birth: document.getElementById("birth").value,
                    gender: document.getElementById("gender").value,
                    calendar: document.getElementById("calendar").value,
                    score: Math.floor(Math.random() * 100) + 1
                };
                localStorage.setItem("userData", JSON.stringify(data));
                localStorage.setItem("lastFortuneDate", today);
            });
        </script>
        <script src="https://developers.kakao.com/sdk/js/kakao.js"></script>
        <script>
            Kakao.init("f29ff24b0feeb75f41f51f0c939c0f9f");
            function kakaoShare() {
                const saved = JSON.parse(localStorage.getItem("userData"));
                Kakao.Link.sendDefault({
                    objectType: 'text',
                    text: `${saved.name}님의 운세는 ${saved.score}점이에요! 💖`,
                    link: {
                        mobileWebUrl: window.location.href,
                        webUrl: window.location.href
                    }
                });
            }
        </script>
    </body>
    </html>
    '''

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
