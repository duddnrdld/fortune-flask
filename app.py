from flask import Flask, request, send_from_directory
from datetime import date

app = Flask(__name__)

# image.png 파일 제공
@app.route("/image.png")
def serve_image():
    return send_from_directory(".", "image.png")

# 1. 인사 화면 (항상 먼저 보임)
@app.route("/", methods=["GET"])
def greeting():
    return f'''
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <!-- 아이폰 확대/축소 방지 -->
        <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=0, shrink-to-fit=no">
        <title>인사</title>
        <link href="https://fonts.googleapis.com/css2?family=Jua&family=Poor+Story&display=swap" rel="stylesheet">
        <style>
            body {{
                margin: 0;
                padding: 0;
                display: flex;
                justify-content: center;
                align-items: center;
                flex-direction: column;
                height: 100vh;
                background: #F5E6CC; /* 파스텔 톤 배경 */
                font-family: 'Poor Story', 'Jua', sans-serif;
                position: relative;
                overflow: hidden;
            }}
            .central-image {{
                width: 200px; /* 원래 60px의 2배 크기 */
                z-index: 10;
            }}
            .speech-bubble {{
                position: absolute;
                top: 30%;
                left: 50%;
                transform: translateX(-50%);
                background: white;
                padding: 15px 20px;
                border-radius: 10px;
                border: 2px solid #ccc;
                font-size: 16px;
                min-width: 200px;
                text-align: center;
                z-index: 10;
            }}
            .speech-bubble::after {{
                content: "";
                position: absolute;
                bottom: -10px;
                left: 50%;
                transform: translateX(-50%);
                border-width: 10px;
                border-style: solid;
                border-color: white transparent transparent transparent;
            }}
            .action-button {{
                position: absolute;
                bottom: 40px;
                left: 50%;
                transform: translateX(-50%);
                padding: 10px 20px;
                font-size: 18px;
                background-color: #ff9caa;
                color: white;
                border: none;
                border-radius: 10px;
                cursor: pointer;
                display: none;
                z-index: 10;
            }}
        </style>
    </head>
    <body>
        <!-- 중앙에 2배 크기의 이미지 -->
        <img src="/image.png" class="central-image" alt="중앙 이미지">
        <!-- 말풍선 (타이핑 애니메이션) -->
        <div class="speech-bubble" id="speechBubble"></div>
        <!-- 대사 종료 후 나타나는 버튼 -->
        <button class="action-button" id="actionButton">부탁해!</button>
        <script>
            // 말풍선 타이핑 애니메이션 (총 2초 동안 진행)
            const text = "안녕하세요 주인님, 오늘의 운세를 봐드릴께요!";
            const bubble = document.getElementById("speechBubble");
            let index = 0;
            function typeText() {{
                if(index < text.length){{
                    bubble.innerText += text.charAt(index);
                    index++;
                    setTimeout(typeText, 2000 / text.length);
                }} else {{
                    document.getElementById("actionButton").style.display = "block";
                }}
            }}
            typeText();
            // "부탁해!" 버튼 클릭 시, 회원가입 정보가 있으면 /result, 없으면 /home으로 이동
            document.getElementById("actionButton").onclick = function() {{
                const userData = localStorage.getItem("userData");
                if (userData) {{
                    location.href = "/result";
                }} else {{
                    location.href = "/home";
                }}
            }};
        </script>
    </body>
    </html>
    '''

