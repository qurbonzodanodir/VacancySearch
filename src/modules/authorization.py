from lib.connection import connection
from src.models import models
import lib.acl as ACL

async def login(user: models.LoginModel):
    result = None
    with connection() as cur:
        cur.execute('call vacancy_user.user_authentication(%s, %s, %s, %s)', (user.phone_number, user.password, '{}','{}'))
        result = cur.fetchone()[0]
        print(result)
        if result['_status_code'] == 0:
            result['access_token'] = ACL.access_token(user.username, result['user_id'])
            # set in cookie
            result['refresh_token'] = ACL.refresh_token(user.username, result['user_id'])
    return result


async def registration(data: models.RegistrationModel):
    result = None
    with connection() as cur:
        cur.execute('call vacancy_user.insert_user(%s,%s,%s,%s,%s)',
                    (data.first_name,data.last_name,data.gender,data.phone_number,data.user_password, '{}'))
        result = cur.fetchone()[0]
    return result



async def save_device(data: models.DeviceTokenModel, payload):
    result = None
    with connection() as cur:
        cur.execute('call account.save_device_token(%s, %s, %s)', 
                    (payload['user_id'], data.dtoken, '{}'))
        result = cur.fetchone()[0]
    return result

async def logout(payload):
    # TODO: delete device token
    pass
