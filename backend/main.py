# 第三方类--------------------------------
from fastapi import FastAPI, Request, BackgroundTasks
from fastapi.responses import HTMLResponse
from starlette.templating import Jinja2Templates
import uvicorn,hashlib,json,time,re,markdown
from datetime import datetime
from qiniu import Auth
# 自定义类-------------------------------
import lib.api as api
from lib.db import *
from lib.schemas import * 
from lib.function import *
# -------------------------------------
app = FastAPI(docs_url=None)
templates = Jinja2Templates(directory="templates")
# 七牛云储存图片配置-----------------------
QINIU_ACCESS_KEY = ''# AK
QINIU_SECRET_KEY = ''# SK
QINIU_BUCKET = ''# 空间名称
QINIU_UPLOAD_URL = "" #区域域名列
QINIU_CDN_DOMAIN = "" #自定义源站域名
# ！！！ 数据库也需要配置
# -------------------------------------

@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# TODO 公告功能 开发ing
@app.get("/data")
def read_root():
    return {"ICP": "粤ICP备2024179917号-2X","app_version": "001","topic":"程序内测中，数据有可能会丢失，有意合作请联系。"}

# 注册与登录 （只有登录，无需注册。逻辑：用户输入手机号码-如存在用户直接验证密码-如不存在直接注册）
@app.post("/login")
async def login(login:Login,request:Request,background_tasks: BackgroundTasks):

    systeminfo = login.systemInfo
    user = login.user
    password = login.password
    client_ip = request.client.host
    # 先校验手机号码和密码格式
    if not validate_phone(user):
        return {"code": 0, "msg": "手机号码格式不正确", "errcode": 10003}
    if not validate_password(password):
        return {"code": 0, "msg": "密码格式不符合要求,仅数字、大小写字母、常用特殊符号且大于6个字符", "errcode": 10004}

    # 获取数据库连接
    connect = get_db_connection()
    try:
        cursor = connect.cursor()
        # 查询用户是否存在
        sql_check = "SELECT password,name FROM users WHERE username = %s"
        cursor.execute(sql_check, (user,))
        result = cursor.fetchone()
        if result:
            # 用户存在，检查密码是否正确
            if result[0] == password:
                
                background_tasks.add_task(log_event, "login_success", user, client_ip, systeminfo)
                return {"code": 1, "msg": "登录成功" ,"user":user, "name":result[1]}
            else:
                background_tasks.add_task(log_event, "login_fail", user, client_ip, systeminfo)
                return {"code": 0, "msg": "密码错误,或手机号码已存在", "errcode": 10001}
        else:
            # 用户不存在，进行注册
            sql_insert = "INSERT INTO users (username, password,reg_system_info,rg_ip,rg_date,name) VALUES (%s, %s, %s, %s, %s, %s)"
            cursor.execute(sql_insert, (user, password, systeminfo, client_ip, datetime.now(),"未设置"))
            connect.commit()
            return {"code": 1, "msg": "注册成功","user":user, "name":"未设置"}
    except Exception as e:
        print(e)
        return {"code": 0, "msg": "操作出现异常", "errcode": 10002}
    except Exception as e:
        print(e)
        return {"code": 0, "msg": "操作出现异常", "errcode": 10002}
    finally:
        cursor.close()
        connect.close()

# TODO 重置密码 暂未完成
@app.post("/reset_password")
async def reset_password(resetpassword: ResetPassword):
    phone = resetpassword.user
    new_password = resetpassword.password
    
    # 校验手机号格式
    if not validate_phone(phone):
        return {"code": 0, "msg": "手机号码格式不正确", "errcode": 10003}
    # 校验新密码格式
    if not validate_password(new_password):
        return {"code": 0, "msg": "新密码格式不符合要求", "errcode": 10004}

    # 获取数据库连接
    connect = get_db_connection()
    try:
        cursor = connect.cursor()
        # 先查询手机号对应的用户是否存在
        sql_check_user = "SELECT * FROM users WHERE username = %s"
        cursor.execute(sql_check_user, (phone,))
        result = cursor.fetchone()
        if result:
            # 用户存在，更新密码
            sql_update_password = "UPDATE users SET password = %s WHERE username = %s"
            cursor.execute(sql_update_password, (new_password, phone))
            connect.commit()
            return {"code": 1, "msg": "密码重置成功"}
        else:
            return {"code": 0, "msg": "手机号未注册，无法重置密码", "errcode": 10005}
    except Exception as e:
        print(e)
        return {"code": 0, "msg": "操作出现异常", "errcode": 10002}
    finally:
        cursor.close()
        connect.close()

