from main import *
from flask import Blueprint

blueprint = Blueprint("member", __name__, url_prefix="/member")

# @csrf.exempt 데코레이터 사용으로 아래 함수 csrf 예외처리 가능
@blueprint.route("/join", methods=["GET", "POST"])
def member_join():
    if request.method == "POST":
        name = request.form.get("name", type=str)
        email = request.form.get("email", type=str)
        pass1 = request.form.get("pass", type=str)
        pass2 = request.form.get("pass2", type=str)

        if name == "" or email == "" or pass1 == "" or pass2 == "":
            flash("입력되지 않은 값이 있습니다.")
            return render_template("join.html", title="회원가입")

        if pass1 != pass2:
            flash("비밀번호가 일치하지 않습니다.")
            return render_template("join.html", title="회원가입")

        members = mongo.db.members
        cnt = members.find({"email": email}).count()
        if cnt > 0:
            flash("중복된 이메일 주소입니다.")
            return render_template("join.html", title="회원가입")

        current_utc_time = round(datetime.utcnow().timestamp() * 1000)
        post = {
            "name": name,
            "email": email,
            "pass": hash_password(pass1),
            "joindate": current_utc_time,
            "logintime": "",
            "logincount": 0,
        }

        members.insert_one(post)

        return redirect(url_for("lists"))
    else:
        return render_template("join.html", title="회원가입")


@blueprint.route("/login", methods=["GET", "POST"])
def member_login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("pass")
        next_url = request.form.get("next_url")

        members = mongo.db.members
        data = members.find_one({"email": email})

        if data is None:
            flash("회원 정보가 없습니다.")
            return redirect(url_for("member.member_login"))
        else:
            if check_password(data.get("pass"), password):
                current_utc_time = round(datetime.utcnow().timestamp() * 1000)
                members.update_one({"email": email}, {
                    "$set": {"logintime": current_utc_time},
                    "$inc": {"logincount": 1}
                })
                session["email"] = email
                session["name"] = data.get("name")
                session["id"] = str(data.get("_id"))
                session.permanent = True  # 세션은 서버 자원을 사용하므로 사용시간 설정 필요
                if next_url is not None:
                    return redirect(next_url)
                return redirect(url_for("board.lists"))  # 로그인 성공 시 lists 로 redirect
            else:
                flash("비밀번호가 일치하지 않습니다.")
                return redirect(url_for("member.member_login"))
        return ""
    else:
        next_url = request.args.get("next_url", type=str)
        if next_url is not None:
            return render_template("login.html", next_url=next_url, title="회원로그인")
        else:
            return render_template("login.html", title="회원로그인")


@blueprint.route("/logout")
def member_logout():
    try:
        del session["name"]
        del session["id"]
        del session["email"]
    except:
        pass
    return redirect(url_for('member.member_login'))