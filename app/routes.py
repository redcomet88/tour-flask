from flask import Blueprint, jsonify, request
from werkzeug.security import generate_password_hash, check_password_hash

from app import db
from app.models import Tour, User
from app.schemas import tours_schema, chart_schema, tour_schema, user_schema, users_schema
from app.utils import make_response

main = Blueprint('main', __name__)

# # 这个测试的后面就不需要了，可以删除
# @main.route('/test', methods=['GET'])
# def test():
#     data = [{'id': 1, 'name': 'John'}, {'id': 2, 'name': 'Jane'}]
#     return jsonify(data)

# 十大热门景点(按照评论数排名)
@main.route('/commentsRank', methods=['GET'])
def getCommentsRank():
    try:
        top_tours = Tour.query.order_by(Tour.comments.desc()).limit(10).all()
        result = tours_schema.dump(top_tours)
        return make_response(data=result)
    except Exception as e:
        return make_response(code=1, message=str(e))

# 景点按照评分排名
@main.route('/scoreRank', methods=['GET'])
def getScoreRank():
    try:
        top_tours = Tour.query.filter(Tour.comments>1000).order_by(Tour.score.desc()).limit(5).all()
        result = tours_schema.dump(top_tours)
        return make_response(data=result)
    except Exception as e:
        return make_response(code=1, message=str(e))

# 景点按照城市统计
@main.route('/cityRank', methods=['GET'])
def getCityRank():
    try:
        ret = db.session.query(Tour.city.label('name'),
                               db.func.count(Tour.id).label('value')).group_by(Tour.city).order_by(db.desc('value')).all()
        result = chart_schema.dump(ret)
        return make_response(data=result)
    except Exception as e:
        return make_response(code=1, message=str(e))

@main.route('/tours', methods=['GET'])
def get_tours():
    try:
        title = request.args.get('title', '')  # 获取查询参数中的 title
        page = int(request.args.get('page', 1))  # 获取当前页码，默认为 1
        limit = int(request.args.get('limit', 10))  # 获取每页显示的记录数，默认为 10
        # 根据 title 进行模糊搜索
        query = Tour.query.filter(Tour.title.like(f'%{title}%'))
        # 计算总数和获取当前页数据
        total = query.count()  # 总记录数
        tours = query.offset((page - 1) * limit).limit(limit).all()  # 当前页的数据
        result = tours_schema.dump(tours)  # 使用你的序列化方案处理数据
        return make_response(data={'total': total, 'records': result})
    except Exception as e:
        return make_response(code=1, message=str(e))

@main.route('/tour', methods=['POST'])
def add_tour():
    data = request.json  # 获取JSON数据
    # 这里可以进行数据验证，例如检查必填字段是否存在
    required_fields = ['img', 'title', 'title_en', 'comments', 'score', 'select_comment', 'nation', 'city']
    for field in required_fields:
        if field not in data:
            return make_response(code=1, message= f'错误,缺少字段: {field}')

    notnull_fields = ['title']
    for field in notnull_fields:
        if data[field]=='' or data[field]==None:
            return make_response(code=1, message= f'错误,字段不能为空: {field}')

    # 创建新的景点对象
    new_tour = Tour(
        img=data['img'],
        title=data['title'],
        title_en=data['title_en'],
        comments=data['comments'],
        score=data['score'],
        select_comment=data['select_comment'],
        nation=data['nation'],
        city=data['city'] )

    # 将新景点添加到数据库
    db.session.add(new_tour)
    db.session.commit()
    return make_response(code=0, message='添加景点成功')

@main.route('/tour/<int:id>', methods=['PUT'])
def update_tour(id):
    data = request.json  # 获取JSON数据
    tour = Tour.query.get(id)  # 根据ID查找景点

    if not tour:
        return make_response(code=1, message='景点不存在')

    # 更新景点的字段
    for field in ['img', 'title', 'title_en', 'comments', 'score', 'select_comment', 'nation', 'city']:
        if field in data:
            setattr(tour, field, data[field])

    db.session.commit()
    return make_response(code=0, message='修改景点成功')