# 设置用户个人信息
@app.post("/setUserInfo")
async def set_user_info(userinfo: UserInfo,request:Request,background_tasks: BackgroundTasks):
    user = userinfo.user
    name = userinfo.name
    gender = userinfo.gender
    age = userinfo.age
    height = userinfo.height
    weight = userinfo.weight
    activityLevel = userinfo.activityLevel
    systeminfo = userinfo.systemInfo
    client_ip = request.client.host
    
    # 数据校验
    if not user or not validate_phone(user):
        return {"code": 0, "msg": "用户未登录", "errcode": 10003}
    if not name:
        return {"code": 0, "msg": "姓名不能为空", "errcode": 10008}
    if gender not in ["男", "女"]:
        return {"code": 0, "msg": "性别必须为男或女", "errcode": 10006}
    if not (1 <= age <= 120):
        return {"code": 0, "msg": "年龄必须在1到120之间", "errcode": 10009}
    if not (50 <= height <= 250):
        return {"code": 0, "msg": "身高必须在50到250厘米之间", "errcode": 10010}
    if not (30 <= weight <= 300):
        return {"code": 0, "msg": "体重必须在30到300公斤之间", "errcode": 10011}
    if activityLevel not in [0, 1, 2, 3]:
        return {"code": 0, "msg": "无效的活动水平", "errcode": 10007}
    
    # 根据Mifflin-St Jeor公式计算BMR
    if gender == "男":
        bmr = (10 * weight) + (6.25 * height) - (5 * age) + 5
    elif gender == "女":
        bmr = (10 * weight) + (6.25 * height) - (5 * age) - 161
    else:
        return {"code": 0, "msg": "性别必须为男或女", "errcode": 10006}
    
    
    # 根据activityLevel计算PAL
    if activityLevel == 0:
        pal = 1.2  # 久坐或很少活动
    elif activityLevel == 1:
        pal = 1.375  # 轻度活动
    elif activityLevel == 2:
        pal = 1.55  # 中度活动
    elif activityLevel == 3:
        pal = 1.725  # 重度活动
    else:
        return {"code": 0, "msg": "无效的活动水平", "errcode": 10007}

    # 计算TDEE
    tdee = bmr * pal

    user_info_combin = f"{name}的年龄是{age}岁，基础代谢率为{bmr}千卡，身高{height}cm，PAL数值{pal}，总能量消耗{tdee}千卡，性别{gender}，体重{weight}kg"
    
    # 获取数据库连接
    connect = get_db_connection()
    
    try:
        cursor = connect.cursor()
        # 检查用户是否存在
        sql_check_user = "SELECT * FROM user_info WHERE user = %s"
        cursor.execute(sql_check_user, (user,))
        existing_user = cursor.fetchone()

        if existing_user:
            # 用户存在，更新其他字段
            sql_update_user = "UPDATE user_info SET name = %s, gender = %s, age = %s, height = %s, weight = %s, activity_level = %s, bmr = %s, pal = %s, tdee = %s, user_info_combin = %s, time = %s WHERE user = %s"
            user_data = (name, gender, age, height, weight, activityLevel, bmr, pal, tdee, user_info_combin, datetime.now().strftime('%Y-%m-%d %H:%M:%S'), user)
            cursor.execute(sql_update_user, user_data)
            connect.commit()
            # 更新users表中的name字段
            us_sql = "UPDATE users SET name = %s WHERE username = %s"
            us_data = (name, user)
            cursor.execute(us_sql, us_data)
            connect.commit()
            
            background_tasks.add_task(log_event, "update_user_info", user, client_ip, systeminfo)
            return {"code": 1, "msg": "用户信息更新成功"}
        else:
            # 用户不存在，插入新的用户信息
            sql_insert_user = "INSERT INTO user_info (user, name, gender, age, height, weight, activity_level, bmr, pal, tdee, user_info_combin, time) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            user_data = (user, name, gender, age, height, weight, activityLevel, bmr, pal, tdee, user_info_combin, datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            cursor.execute(sql_insert_user, user_data)
            connect.commit()
            # 更新users表中的name字段
            us_sql = "UPDATE users SET name = %s WHERE username = %s"
            us_data = (name, user)
            cursor.execute(us_sql, us_data)
            connect.commit()
            # 记录log
            background_tasks.add_task(log_event, "add_user_info", user, client_ip, systeminfo)
            return {"code": 1, "msg": "用户信息设置成功"}
    except Exception as e:
        connect.rollback()
        return {"code": 0, "msg": f"操作失败: {str(e)}", "errcode": 10002}
    finally:
        cursor.close()
        connect.close()        

