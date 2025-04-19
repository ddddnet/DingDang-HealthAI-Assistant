import pymysql,json
from datetime import datetime
import lib.api as api

# 获取数据库连接
def get_db_connection():
    connection = pymysql.connect(
        host="mysql",  # 你的数据库主机地址，这里以本地为例
        user="ai",  # 数据库用户名
        password="",  # 数据库密码
        database="ai"  # 数据库名
    )
    return connection

# 记录事件到日志表中
def log_event(event, user, client_ip, systeminfo):
    """
    记录事件到日志表中。

    :param event: 事件类型，例如 "log_success"
    :param user: 用户名
    :param client_ip: 客户端IP地址
    :param systeminfo: 系统信息
    """
    sql_log_event = "INSERT INTO log (event, user, time, ip, system_info) VALUES (%s, %s, %s, %s, %s)"
    connect = get_db_connection()
    try:
        cursor = connect.cursor()
        cursor.execute(sql_log_event, (event, user, datetime.now(), client_ip, systeminfo))
        connect.commit()
    except Exception as e:
        connect.rollback()
        print(f"记录事件失败: {str(e)}")
    finally:
        connect.close()

# 插入事件到记录表中 目的是为了前端展示
def insert_record(id,url,type,aidata,title,time,time_de,date,user):
    record_id = id
    record_type = type
    record_aidata = aidata
    record_url = url
    record_title = title
    record_time = time
    record_time_de = time_de
    record_date = date
    record_user = user
    connect = get_db_connection()
    try:
        cursor = connect.cursor()
        sql_insert_record = """
            INSERT INTO record (record_id, record_url, record_type, aidata, record_title, record_date, record_time, record_time_de, user)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(sql_insert_record, (record_id, record_url, record_type, record_aidata, record_title, record_date, record_time, record_time_de, record_user))
        connect.commit()
        
        # 执行ai分析
        day_hole(user,date)
        
    except Exception as e:
        print(f"Failed to insert record: {e}")
        connect.rollback()
    finally:
        cursor.close()
        connect.close()
       
# 统计以及获取今日所有数据 交由ai处理 获得数据后 返回数据插入数据库
def day_hole(user, date):
    connect = get_db_connection()
    try:
        cursor = connect.cursor(pymysql.cursors.DictCursor)
        
        # 查询user_info表获取user_info_combin
        sql_user_info = "SELECT user_info_combin FROM user_info WHERE user = %s"
        cursor.execute(sql_user_info, (user,))
        user_info_result = cursor.fetchone()
        user_info_combin = user_info_result['user_info_combin'] if user_info_result else None
        
        # 查询record表，仅选择指定字段
        sql_record = """
            SELECT
                record_id,
                record_type,
                aidata,
                record_title,
                record_date,
                record_time,
                record_time_de
            FROM record
            WHERE user = %s AND record_date = %s
        """
        cursor.execute(sql_record, (user, date))
        results = cursor.fetchall()
        
        # 按record_type分类存储
        weight_records = []
        sport_records = []
        food_records = []
            
        for record in results:
            if record['record_type'] == 'weight':
                weight_records.append(record)
            elif record['record_type'] == 'sport':
                sport_records.append(record)
            elif record['record_type'] == 'food':
                food_records.append(record)
                
        records_data = {
            '今日体重记录': weight_records,
            '今日运动记录': sport_records, 
            '今日饮食记录': food_records
        }
        records_json_data = json.dumps(records_data, ensure_ascii=False)
        
        count_res_str = api.healthy_data_count(user_info_combin,records_json_data)
        count_res_dict = json.loads(count_res_str)
        # {'基础代谢': 1206.75, '体重': 48.65, '是否超标': True, '进食顿数': 2, '摄入卡路里': 1830, '碳水': 97, '蛋白质': 105, '脂肪': 64, '膳食纤维': 10}
        
        healthy_res = api.healthy_report(user_info_combin,records_json_data)
        
        # 更新daily表记录
        daily_id = user + "_" + date
        connect = get_db_connection()
        try:
            cursor = connect.cursor()
            
            # 检查记录是否存在
            sql_check = "SELECT daily_id FROM daily WHERE user = %s AND daily_date = %s"
            cursor.execute(sql_check, (user, date))
            exists = cursor.fetchone()
            
            if exists:
                # 更新记录
                sql_update = """
                    UPDATE daily SET
                        daily_TDEE = %s,
                        daily_weight = %s,
                        daily_count = %s,
                        daily_cal = %s,
                        daily_carbon = %s,
                        daily_protein = %s,
                        daily_fat = %s,
                        daily_over = %s,
                        daily_coach = %s,
                        daily_df = %s
                    WHERE user = %s AND daily_date = %s
                """
                cursor.execute(sql_update, (
                    count_res_dict['基础代谢'],
                    count_res_dict['体重'],
                    count_res_dict['进食顿数'],
                    count_res_dict['摄入卡路里'],
                    count_res_dict['碳水'],
                    count_res_dict['蛋白质'],
                    count_res_dict['脂肪'],
                    int(count_res_dict['是否超标']),
                    healthy_res,
                    count_res_dict['膳食纤维'],
                    user,
                    date
                ))
            else:
                # 插入新记录
                sql_insert = """
                    INSERT INTO daily (
                        daily_id, daily_date, daily_TDEE, daily_weight,
                        daily_count, daily_cal, daily_carbon, daily_protein,
                        daily_fat, daily_over, daily_coach, user, daily_df
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                cursor.execute(sql_insert, (
                    daily_id,
                    date,
                    count_res_dict['基础代谢'],
                    count_res_dict['体重'],
                    count_res_dict['进食顿数'],
                    count_res_dict['摄入卡路里'],
                    count_res_dict['碳水'],
                    count_res_dict['蛋白质'],
                    count_res_dict['脂肪'],
                    int(count_res_dict['是否超标']),
                    healthy_res,
                    user,
                    count_res_dict['膳食纤维']
                ))
            
            connect.commit()
        except Exception as e:
            print(f"更新daily表失败: {str(e)}")
            connect.rollback()
        except Exception as e:
            print(f"更新daily表失败: {str(e)}")
            connect.rollback()
            raise e
        finally:
            if cursor:
                cursor.close()
            if connect and connect.open:
                connect.close()
        
        return 
        
    except Exception as e:
        print(f"查询今日数据失败: {str(e)}")
        return []
    finally:
        cursor.close()
    
