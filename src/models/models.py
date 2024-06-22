from pydantic import BaseModel,Field
from typing import Union,Optional


class InsertVacancies(BaseModel):
    title:str
    description:str
    company_id:int
    category_id:int   
    address:str
    request: str
    salary:float
    type_employment:Union[str,None] = None

class UpdateVacancy(BaseModel):
    vacancy_id:int
    title:str
    desc:str
    company_id:int
    category_id:int
    address:int
    request:str
    salary:float
    type_employment:str



class InsertProfession(BaseModel):
    prof_name:str 

class InsertCompany(BaseModel):
    comp_name:str
    comp_email:str 

class UpdateCompany(BaseModel):
    comp_id:int
    comp_name:Union[str,None]=None
    comp_email:Union[str,None]=None


class InsertCategory(BaseModel):
    category_name:str
    parent_category:Union[int,None] = None

class DeleteCategory(BaseModel):
    category_id:int
    parent_category_id:Union[int,None]=None

class UpdateCategory(BaseModel):
    category_id:int
    category_name:str
    parent_category_id:Union[int,None]=None

class UpdateProfession(BaseModel):
    prof_id:int
    prof_name:str



class InsertSkills(BaseModel):
    skills:str
    profession_id:int

class UpdateSkills(BaseModel):
    id:Union[int,None] = None
    skills:str
    profession_id:Union[int,None] = None

class InsertCv(BaseModel):
    prof_id:int
    about_user:str
    skills_id:int
    experience:str 


class UsersRegistration (BaseModel):
    first_name:str
    last_name:str
    gender:str
    phone_number:str
    user_password:str

class LoginUser(BaseModel):
    phone_number:str
    password:str

class FilterVacancy(BaseModel):
    company_name:Union[str,None]=None
    category_name:Union[str,None]=None
    address:Union[str,None]=None
    salary:Union[float,None]=None
    type_employment:Union[str,None]=None


class LoginModel(BaseModel):
    phone_number: str = Field(..., max_length=20)
    password: str = Field(..., max_length=20)

class RegistrationModel(BaseModel):
    first_name: str = Field(..., max_length=20)
    last_name: str = Field(..., max_length=20)
    gender: str = Field(..., max_length=20)
    phone_number:str = Field(..., max_length=20)
    password: str = Field(..., max_length=20)

class DeviceTokenModel(BaseModel):
    dtoken: str