# 获取用户个人信息
@app.post("/getUserInfo")
async def get_user_info(getuserinfo: GetUserInfo,request:Request,background_tasks: BackgroundTasks):
    user = getuserinfo.user
    code = getuserinfo.code
    systeminfo = getuserinfo.systemInfo
    client_ip = request.client.host
    
    deviceId = json.loads(systeminfo)
    md_org = str(user) + deviceId['deviceId']
    md_en = md_org.encode('utf-8')
    md5_hash =  hashlib.md5(md_en)
    
    # 获取数据库连接
    connect = get_db_connection()

    try:
        cursor = connect.cursor()
        # 查询用户信息
        sql_get_user_info = "SELECT * FROM user_info WHERE user = %s"
        cursor.execute(sql_get_user_info, (user,))
        user_info = cursor.fetchone()
        background_tasks.add_task(log_event, "get_user_info", user, client_ip, systeminfo)
        # log_event("get_user_info", user, client_ip, systeminfo)
        user_info_dict = {
                "user": user_info[0],
                "name": user_info[1],
                "gender": user_info[2],
                "age": user_info[3],
                "height": user_info[4],
                "weight": user_info[5],
                "activity_level": user_info[6],
                "bmr": user_info[7],
                "pal": user_info[8],
                "tdee": user_info[9],
                "user_info_combin": user_info[11],
                "time": user_info[10]
        }
        
        if user_info:
            # 返回用户信息
            return {"code": 1, "msg": "用户信息获取成功", "data": user_info_dict}
        else:
            return {"code": 0, "msg": "用户不存在", "errcode": 10004}
    except Exception as e:
        return {"code": 0, "msg": f"操作失败: {str(e)}", "errcode": 10002}
    finally:
        cursor.close()
        connect.close()

# 给前端上传食物图片的凭证
@app.post("/getUploadSet")
async def upload_food_image(uploadset: UploadSet,request:Request):
    user = uploadset.user
    systeminfo = uploadset.systemInfo
    client_ip = request.client.host

    # 获取数据库连接
    connect = get_db_connection()

    try:
        cursor = connect.cursor()
        # 查询用户是否存在
        sql_check_user = "SELECT COUNT(*) FROM user_info WHERE user = %s"
        cursor.execute(sql_check_user, (user,))
        user_count = cursor.fetchone()[0]
        log_event("upload_image", user, client_ip, systeminfo)

        if user_count > 0:
            # 用户存在，生成上传凭证
            access_key = QINIU_ACCESS_KEY
            secret_key = QINIU_SECRET_KEY
            upload_url = QINIU_UPLOAD_URL
            bucket_name = QINIU_BUCKET
            upload_file_name = "file"
            now = datetime.now()
            date = now.strftime('%Y%m%d%H%M%S')
            key = "food/food-" + user + "-" + date

            q = Auth(access_key, secret_key)
            token = q.upload_token(bucket_name)

            return {
                "code": 1,
                "msg": "success",
                "token": token,
                "upload_url": upload_url,
                "upload_file_name": upload_file_name,
                "key": key
            }
        else:
            # 用户不存在，返回错误信息
            return {
                "code": 0,
                "msg": "用户不存在",
                "errcode": 10004
            }
    except Exception as e:
        return {
            "code": 0,
            "msg": f"操作失败: {str(e)}",
            "errcode": 10002
        }
    finally:
        cursor.close()
        connect.close()