@main.route('/tour/<int:id>', methods=['DELETE'])
def delete_tour(id):
    tour = Tour.query.get(id)  # 根据ID查找景点

    if not tour:
        return make_response(code=1, message='景点不存在')

    db.session.delete(tour)
    db.session.commit()
    return make_response(code=0, message='删除景点成功')

# 用户注册接口
@main.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if User.query.filter_by(username=username).first():
        return make_response(code=1, message='用户名已存在')

    hashed_password = generate_password_hash(password)
    new_user = User(username=username, password=hashed_password)

    db.session.add(new_user)
    db.session.commit()

    return make_response(code=0, message='注册成功', data=user_schema.dump(new_user))


# 用户登录接口
@main.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(username=username).first()
    if not user or not check_password_hash(user.password, password):
        return make_response(code=1, message='用户名或者密码错误')

    return make_response(code=0, message='登录成功', data=user_schema.dump(user))

#** 用户信息的增删改查 ***
# 用户列表
@main.route('/users', methods=['GET'])
def get_users():
    try:
        username = request.args.get('username', '')  # 获取查询参数中的 title
        page = int(request.args.get('page', 1))  # 获取当前页码，默认为 1
        limit = int(request.args.get('limit', 10))  # 获取每页显示的记录数，默认为 10
        # 根据 title 进行模糊搜索
        query = User.query.filter(User.username.like(f'%{username}%'), User.deleted==0)
        # 计算总数和获取当前页数据
        total = query.count()  # 总记录数
        records = query.offset((page - 1) * limit).limit(limit).all()  # 当前页的数据
        result = users_schema.dump(records)  # 使用你的序列化方案处理数据
        return make_response(data={'total': total, 'records': result})
    except Exception as e:
        return make_response(code=1, message=str(e))

@main.route('/user/<int:id>', methods=['GET'])
def get_user(id):
    try:
        user = User.query.get(id)  # 根据 ID 查询用户
        result = user_schema.dump(user)  # 使用你的序列化方案处理数据
        return make_response(data=result)
    except Exception as e:
        return make_response(code=1, message=str(e))

@main.route('/user', methods=['POST'])
def add_user():
    data = request.json  # 获取JSON数据

    # 这里可以进行数据验证，例如检查必填字段是否存在
    required_fields = ['username', 'realname', 'job', 'age', 'addr', 'intro', 'phone', 'email']
    for field in required_fields:
        if field not in data:
            return make_response(code=1, message=f'错误,缺少字段: {field}')

    notnull_fields = ['username']
    for field in notnull_fields:
        if data[field]=='' or data[field]==None:
            return make_response(code=1, message= f'错误,字段不能为空: {field}')

    hashed_password = generate_password_hash('123456')

    # 创建新的用户对象
    new_record = User(
        realname=data['realname'],
        username=data['username'],
        password=hashed_password,
        job=data['job'],
        age=data['age'],
        addr=data['addr'],
        intro=data['intro'],
        phone=data['phone'],
        email=data['email'],
        deleted=0
    )

    # 将新景点添加到数据库
    db.session.add(new_record)
    db.session.commit()
    return make_response(code=0, message='添加用户成功')

@main.route('/user/<int:id>', methods=['PUT'])
def update_user(id):
    data = request.json  # 获取JSON数据
    user = User.query.get(id)  # 根据ID查找

    if not user:
        return make_response(code=1, message='用户不存在')

    # 更新字段
    for field in ['realname', 'job', 'addr', 'intro', 'phone', 'email', 'age']:
        if field in data:
            setattr(user, field, data[field])

    db.session.commit()
    return make_response(code=0, message='修改用户成功')

@main.route('/user/<int:id>', methods=['DELETE'])
def delete_user(id):
    user = User.query.get(id)  # 根据ID查找景点

    if not user:
        return make_response(code=1, message='用户不存在')

    user.deleted = 1
    db.session.commit()
    return make_response(code=0, message='删除用户成功')