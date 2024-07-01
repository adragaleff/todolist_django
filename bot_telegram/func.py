import simplemysql, settings

db = simplemysql.Pymysql(host=settings.host,user=settings.user, password=settings.password,db=settings.db,port=3306)


async def check_user(user_id):
    result = db.request(f"SELECT * FROM `users` WHERE user_id = '{user_id}'", 'fetchone')
    token = result['token']
    war_token = result['war_token']
    if war_token == '0':
        return False
    else:
        return True