# ai分析图片 
@app.post("/ai")
def ai_scarne(getdata:AiScarne,request:Request,background_tasks: BackgroundTasks):
    # 前端接收到的数据
    user = getdata.user
    systeminfo = getdata.systemInfo
    data = getdata.data
    client_ip = request.client.host
    # 数据解析与拼接
    de_data = json.loads(data)
    image_url = QINIU_CDN_DOMAIN + "/" + de_data["key"]
    # 进行ai识图分析 返回json数据
    ai_data_json = api.ai_scarn_picture(image_url,user)
    
    # 判断识别结果
    if ai_data_json["msg"] == "success":
        # 识别到健康数据
        background_tasks.add_task(log_event, "ai_scarn_picture", user, client_ip, systeminfo)
        # 返回数据给前端
        rtdata = {
            "code":1,
            "msg":"success",
            "type":"",
            "content":""
        }
        if ai_data_json["type"] == "food":
            # 识别到是食物
            rtdata["type"] = "✅食物记录"
            rtdata["content"] = ai_data_json["食品名字"]
            background_tasks.add_task(ai_food_analyse,user,ai_data_json,image_url,client_ip,systeminfo)
            
        elif ai_data_json["type"] == "sport":
            # 识别到是运动软件截图
            rtdata["type"] = "🏅运动记录"
            rtdata["content"] = ai_data_json["总消耗卡路里"] + ai_data_json["单位"]
            background_tasks.add_task(ai_sport_analyse,user,ai_data_json,image_url,client_ip,systeminfo)
            
        elif ai_data_json["type"] == "weight":
            # 识别到是体重数据
            rtdata["type"] = "📊体重记录"
            rtdata["content"] = ai_data_json["体重"] + ai_data_json["单位"]
            background_tasks.add_task(ai_weight_analyse,user,ai_data_json,image_url,client_ip,systeminfo)

        else:
            # 识别到是其他类型
            rtdata["type"] = "❌不知道是什么"
            rtdata["content"] = ai_data_json
        
        return rtdata

    else:
        # 识别不到任何数据
        background_tasks.add_task(log_event, "ai_scarn_picture_fail", user, client_ip, systeminfo)
        return {"code":0,"msg":ai_data_json["err_msg"],"data":ai_data_json}

