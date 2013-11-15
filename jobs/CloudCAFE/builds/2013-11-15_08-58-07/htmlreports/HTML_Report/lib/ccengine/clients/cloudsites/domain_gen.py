import time

#===============================================================================
# fqdn 
# db_name
# db_password
# db_user
#===============================================================================
class data_gen(object):

    def __init__(self):
        pass
                    
    def gen_date(self):
        ext_raw = time.time()
        ext_str = str(ext_raw)
        ext_split = ext_str.split('.', 1)[0]
        ext = ext_split[-6:]
        user_ext = ext_split[-6: -2]
        fqdn = 'www.ryanpysite'+ext+'.com'
        db_name = 'qepy'+ext
        db_password = 'Password!'
        db_user = 'qepy'+user_ext
        return fqdn, db_name, db_password, db_user
