from flask_sqlalchemy import SQLAlchemy
import os
from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime, timedelta

app = Flask(__name__)

# 보험상담 DB 기본 코드
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # SQLAlchemy 이벤트 시스템 비활성화

db = SQLAlchemy(app)

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # 기본 키 필드 추가
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(100), nullable=False)
    agreement = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # 생성 시간 필드 추가

    def __repr__(self):
        return f'User(name={self.name}, age={self.age}, phone={self.phone}, type={self.type}, agreement={self.agreement})'

with app.app_context():
    db.create_all()  # 데이터베이스와 테이블 생성

@app.route('/')
def index():
    twenty_four_hours_ago = datetime.utcnow() - timedelta(hours=24)
    user_list = Users.query.filter(Users.created_at >= twenty_four_hours_ago).order_by(Users.created_at.desc()).all()
    
    # 전화번호 마스킹 및 시간 차이 계산
    for user in user_list:
        user.phone = f"{user.phone[:3]}-****-{user.phone[9:]}"  # 전화번호 마스킹
        time_diff = datetime.utcnow() - user.created_at
        if time_diff < timedelta(minutes=60):
            user.time_ago = f"{time_diff.seconds // 60}분 전"
        else:
            user.time_ago = f"{time_diff.seconds // 3600}시간 전"

    return render_template('index.html', users=user_list)

@app.route('/user/create/', methods=['GET', 'POST'])  # POST 메서드 추가
def user_create():
    if request.method == 'POST':  # POST 요청 처리
        # form에서 보낸 데이터 받아오기
        name_receive = request.form.get("recipient-name")  # 고객명
        age_receive = request.form.get("recipient-age")  # 고객나이
        phone_receive = request.form.get("recipient-phone")  # 고객번호
        type_receive = request.form.get("recipient-type")  # 상담타입
        agreement_receive = 'y' if request.form.get("recipient-agreement") == 'y' else 'n'  # 개인정보활용동의

        # 데이터를 DB에 저장하기
        users = Users(name=name_receive, age=age_receive, phone=phone_receive, type=type_receive, agreement=agreement_receive)
        db.session.add(users)
        db.session.commit()

        return redirect(url_for('index'))

    return render_template('index.html')  # GET 요청 시 폼 렌더링

@app.route('/document/<int:id>')
def document(id):
    user = Users.query.get_or_404(id)
    return render_template('document.html', user=user)

if __name__ == '__main__':
    app.run(debug=True)  # 디버그 모드 활성화
