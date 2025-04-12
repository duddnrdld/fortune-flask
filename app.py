from flask import Flask, request, send_from_directory
from datetime import date
import random

app = Flask(__name__)

@app.route("/image.png")
def serve_image():
    return send_from_directory(".", "image.png")

@app.route("/", methods=["GET", "POST", "HEAD"])
def home():
    if request.method == "HEAD":
        return '', 200

    if request.method == "POST":
        # 사용자가 제출한 폼 데이터를 받아서 처리
        name = request.form.get("name")
        birth = request.form.get("birth")
        gender = request.form.get("gender")
        calendar = request.form.get("calendar")
        today = str(date.today())

        # 히든 필드로 전달된 score(오늘 이미 점쳤다면 해당 점수) 또는 새로 계산
        score_str = request.form.get("score")
        if score_str and score_str.strip() != "":
            score = int(score_str)
        else:
            score = random.randint(1, 100)

        # 점수 구간별 운세 메시지
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
                function recalculateFortune() {{
                    // localStorage 데이터 삭제 후 입력 화면으로 이동
                    localStorage.removeItem("userData");
                    localStorage.removeItem("lastFortuneDate");
                    window.location.href = "/";
                }}
                // 지금 받은 데이터(당일 점수)를 다시 localStorage에 저장하여 재접속 시 자동으로 결과 화면이 나오도록
                const today = new Date().toISOString().split('T')[0];
                const data = {{
                    name: "{name}",
                    birth: "{birth}",
                    gender: "{gender}",
                    calendar: "{calendar}",
                    score: {score}
                }};
                localStorage.setItem("userData", JSON.stringify(data));
                localStorage.setItem("lastFortuneDate", today);
            </script>
            <style>
                body {{
                    margin: 0; padding: 0; overflow: hidden;
                    font-family: 'Poor Story', 'Jua', sans-serif;
                    background: #fff7ed; height: 100vh; position: relative;
                }}
                .fixed-header {{
                    position: fixed; top: 20px; width: 100%; text-align: center;
                    font-size: 28px; font-weight: bold; z-index: 20;
                    color: #333; font-family: 'Jua', sans-serif;
                }}
                .fortune-box {{
                    background: rgba(255,255,255,0.95);
                    padding: 40px 30px; border-radius: 30px;
                    box-shadow: 0 4px 20px rgba(0,0,0,0.1);
                    text-align: center; width: 90%; max-width: 400px;
                    z-index: 10; position: relative; top: 80px;
                    margin: 0 auto;
                }}
                .fortune-box h2 {{
                    font-size: 26px; color: #aa5c5c;
                    margin-bottom: 12px;
                }}
                .fortune-box p {{
                    font-size: 20px; color: #5c5c5c;
                    margin: 10px 0;
                }}
                .btn {{
                    margin: 10px 5px; display: inline-block;
                    padding: 10px 16px; background-color: #ff9caa;
                    color: white; border-radius: 20px;
                    text-decoration: none; font-weight: bold;
                }}
                .rotating-floating {{
                    position: absolute; width: 60px; opacity: 0.8;
                    pointer-events: none; animation: floatRotate linear infinite;
                }}
                @keyframes floatRotate {{
                    0% {{ transform: translateY(100vh) rotate(0deg); }}
                    100% {{ transform: translateY(-150px) rotate(360deg); }}
                }}
            </style>
        </head>
        <body>
            <div class="fixed-header">복토리</div>
            <div class="fortune-box">
                <h2>✨ {name}님의 운세 ✨</h2>
                <p>{today}</p>
                <p><strong>{score}점</strong></p>
                <p>{msg}</p>
                <a class="btn" href="javascript:kakaoShare()">카카오톡 공유하기</a>
                <a class="btn" href="javascript:recalculateFortune()">오늘의 운세 다시 점쳐보기</a>
            </div>
            <script>
                for (let i = 0; i < 30; i++) {{
                    const img = document.createElement("img");
                    img.src = "/image.png";
                    img.className = "rotating-floating";
                    img.style.left = Math.random() * 100 + "%";
                    img.style.zIndex = 1;
                    img.style.animationDuration = (15 + Math.random() * 15) + "s";
                    img.style.animationDelay = Math.random() * 10 + "s";
                    document.body.appendChild(img);
                }}
            </script>
        </body>
        </html>
        '''

    # GET 요청: 입력 화면
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title>복토리 운세입력</title>
        <link href="https://fonts.googleapis.com/css2?family=Jua&family=Poor+Story&display=swap" rel="stylesheet">
        <style>
            body {
                margin: 0; padding: 0; overflow: hidden;
                font-family: 'Poor Story', 'Jua', sans-serif;
                background: #fff7ed; height: 100vh; position: relative;
            }
            .fixed-header {
                position: fixed; top: 20px; width: 100%; text-align: center;
                font-size: 28px; font-weight: bold; z-index: 20;
                color: #333; font-family: 'Jua', sans-serif;
            }
            .fortune-box {
                background: rgba(255,255,255,0.95);
                padding: 40px 30px; border-radius: 30px;
                box-shadow: 0 4px 20px rgba(0,0,0,0.1);
                text-align: center; width: 90%; max-width: 400px;
                z-index: 10; position: relative; top: 80px;
                margin: 0 auto;
            }
            .fortune-box input, .fortune-box select, .fortune-box button {
                width: 100%; padding: 12px; margin-top: 12px;
                font-size: 16px; border-radius: 20px; border: none;
                box-shadow: inset 0 0 5px rgba(0,0,0,0.05);
            }
            .btn {
                background-color: #ff9caa; color: white;
                font-weight: bold; cursor: pointer;
            }
            .rotating-floating {
                position: absolute; width: 60px; opacity: 0.8;
                pointer-events: none; animation: floatRotate linear infinite;
            }
            @keyframes floatRotate {
                0% { transform: translateY(100vh) rotate(0deg); }
                100% { transform: translateY(-150px) rotate(360deg); }
            }
        </style>
    </head>
    <body>
        <div class="fixed-header">복토리</div>
        <div class="fortune-box">
            <form method="post" id="fortuneForm">
                <input name="name" id="name" placeholder="이름 입력">
                <input type="date" name="birth" id="birth">
                <select name="calendar" id="calendar">
                    <option>양력</option>
                    <option>음력</option>
                </select>
                <select name="gender" id="gender">
                    <option>여성</option>
                    <option>남성</option>
                </select>
                <!-- 기존 점수가 있으면 서버로 전달하기 위한 히든 필드 -->
                <input type="hidden" name="score" id="score" value="">
                <button type="submit" class="btn">입력 완료</button>
            </form>
        </div>
        <script>
            const form = document.getElementById('fortuneForm');
            const today = new Date().toISOString().split('T')[0];

            window.onload = () => {
                const saved = JSON.parse(localStorage.getItem("userData"));
                const lastDate = localStorage.getItem("lastFortuneDate");

                // 이미 오늘 점쳤다면 팝업 없이 바로 결과 페이지로 이동
                if (saved && lastDate === today) {
                    // 폼에 저장된 내용 자동 세팅
                    document.getElementById('name').value = saved.name;
                    document.getElementById('birth').value = saved.birth;
                    document.getElementById('calendar').value = saved.calendar;
                    document.getElementById('gender').value = saved.gender;
                    document.getElementById('score').value = saved.score;

                    // 자동으로 POST 전송 -> 결과 화면으로 이동
                    form.submit();
                }

                // 배경효과 이미지 생성
                for (let i = 0; i < 30; i++) {
                    const img = document.createElement("img");
                    img.src = "/image.png";
                    img.className = "rotating-floating";
                    img.style.left = Math.random() * 100 + "%";
                    img.style.zIndex = 1;
                    img.style.animationDuration = (15 + Math.random() * 15) + "s";
                    img.style.animationDelay = Math.random() * 10 + "s";
                    document.body.appendChild(img);
                }
            }

            form.addEventListener("submit", (e) => {
                // 오늘 점친 기록이 없으면 새 점수를 생성하여 localStorage 저장
                const saved = JSON.parse(localStorage.getItem("userData"));
                if (saved && localStorage.getItem("lastFortuneDate") === today) {
                    // 이미 오늘자 점수 존재 -> 해당 점수를 히든 필드에 담아서 서버로 전송
                    document.getElementById("score").value = saved.score;
                } else {
                    // 새로 점치기
                    const newScore = Math.floor(Math.random() * 100) + 1;
                    document.getElementById("score").value = newScore;

                    const data = {
                        name: document.getElementById("name").value,
                        birth: document.getElementById("birth").value,
                        gender: document.getElementById("gender").value,
                        calendar: document.getElementById("calendar").value,
                        score: newScore
                    };
                    localStorage.setItem("userData", JSON.stringify(data));
                    localStorage.setItem("lastFortuneDate", today);
                }
            });
        </script>
    </body>
    </html>
    '''

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