# 2. 회원가입/입력 화면 (/home)
@app.route("/home", methods=["GET", "POST"])
def home():
    today = str(date.today())
    if request.method == "POST":
        # 회원가입 폼 데이터 처리 후 localStorage에 저장
        name = request.form.get("name", "")
        birth = request.form.get("birth", "")
        calendar = request.form.get("calendar", "")
        gender = request.form.get("gender", "")
        return f'''
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=0, shrink-to-fit=no">
            <title>회원가입 완료</title>
        </head>
        <body>
            <script>
                const userData = {{
                    name: "{name}",
                    birth: "{birth}",
                    calendar: "{calendar}",
                    gender: "{gender}"
                }};
                localStorage.setItem("userData", JSON.stringify(userData));
                localStorage.setItem("hasVisited", "true");
                location.href = "/result";
            </script>
        </body>
        </html>
        '''
    return f'''
    <!DOCTYPE html>
    <html>
    <head>
       <meta charset="UTF-8">
       <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=0, shrink-to-fit=no">
       <title>복토리 운세입력</title>
       <link href="https://fonts.googleapis.com/css2?family=Jua&family=Poor+Story&display=swap" rel="stylesheet">
       <style>
          body {{
              margin: 0;
              padding: 0;
              overflow: hidden;
              font-family: 'Poor Story', 'Jua', sans-serif;
              background: #fff7ed;
              height: 100vh;
              position: relative;
          }}
          .fixed-header {{
              position: fixed;
              top: 20px;
              width: 100%;
              text-align: center;
              font-size: 28px;
              font-weight: bold;
              z-index: 110;
              color: #333;
          }}
          .greeting {{
              position: fixed;
              top: 60px;
              width: 100%;
              text-align: center;
              font-size: 20px;
              color: #333;
              z-index: 120;
          }}
          .form-box {{
              background: rgba(255,255,255,0.95);
              padding: 40px 10px;
              border-radius: 30px;
              box-shadow: 0 4px 20px rgba(0,0,0,0.1);
              text-align: center;
              width: 80%;
              max-width: 340px;
              z-index: 100;
              margin: 120px auto;
          }}
          input, select, button {{
              width: 100%;
              padding: 12px;
              margin-top: 12px;
              font-size: 16px;
              border-radius: 20px;
              border: none;
          }}
          button {{
              background-color: #ff9caa;
              color: white;
              font-weight: bold;
              cursor: pointer;
          }}
          .rotating-floating {{
              position: absolute;
              width: 60px;
              opacity: 0.8;
              pointer-events: none;
              z-index: -1; /* 항상 뒤쪽에 */
          }}
          /* 네 방향 애니메이션 keyframes */
          @keyframes floatRotateBottomToTop {{
              0% {{ transform: translateY(100vh) rotate(0deg); }}
              100% {{ transform: translateY(-150px) rotate(360deg); }}
          }}
          @keyframes floatRotateTopToBottom {{
              0% {{ transform: translateY(-150px) rotate(0deg); }}
              100% {{ transform: translateY(100vh) rotate(360deg); }}
          }}
          @keyframes floatRotateLeftToRight {{
              0% {{ transform: translateX(-150px) rotate(0deg); }}
              100% {{ transform: translateX(100vw) rotate(360deg); }}
          }}
          @keyframes floatRotateRightToLeft {{
              0% {{ transform: translateX(100vw) rotate(0deg); }}
              100% {{ transform: translateX(-150px) rotate(360deg); }}
          }}
       </style>
    </head>
    <body>
       <div class="fixed-header">복토리</div>
       <div class="greeting" id="greeting"></div>
       <div class="form-box">
          <form method="post">
              <input name="name" id="name" placeholder="이름 입력" required>
              <input type="date" name="birth" id="birth" required>
              <select name="calendar" id="calendar">
                  <option value="양력">양력</option>
                  <option value="음력">음력</option>
              </select>
              <select name="gender" id="gender">
                  <option value="여성">여성</option>
                  <option value="남성">남성</option>
              </select>
              <button type="submit">입력 완료</button>
          </form>
       </div>
       <script>
           // 상단 인삿말 타이핑 애니메이션 (반복)
           const greetingText = "안녕하세요 주인님! 오늘도 방문해 주셔서 감사합니다!";
           let greetIndex = 0;
           function typeGreeting() {{
               const greetElem = document.getElementById("greeting");
               greetElem.innerText = greetingText.slice(0, greetIndex);
               greetIndex++;
               if (greetIndex > greetingText.length) {{
                   setTimeout(() => {{
                       greetIndex = 0;
                       typeGreeting();
                   }}, 2000);
               }} else {{
                   setTimeout(typeGreeting, 150);
               }}
           }}
           typeGreeting();
           // flying image.png 생성 (배경, 즉시 시작)
           const numCols = 6;
           const numRows = 5;
           const animations = [
               "floatRotateBottomToTop",
               "floatRotateTopToBottom",
               "floatRotateLeftToRight",
               "floatRotateRightToLeft"
           ];
           for (let i = 0; i < numCols * numRows; i++) {{
               const img = document.createElement("img");
               img.src = "/image.png";
               img.className = "rotating-floating";
               const col = i % numCols;
               const row = Math.floor(i / numCols);
               img.style.left = (col * (100 / numCols)) + "%";
               img.style.top = (row * (100 / numRows)) + "%";
               const animationChoice = animations[Math.floor(Math.random() * animations.length)];
               const duration = 15 + Math.random() * 15;
               img.style.animation = animationChoice + " " + duration + "s linear infinite";
               img.style.animationDelay = "0s";
               document.body.appendChild(img);
           }}
       </script>
    </body>
    </html>
    '''

