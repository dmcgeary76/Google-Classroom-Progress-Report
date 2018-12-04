from configparser import SafeConfigParser

# Retrieve some config values from a config file
def get_config_vals():
    config = SafeConfigParser()
    config.read(<pathway to config file>)
    mysql_pwd = config.get('MYSQL', 'password')
    mysql_user = config.get('MYSQL', 'username')
    student_db = config.get('MYSQL', 'student_db')

    return [mysql_pwd, mysql_user, student_db]
