import re
def validate_phone(phone):
    """
    校验手机号码格式是否正确
    """
    pattern = r'^1[3-9]\d{9}$'
    if re.match(pattern, phone):
        return True
    return False


def validate_password(password):
    """
    校验密码格式是否满足要求，仅限于数字、大小写字母、常用特殊符号，且长度大于等于6位
    常用特殊符号这里简单定义为:!@#$%^&*()-_=+[]{}|;':",./<>?
    """
    pattern = r'^[a-zA-Z0-9!@#$%^&*()\-_=+[\]{}|;\':",./<>?]{6,}$'
    if re.match(pattern, password):
        return True
    return False

