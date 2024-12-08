from datetime import datetime
from flask import render_template, request
from run import app
from wxcloudrun.dao import delete_counterbyid, query_counterbyid, insert_counter, update_counterbyid
from wxcloudrun.model import Counters
from wxcloudrun.response import make_succ_empty_response, make_succ_response, make_err_response

import traceback
import random

@app.route('/')
def index():
    """
    :return: 返回index页面
    """
    return render_template('index.html')

@app.route('/api/service', methods=['GET', 'POST'])
def service():
    # Parse request.
    try:
        request_json = request.get_json()
        from_user_name = request_json["FromUserName"]
        to_user_name = request_json["ToUserName"]
        user_content = request_json["Content"]
    except Exception:
        print(traceback.format_exc())
        return make_succ_empty_response()

    # Process.
    response_content = ""
    if user_content.contains("亚亚"):
        func_content = ""
        if user_content.contains("笑话"):
            # 笑话开头列表
            startings = [
                "为什么程序员总是忘记日期？",
                "为什么程序员不喜欢自然光？",
                "为什么程序员总是混淆圣诞节和万圣节？",
            ]

            # 笑话结尾列表
            endings = [
                "因为他们的日历上只有二进制。",
                "因为他们更喜欢黑暗——它不会导致bug。",
                "因为 Oct 31 == Dec 25。",
            ]
            # 随机选择一个开头和一个结尾
            joke_starting = random.choice(startings)
            joke_ending = random.choice(endings)
            func_content = f"给你讲个笑话：\n{joke_starting} \n {joke_ending}\n哈哈哈，好笑不!"
        else:
            func_content = f"我要去带娃了，没时间实现这个功能，先重复下你的话吧:\n{user_content}\n爱你！"
        response_content = f"欧，是我最爱的老婆:\n{func_content}"
    else:
        response_content = f"你谁呀，我只能把你话重复一遍:{user_content}"

    # Generete response json.
    response_json = {
        "ToUserName": from_user_name,
        "FromUserName": to_user_name,
        "CreateTime": int(datetime.now().timestamp()),
        "MsgType": "text",
        "Content": response_content,
    }

    try:
        app.logger.info(f'Request method: {request.method}')
        app.logger.info(f'Request headers: {request.headers}')
        app.logger.info(f'Request form: {request.form}')
        app.logger.info(f'Request data: {request.data}')
    except Exception:
        app.logger.error(traceback.format_exc())

    return make_succ_response(response_json)

@app.route('/api/count', methods=['POST'])
def count():
    """
    :return:计数结果/清除结果
    """

    # 获取请求体参数
    params = request.get_json()

    # 检查action参数
    if 'action' not in params:
        return make_err_response('缺少action参数')

    # 按照不同的action的值，进行不同的操作
    action = params['action']

    # 执行自增操作
    if action == 'inc':
        counter = query_counterbyid(1)
        if counter is None:
            counter = Counters()
            counter.id = 1
            counter.count = 1
            counter.created_at = datetime.now()
            counter.updated_at = datetime.now()
            insert_counter(counter)
        else:
            counter.id = 1
            counter.count += 1
            counter.updated_at = datetime.now()
            update_counterbyid(counter)
        return make_succ_response(counter.count)

    # 执行清0操作
    elif action == 'clear':
        delete_counterbyid(1)
        return make_succ_empty_response()

    # action参数错误
    else:
        return make_err_response('action参数错误')


@app.route('/api/count', methods=['GET'])
def get_count():
    """
    :return: 计数的值
    """
    counter = Counters.query.filter(Counters.id == 1).first()
    return make_succ_response(0) if counter is None else make_succ_response(counter.count)