# 食物事件    
def ai_food_analyse(user, aidata, image, client_ip, systeminfo):
    # 根据分析到的食物数据 再分析
    jo_aidata = json.dumps(aidata, ensure_ascii=False)  # Ensure Chinese characters are not escaped
    # 基础数据
    food_id = user + "_" + str(int(time.time()))
    food_user = user
    food_image = image
    food_name = aidata["食品名字"]
    food_cal = aidata["总卡路里估算"]
    # 获取食物千卡 单纯是数字
    pattern_cal = r"=\s*(\d+)\s*千卡"
    food_cal_de = re.search(pattern_cal,food_cal)
    if food_cal_de:
        food_cal_int = food_cal_de.group(1)
    # 日期转化
    food_time = str(int(time.time()))
    food_time_de = time.strftime('%H:%M:%S', time.localtime(int(time.time())))
    food_date = time.strftime('%Y%m%d', time.localtime(int(time.time())))
    # 营养怪博士 返回信息
    food_assistant = api.ai_nutrition_assistant(str(aidata))
    
    # 插入食物数据到food表
    connect = get_db_connection()
    try:
        cursor = connect.cursor()
        sql_insert_food = """
            INSERT INTO food (food_id, food_url, food_data, food_name, food_cal, food_assistant, food_time, food_time_de, food_date, user)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(sql_insert_food, (food_id, food_image, jo_aidata, food_name, food_cal_int, food_assistant, food_time, food_time_de, food_date, food_user))
        connect.commit()
        insert_record(food_id,food_image,"food",jo_aidata,food_name,food_time,food_time_de,food_date,food_user)
        log_event("ai_food_analyse_success", user, client_ip, systeminfo)
    except Exception as e:
        print(f"Failed to insert food data: {e}")
        log_event("ai_food_analyse_fail", user, client_ip, systeminfo)
        connect.rollback()
    finally:
        cursor.close()
        connect.close()
        
    
# 运动事件
def ai_sport_analyse(user,aidata,image,client_ip,systeminfo):
    jo_aidata = json.dumps(aidata, ensure_ascii=False)  # Ensure Chinese characters are not escaped
    # 基础数据
    sport_id = user + "_" + str(int(time.time()))
    sport_user = user
    soprt_image = image
    sport_cal = aidata["总消耗卡路里"]
    sport_cal_operation = aidata["单位"]
    sport_duration = aidata["运动时长"]
    # 时间数据
    sport_time = str(int(time.time()))
    sport_time_de = time.strftime('%H:%M:%S', time.localtime(int(time.time())))
    sport_date = time.strftime('%Y%m%d', time.localtime(int(time.time())))
    # 运动小助手
    sport_assistant = "TODO"
    
    # 插入运动数据到sport表
    connect = get_db_connection()
    try:
        cursor = connect.cursor()
        sql_insert_sport = """
            INSERT INTO sport (sport_id, sport_url, sport_data, sport_cal, sport_duration, sport_cal_operation, sport_assistant, sport_time, sport_time_de, sport_date, user)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(sql_insert_sport, (sport_id, soprt_image, jo_aidata, sport_cal, sport_duration, sport_cal_operation, sport_assistant, sport_time, sport_time_de, sport_date, sport_user))
        connect.commit()
        sport_name = "运动消耗：" + sport_cal + sport_cal_operation
        insert_record(sport_id,soprt_image,"sport",jo_aidata,sport_name,sport_time,sport_time_de,sport_date,sport_user)
        log_event("ai_sport_analyse_success", user, client_ip, systeminfo)
    except Exception as e:
        print(f"Failed to insert sport data: {e}")
        log_event("ai_sport_analyse_fail", user, client_ip, systeminfo)
        connect.rollback()
    finally:
        cursor.close()
        connect.close()
        
    # TODO 插入到结合事件中
    
