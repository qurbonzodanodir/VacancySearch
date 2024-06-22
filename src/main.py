from fastapi import FastAPI,HTTPException
from fastapi.middleware.cors import CORSMiddleware
from src.models.models import InsertVacancies,InsertProfession,InsertCompany,UpdateCompany,InsertCategory,DeleteCategory,UpdateCategory,UpdateProfession,UpdateVacancy,InsertSkills,UpdateSkills,InsertCv,UsersRegistration,LoginUser,FilterVacancy

# from elasticsearch import Elasticsearch

from lib.connection import connection
from src.models import models
from fastapi import APIRouter,Depends
from src.modules import authorization
import lib.acl as ACL
import random
from psycopg2 import sql
app = FastAPI()

# Correct way to add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:3000'],  # Allow React app to connect
    allow_credentials=True,
    allow_methods=['GET', 'POST'],
    allow_headers=['*']
)

# @app.get('/category/all')
# def get_all_categories():
#     result = None
#     with get_cursor() as cur:
#         # method callproc calling func
#         cur.callproc('products.get_all_categories')
#         result = cur.fetchone()

#     return result

@app.get('/hello')
def say_hello(x: int, y, z):
    names = ['muhammad', 'umar', 'nodir', 'ismoil']
    random_name = random.choice(names)
    return {
        'data': x,
        'msg': f"Hello {random_name}"
    }


@app.get('/vacancies/all')
def get_all_vacancies():
    result = None 
    with connection() as cur:
        cur.callproc('vacancy.get_all_vacanies')
        result = cur.fetchone()[0]

    return result   

@app.get('/company/all')
def get_all_company():
    result = None 
    with connection() as cur:
        cur.callproc('vacancy.selections')
        result = cur.fetchone()[0]

    return result  



@app.get('/selections')
def selections():
    result = None 
    with connection() as cur:
        cur.callproc('vacancy.selections')
        result = cur.fetchone()[0]

    return result    


# --------------------------------------------------------------

@app.post('/insert/profession')
def InsertProfession(data:InsertProfession):
    try:
        with connection() as cur:
            cur.execute('call vacancy.insert_profession(%s)',(data.prof_name,))
            return 'OK'
    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e))    
    

@app.put('/update/profession')   
def UpdateProfession(data:UpdateProfession):
    try:
        with connection() as cur:
            cur.execute('call vacancy.update_profession(%s,%s)',(data.prof_id,data.prof_name,))
            return 'Ok'
    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e))

# ---------------------------------------------------------------------------------

    
@app.post('/insert/company')   
def InsertCompany(data:InsertCompany):
    try:
        with connection() as cur:
            cur.execute('call vacancy.insert_company(%s,%s)',(data.comp_name,data.comp_email))
            return 'Ok'
    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e)) 


@app.put('/update/company')   
def UpdateCompany(data:UpdateCompany):
    try:
        with connection() as cur:
            cur.execute('call vacancy.update_company(%s,%s,%s)',(data.comp_id,data.comp_name,data.comp_email,))
            return 'Ok'
    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e))   
    

# ---------------------------------------------------------------------------------------------------------------    
    
@app.post('/insert/category') 
def InsertCategory(data:InsertCategory):
    try:
        with connection() as cur:
            cur.execute('call const.insert_category(%s,%s)',(data.category_name,data.parent_category,))
            return"Ok"
    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e))  


@app.put('/update/category')   
def UpdateCategory(data:UpdateCategory):
    try:
        with connection() as cur:
            cur.execute('call const.update_category(%s,%s,%s)',(data.category_id,data.category_name,data.parent_category_id,))
            return 'Ok'
    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e))    


@app.delete('/delete/categoty')
def DeleteCategory(data: DeleteCategory ):
    try:
        with connection() as cur:
            cur.execute("Call const.delete_category (%s,%s)",(data.category_id,data.parent_category_id)) 
            return "OK"
    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e))      


# ---------------------------------------------------------------------------------------------------------------    



@app.post('/insert/vacancy')
def InsertVacancies(data: InsertVacancies ):
    try:
        with connection() as cur:
            cur.execute("CALL vacancy.insert_vacancy(%s,%s,%s,%s,%s,%s,%s,%s)", (data.title,data.description,data.company_id,data.category_id,data.address,data.request,data.salary,data.type_employment))
            return "OK"
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 


@app.put('/update/vacancy')   
def UpdateVacancy(data:UpdateVacancy):
    try:
        with connection() as cur:
            cur.execute('call vacancy.update_vacancy(%s,%s,%s,%s,%s,%s,%s,%s,%s)',(data.vacancy_id,data.title,data.desc,data.company_id,data.category_id,data.address,data.request,data.salary,data.type_employment,))
            return 'Ok'
    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e))       
                



# ---------------------------------------------------------------------------------------------------------------    

@app.post('/insert/skills')
def InsertSkills(data:InsertSkills):
    try:
        with connection() as cur:
            cur.execute('call vacancy_user.insert_skills(%s,%s)',(data.skills,data.profession_id,))
            return 'Ok'
    except Exception as e:
        raise HTTPException(status_code=500,detail = str(e))    
    

@app.put('/update/skills')   
def UpdateSkills(data:UpdateSkills):
    try:
        with connection() as cur:
            cur.execute('call vacancy_user.update_skills(%s,%s,%s)',(data.id,data.skills,data.profession_id,))
            return 'Ok'
    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e))




# ---------------------------------------------------------------------------------------------------------------    

@app.post('/insert/cv')   
def InsertCv(data:InsertCv):
    try:
        with connection() as cur:
            cur.execute('call vacancy_user.insert_cv(%s,%s,%s,%s)',(data.prof_id,data.about_user,data.skills_id,data.experience,))
            return 'Ok'
    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e)) 


# ---------------------------------------------------------------------------------------------------------------    


@app.post('/registration')
async def registration(data: models.RegistrationModel):
    return await authorization.registration(data)


@app.post('/login')
async def login(data: models.LoginModel):
    return await authorization.login(data)


# @app.post('/registration')   
# def UsersRegistration(data:UsersRegistration):
#     try:
#         with connection() as cur:
#             cur.execute('call vacancy_user.insert_user(%s,%s,%s,%s,%s)',(data.first_name,data.last_name,data.gender,data.phone_number,data.user_password,))
#             return 'Ok'
#     except Exception as e:
#         raise HTTPException(status_code=500,detail=str(e)) 
    

    
    


@app.post('/vacancy/filter/')
def filter_vacancy(data: FilterVacancy):
    try:
        with connection() as conn:
             with conn as cur:
                cur.execute('select vacancy.filter_vacancy(%s, %s, %s, %s, %s)',
                       (data.company_name,
                        data.category_name,
                        data.address,  
                        data.salary, 
                        data.type_employment
                        ))
                results = cur.fetchall()[0][0]
             
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

