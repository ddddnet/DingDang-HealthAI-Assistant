from pydantic import BaseModel
    
class Login(BaseModel):
    user: str
    password: str
    systemInfo: str
    
class ResetPassword(BaseModel):
    user: str
    password: str
    
class UserInfo(BaseModel):
    user: str
    name: str
    gender: str
    age: int
    height: float
    weight: float
    activityLevel: int
    systemInfo: str
    
class GetUserInfo(BaseModel):
    user: str
    systemInfo: str
    code: str
    
class UploadSet(BaseModel):
    user: str
    systemInfo: str

class Ai_analysis_food(BaseModel):
    user: str
    systemInfo: str
    data: str
    
class AiScarne(BaseModel):
    user: str
    systemInfo: str
    data: str

class GetDaily(BaseModel):
    user: str
    date: str
    systemInfo: str

class GetLastMealTime(BaseModel):
    user: str
    systemInfo: str