# 3. 결과 화면 (/result)
@app.route("/result")
def result():
    script = """
        let saved = JSON.parse(localStorage.getItem("userData"));
        const today = new Date().toISOString().split('T')[0];
        let score;
        if (saved && localStorage.getItem("lastFortuneDate") === today && saved.score !== undefined) {
            score = saved.score;
        } else {
            score = Math.floor(Math.random() * 100) + 1;
            saved.score = score;
            localStorage.setItem("userData", JSON.stringify(saved));
            localStorage.setItem("lastFortuneDate", today);
        }
        let msg = "";
        if (score <= 10) {
            msg = "오늘의 점수가 1에서 10 사이로 매우 낮게 나왔습니다. 오늘은 전반적으로 어려움과 좌절이 예상되나, 작은 성공에도 감사하며 마음을 다잡아야 할 때입니다. 모든 어려움 속에서도 성장의 기회를 포착하며, 미래를 향한 발판으로 삼을 수 있는 중요한 교훈을 얻을 수 있을 것입니다.";
        } else if (score <= 20) {
            msg = "오늘의 점수가 11에서 20 사이로 나오며, 약간의 불운이 예상됩니다. 예상치 못한 어려움이나 작은 실수가 생길 수 있으나, 그러한 경험은 앞으로의 삶에 소중한 배움의 기회로 작용할 것입니다. 침착하게 자신의 상황을 돌아보고, 주위의 도움을 받으면 금세 회복할 수 있습니다.";
        } else if (score <= 30) {
            msg = "오늘의 점수가 21에서 30 사이로 낮게 나왔습니다. 약간의 운세 부진이 예상되지만, 이는 당신에게 자기 성찰의 시간을 제공하며, 앞으로 나아갈 방향을 재정비할 기회를 줍니다. 예상치 못한 작은 시련 속에서도 배움의 씨앗을 찾고, 긍정적인 마음가짐을 유지하면 큰 발전으로 이어질 것입니다.";
        } else if (score <= 40) {
            msg = "오늘의 점수가 31에서 40 사이로 측정되었습니다. 약간의 곤란함과 도전이 따르겠지만, 이는 당신이 더욱 성장할 수 있는 계기가 될 것입니다. 어려움을 극복하고 스스로를 단련하는 과정에서, 평소에 깨닫지 못한 자신의 잠재력을 발견할 수 있는 기회가 제공될 것입니다.";
        } else if (score <= 50) {
            msg = "오늘의 점수가 41에서 50 사이로 중간 정도의 운세를 보여줍니다. 상황에 따라 안정과 도전이 교차하는 하루가 예상되며, 평범해 보이는 순간들 속에도 예상치 못한 기회와 변화의 조짐이 숨어 있습니다. 꾸준한 노력과 긍정적인 태도가 결국 큰 변화를 만들어낼 것입니다.";
        } else if (score <= 60) {
            msg = "오늘의 점수가 51에서 60 사이로, 다소 긍정적인 운세를 보입니다. 평소보다 좋은 기운이 주변을 감싸며, 작은 성공과 성취가 이루어질 가능성이 높습니다. 이런 흐름을 유지하면서 꾸준한 노력을 더하면, 앞으로의 도전에 있어서 큰 든든한 버팀목이 되어줄 것입니다.";
        } else if (score <= 70) {
            msg = "오늘의 점수가 61에서 70 사이로, 전반적으로 운이 따르는 날입니다. 여러 모로 순조로운 일이 펼쳐지며, 자신감과 희망을 가지고 나아갈 수 있는 기회들이 찾아옵니다. 사람들과의 소통과 협력을 통해 예상치 못한 행운과 성장이 뒤따를 수 있는 훌륭한 하루가 될 것입니다.";
        } else if (score <= 80) {
            msg = "오늘의 점수가 71에서 80 사이로 꽤 좋은 운세를 보여줍니다. 긍정적인 에너지와 창의력이 넘치는 날로, 새로운 도전에서 성공할 가능성이 높습니다. 준비된 마음과 용기를 가지고 앞서 나아간다면, 뜻깊은 성취와 만족스러운 결과가 기다리고 있을 것입니다.";
        } else if (score <= 90) {
            msg = "오늘의 점수가 81에서 90 사이로, 매우 유리한 운세를 자랑합니다. 열정과 활력이 넘치는 만큼, 주어진 기회를 효과적으로 활용하면 놀라운 변화와 성과를 이룰 수 있는 날입니다. 당신의 노력이 결실을 맺으며, 주변의 응원과 격려가 더해져 진정한 성공을 경험할 수 있을 것입니다.";
        } else {
            msg = "오늘의 점수가 91에서 100 사이로, 최고의 운세를 보여줍니다. 모든 일이 당신의 의도대로 순조롭게 전개되며, 특별한 행운과 성공이 가득한 날입니다. 열정과 노력이 극대화되어, 평소 꿈꿔왔던 목표를 이룰 수 있는 기회의 문이 활짝 열릴 것입니다. 이번 날을 통해 인생의 새로운 전환점과 기쁨을 만끽할 수 있을 것입니다.";
        }
        document.getElementById("name").innerText = saved.name;
        document.getElementById("score").innerText = score + "점";
        document.getElementById("msg").innerText = msg;
    """
    return f'''
    <!DOCTYPE html>
    <html>
    <head>
       <meta charset="UTF-8">
       <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=0, shrink-to-fit=no">
       <title>오늘의 운세</title>
       <link href="https://fonts.googleapis.com/css2?family=Jua&family=Poor+Story&display=swap" rel="stylesheet">
       <style>
          body {{
              margin: 0;
              padding: 0;
              overflow: hidden;
              font-family: 'Poor Story', 'Jua', sans-serif;
              background: #fff7ed;
              height: 100vh;
              position: relative;
          }}
          .fixed-header {{
              position: fixed;
              top: 20px;
              width: 100%;
              text-align: center;
              font-size: 28px;
              font-weight: bold;
              z-index: 110;
              color: #333;
          }}
          .greeting {{
              position: fixed;
              top: 60px;
              width: 100%;
              text-align: center;
              font-size: 20px;
              color: #333;
              z-index: 120;
          }}
          .fortune-box {{
              background: rgba(255,255,255,0.95);
              padding: 40px 10px;
              border-radius: 30px;
              box-shadow: 0 4px 20px rgba(0,0,0,0.1);
              text-align: center;
              width: calc(100% - 10mm);
              max-width: 340px;
              z-index: 100;
              margin: 120px auto;
          }}
          .fortune-box h2 {{
              font-size: 20px;
              color: #999;
              margin-bottom: 10px;
          }}
          .fortune-box h3 {{
              font-size: 24px;
              color: #aa5c5c;
              margin-bottom: 12px;
          }}
          .fortune-box p {{
              font-size: 20px;
              color: #5c5c5c;
              margin: 10px 0;
              line-height: 1.6;
          }}
          .rotating-floating {{
              position: absolute;
              width: 60px;
              opacity: 0.8;
              pointer-events: none;
              z-index: -1; /* 항상 배경에 위치 */
          }}
          @keyframes floatRotateBottomToTop {{
              0% {{ transform: translateY(100vh) rotate(0deg); }}
              100% {{ transform: translateY(-150px) rotate(360deg); }}
          }}
          @keyframes floatRotateTopToBottom {{
              0% {{ transform: translateY(-150px) rotate(0deg); }}
              100% {{ transform: translateY(100vh) rotate(360deg); }}
          }}
          @keyframes floatRotateLeftToRight {{
              0% {{ transform: translateX(-150px) rotate(0deg); }}
              100% {{ transform: translateX(100vw) rotate(360deg); }}
          }}
          @keyframes floatRotateRightToLeft {{
              0% {{ transform: translateX(100vw) rotate(0deg); }}
              100% {{ transform: translateX(-150px) rotate(360deg); }}
          }}
       </style>
    </head>
    <body>
       <div class="fixed-header">복토리</div>
       <div class="greeting" id="greeting"></div>
       <div class="fortune-box">
          <h2>오늘의 운세는 어떨까요?</h2>
          <h3>✨ <span id="name"></span>님의 운세 ✨</h3>
          <p id="score"></p>
          <p id="msg"></p>
       </div>
       <script>
           // 상단 인삿말 타이핑 애니메이션 (반복)
           const greetingText = "안녕하세요 주인님! 오늘도 방문해 주셔서 감사합니다!";
           let greetIndex = 0;
           function typeGreeting() {{
               const greetElem = document.getElementById("greeting");
               greetElem.innerText = greetingText.slice(0, greetIndex);
               greetIndex++;
               if (greetIndex > greetingText.length) {{
                   setTimeout(() => {{
                       greetIndex = 0;
                       typeGreeting();
                   }}, 2000);
               }} else {{
                   setTimeout(typeGreeting, 150);
               }}
           }}
           typeGreeting();
           {script}
           // flying image.png 생성 (배경, 즉시 시작)
           const numCols = 6;
           const numRows = 5;
           const animations = [
               "floatRotateBottomToTop",
               "floatRotateTopToBottom",
               "floatRotateLeftToRight",
               "floatRotateRightToLeft"
           ];
           for (let i = 0; i < numCols * numRows; i++) {{
               const img = document.createElement("img");
               img.src = "/image.png";
               img.className = "rotating-floating";
               const col = i % numCols;
               const row = Math.floor(i / numCols);
               img.style.left = (col * (100 / numCols)) + "%";
               img.style.top = (row * (100 / numRows)) + "%";
               const animationChoice = animations[Math.floor(Math.random() * animations.length)];
               const duration = 15 + Math.random() * 15;
               img.style.animation = animationChoice + " " + duration + "s linear infinite";
               img.style.animationDelay = "0s";
               document.body.appendChild(img);
           }}
       </script>
    </body>
    </html>
    '''
    
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
