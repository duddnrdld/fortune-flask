
			
			
			
			
			
			
			
			
			
			
			
			
			
			
			
			
			
			
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
        <form method="post">
            이름: <input name="name"><br>
            생년월일: <input name="birth" type="date"><br>
            성별: 
            <select name="gender">
                <option>남성</option><option>여성</option>
            </select><br>
            양력/음력: 
            <select name="calendar">
                <option>양력</option><option>음력</option>
            </select><br>
            <button type="submit">운세 확인</button>
        </form>
    '''

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)