# 体重事件
def ai_weight_analyse(user,aidata,image,client_ip,systeminfo):
    jo_aidata = json.dumps(aidata, ensure_ascii=False)  # Ensure Chinese characters are not escaped
    # 基础数据
    weight_id = user + "_" + str(int(time.time()))
    weight_user = user
    weight_image = image
    weight_weight = aidata["体重"]
    weight_operation = aidata["单位"] #g
    try:
        if weight_operation == "公斤":
            weight_weight_int = float(weight_weight) * 2
        elif weight_operation == "斤":
            weight_weight_int = float(weight_weight)
        elif weight_operation == "kg":
            weight_weight_int = float(weight_weight) * 2
        elif weight_operation == "g":
            weight_weight_int = float(weight_weight)
        else:
            log_event("weight_operation_error",user,client_ip,systeminfo)
            return
    except Exception as e:
        log_event("get_weight_operation_error",user,client_ip,systeminfo)
        return
    
    # 时间数据
    weight_time = str(int(time.time()))
    weight_time_de = time.strftime('%H:%M:%S', time.localtime(int(time.time())))
    weight_date = time.strftime('%Y%m%d', time.localtime(int(time.time())))
    
    # 插入体重数据到weight表
    connect = get_db_connection()
    try:
        cursor = connect.cursor()
        sql_insert_weight = """
            INSERT INTO weight (weight_id, weight_url, weight_data, weight_weight, weight_time, weight_time_de, weight_date, user)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(sql_insert_weight, (weight_id, weight_image, jo_aidata, weight_weight_int, weight_time, weight_time_de, weight_date, weight_user))
        connect.commit()
        
        # 体重换为公斤
        weight_weight_kg = weight_weight_int / 2
        
        # 获取用户信息以更新user_info_combin
        sql_get_user_info = "SELECT * FROM user_info WHERE user = %s"
        cursor.execute(sql_get_user_info, (weight_user,))
        user_info = cursor.fetchone()
        
        if user_info:
            name = user_info[1]
            gender = user_info[2]
            age = float(user_info[3])    # 转换为float
            height = float(user_info[4])  # 转换为float
            pal = float(user_info[8])     # 转换为float
            
            # 确保weight_weight_kg是float类型
            weight_weight_kg = float(weight_weight_kg)
            
            # 计算BMR
            if gender == "男":
                bmr = (10 * weight_weight_kg) + (6.25 * height) - (5 * age) + 5
            elif gender == "女":
                bmr = (10 * weight_weight_kg) + (6.25 * height) - (5 * age) - 161
            # 计算TDEE
            tdee = bmr * pal
            
            # 四舍五入到2位小数
            bmr = round(bmr, 2)
            tdee = round(tdee, 2)
            
            # 更新user_info_combin
            user_info_combin = f"{name}的年龄是{age}岁，基础代谢率为{bmr}千卡，身高{height}cm，PAL数值{pal}，总能量消耗{tdee}千卡，性别{gender}，体重{weight_weight_kg}kg"

        # 更新users表中的weight字段
        us_sql = "UPDATE user_info SET weight = %s,user_info_combin = %s WHERE user = %s"
        us_data = (weight_weight_kg, user_info_combin, weight_user)
        cursor.execute(us_sql, us_data)
        connect.commit()
        weight_name = "更新体重：" + weight_weight + weight_operation
        insert_record(weight_id,weight_image,"weight",jo_aidata,weight_name,weight_time,weight_time_de,weight_date,weight_user)
        log_event("ai_weight_analyse_success", user, client_ip, systeminfo)
    except Exception as e:
        print(f"Failed to insert weight data: {e}")
        log_event("ai_weight_analyse_fail", user, client_ip, systeminfo)
        connect.rollback()
    finally:
        cursor.close()
        connect.close()
   
# 获取今日事件
@app.post("/getDailyEvent")
async def get_daily_record(daily:GetDaily,request:Request,background_tasks: BackgroundTasks):
    user = daily.user
    systeminfo = daily.systemInfo
    client_ip = request.client.host
    date = daily.date
    # 获取数据库连接
    connect = get_db_connection()
    try:
        cursor = connect.cursor(pymysql.cursors.DictCursor)
        
        # 查询daily表今日记录
        sql_daily = """
            SELECT * FROM daily
            WHERE user = %s AND daily_date = %s
        """
        cursor.execute(sql_daily, (user, date))
        daily_result = cursor.fetchone()
        
        # 查询record表今日记录，按时间倒序
        sql_record = """
            SELECT * FROM record
            WHERE user = %s AND record_date = %s
            ORDER BY record_time DESC
        """
        cursor.execute(sql_record, (user, date))
        record_results = cursor.fetchall()
        
        # 组织返回数据
        response_data = {
            "daily": daily_result,
            "records": record_results
        }
        # 处理空的systeminfo
        if not systeminfo:
            systeminfo = json.dumps({"deviceId": "unknown"})
            
        if daily_result or record_results:
            # 返回查询结果
            background_tasks.add_task(log_event, "get_daily_record_success", user, client_ip, systeminfo)
            return {
                "code": 1,
                "msg": "获取今日记录成功",
                "data": response_data
            }
        else:
            # 没有找到记录
            background_tasks.add_task(log_event, "get_daily_record_not_found", user, client_ip, systeminfo)
            return {
                "code": 0,
                "msg": "今日没有记录",
                "errcode": 10012
            }
    except Exception as e:
        # 确保systeminfo不为空
        systeminfo = systeminfo or json.dumps({"deviceId": "unknown"})
        background_tasks.add_task(log_event, "get_daily_record_fail", user, client_ip, systeminfo)
        return {
            "code": 0,
            "msg": f"获取今日记录失败: {str(e)}",
            "errcode": 10002
        }
    finally:
        cursor.close()
        connect.close()
        
# 每日记录详情 html页面
@app.get("/get_daily_detail/{daily_id}", response_class=HTMLResponse)
async def get_daily_detail(daily_id: str, request: Request):
    # 获取数据库连接
    connect = get_db_connection()
    try:
        cursor = connect.cursor()
        # 查询daily表
        sql = """
            SELECT daily_id, daily_coach, daily_date, user
            FROM daily
            WHERE daily_id = %s
        """
        cursor.execute(sql, (daily_id,))
        result = cursor.fetchone()
        
        if result:
            # 返回查询结果
            daily_id = result[0]
            daily_coach = result[1]
            daily_date = result[2]
            user = result[3]
            
            # 处理markdown内容
            mk = daily_coach
            mk = mk.strip()  # 去除首尾空白
            mk = '\n'.join(line.strip() for line in mk.splitlines())  # 去除每行首尾空白
            
            # 预处理markdown内容
            lines = mk.splitlines()
            processed_lines = []
            in_list = False
            
            for line in lines:
                # 处理分割线
                if line.strip() == '---':
                    processed_lines.append('')  # 添加空行
                    processed_lines.append('---')  # 保留分割线
                    processed_lines.append('')  # 添加空行
                    continue
                    
                # 处理列表
                if line.strip().startswith('-'):
                    if not in_list:
                        processed_lines.append('')  # 添加空行开始新列表
                        in_list = True
                    # 转换为标准markdown列表格式
                    processed_lines.append(line.replace('-', '*', 1).strip())
                else:
                    if in_list:
                        processed_lines.append('')  # 添加空行结束列表
                        in_list = False
                    processed_lines.append(line)
            
            mk = '\n'.join(processed_lines)
            
            html = markdown.markdown(mk, extensions=[
                'extra',
                'toc',
                'tables',
                'fenced_code',
                'footnotes',
                'smarty',
                'admonition',
                'meta',
                'nl2br',
                'sane_lists',
                'wikilinks',
                'attr_list',
                'pymdownx.arithmatex',
                'pymdownx.betterem',
                'pymdownx.caret',
                'pymdownx.details',
                'pymdownx.emoji',
                'pymdownx.inlinehilite',
                'pymdownx.magiclink',
                'pymdownx.mark',
                'pymdownx.smartsymbols',
                'pymdownx.superfences',
                'pymdownx.tabbed',
                'pymdownx.tasklist',
                'pymdownx.tilde'
            ])
            
            return templates.TemplateResponse("daily.html", {"request": request, "html": html, "image": ""})
            
        else:
            return templates.TemplateResponse("error.html", {
                "request": request,
                "error_message": "未找到该每日记录"
            })
    except Exception as e:
        return templates.TemplateResponse("error.html", {
            "request": request,
            "error_message": f"查询失败: {str(e)}"
        })
    finally:
        cursor.close()
        connect.close()

# 食物详情 html页面
@app.get("/get_food_detail/{food_id}" ,response_class=HTMLResponse)
async def get_food_detail(food_id: str,request: Request):
    # 获取数据库连接
    connect = get_db_connection()
    try:
        cursor = connect.cursor()
        # 查询food表
        sql = """
            SELECT food_id, food_url, food_data, food_name, food_cal,
                   food_assistant, food_time, food_time_de, food_date, user
            FROM food
            WHERE food_id = %s
        """
        cursor.execute(sql, (food_id,))
        result = cursor.fetchone()
        
        if result:
            # 返回查询结果
            # 将查询结果转换为Python变量
            food_id = result[0]
            food_url = result[1]
            food_data = json.loads(result[2])  # 解析JSON字符串
            food_name = result[3]
            food_cal = int(result[4])  # 转换为整数
            food_assistant = result[5]  # markdown内容
            food_time = result[6]
            food_time_de = result[7]
            food_date = result[8]
            user = result[9]
            mk = food_assistant
            mk = mk.strip()  # 去除首尾空白
            mk = '\n'.join(line.strip() for line in mk.splitlines())  # 去除每行首尾空白
            # 预处理markdown内容
            lines = mk.splitlines()
            processed_lines = []
            in_list = False
            
            for line in lines:
                # 处理分割线
                if line.strip() == '---':
                    processed_lines.append('')  # 添加空行
                    processed_lines.append('---')  # 保留分割线
                    processed_lines.append('')  # 添加空行
                    continue
                    
                # 处理列表
                if line.strip().startswith('-'):
                    if not in_list:
                        processed_lines.append('')  # 添加空行开始新列表
                        in_list = True
                    # 转换为标准markdown列表格式
                    processed_lines.append(line.replace('-', '*', 1).strip())
                else:
                    if in_list:
                        processed_lines.append('')  # 添加空行结束列表
                        in_list = False
                    processed_lines.append(line)
            
            mk = '\n'.join(processed_lines)
            
            html = markdown.markdown(mk, extensions=[
                'extra',
                'toc',
                'tables',
                'fenced_code',
                'footnotes',
                'smarty',
                'admonition',
                'meta',
                'nl2br',
                'sane_lists',
                'wikilinks',
                'attr_list',
                'pymdownx.arithmatex',
                'pymdownx.betterem',
                'pymdownx.caret',
                'pymdownx.details',
                'pymdownx.emoji',
                'pymdownx.inlinehilite',
                'pymdownx.magiclink',
                'pymdownx.mark',
                'pymdownx.smartsymbols',
                'pymdownx.superfences',
                'pymdownx.tabbed',
                'pymdownx.tasklist',
                'pymdownx.tilde'
            ])
            
            return templates.TemplateResponse("food.html", {"request": request,"html": html,"image":food_url})
            
        else:
            return templates.TemplateResponse("error.html", {
                "request": request,
                "error_message": "未找到该食物记录"
            })
    except Exception as e:
        return templates.TemplateResponse("error.html", {
            "request": request,
            "error_message": f"查询失败: {str(e)}"
        })
    finally:
        cursor.close()
        connect.close()
        
        
@app.get("/contract/{type}", response_class=HTMLResponse)
async def contract_page(type: str, request: Request):
    if type == "private":
        return templates.TemplateResponse("contract_private.html", {"request": request})
    elif type == "user":
        return templates.TemplateResponse("contra_user.html", {"request": request})
    else:
        return templates.TemplateResponse("error.html", {
            "request": request,
            "error_message": "Invalid contract type"
        })

# 获取今日第一顿进食时间
@app.post("/getFirstMealTime")
async def get_first_meal_time(getmeal: GetLastMealTime, request: Request, background_tasks: BackgroundTasks):
    user = getmeal.user
    systeminfo = getmeal.systemInfo
    client_ip = request.client.host
    today = datetime.now().strftime('%Y%m%d')
    
    # 获取数据库连接
    connect = get_db_connection()
    try:
        cursor = connect.cursor()
        
        # 查询用户是否存在
        sql_check_user = "SELECT COUNT(*) FROM users WHERE username = %s"
        cursor.execute(sql_check_user, (user,))
        user_count = cursor.fetchone()[0]
        
        if user_count == 0:
            background_tasks.add_task(log_event, "get_first_meal_time_user_not_found", user, client_ip, systeminfo)
            return {"code": 0, "msg": "用户不存在", "errcode": 10004}
            
        # 查询今日最早一次进食时间
        sql_get_first_meal = """
            SELECT food_time
            FROM food
            WHERE user = %s AND food_date = %s
            ORDER BY food_time ASC
            LIMIT 1
        """
        cursor.execute(sql_get_first_meal, (user, today))
        first_meal = cursor.fetchone()
        
        if first_meal:
            background_tasks.add_task(log_event, "get_first_meal_time_success", user, client_ip, systeminfo)
            
            return {"code": 1, "First":True, "msg": "获取今日第一顿进食时间成功", "data": {"first_meal_time": first_meal[0]}}
        else:
            background_tasks.add_task(log_event, "get_first_meal_time_no_record", user, client_ip, systeminfo)
            return {"code": 1, "First":False, "msg": "今日没有进食记录", "errcode": 10014}
            
    except Exception as e:
        background_tasks.add_task(log_event, "get_first_meal_time_fail", user, client_ip, systeminfo)
        return {"code": 0, "msg": f"获取今日第一顿进食时间失败: {str(e)}", "errcode": 10002}
    finally:
        cursor.close()
        connect.close()


if __name__ == "__main__":
    uvicorn.run(app='main:app', host='0.0.0.0', port=8000, reload=True)
    