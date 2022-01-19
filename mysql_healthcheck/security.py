from mysqlsh.plugin_manager import plugin, plugin_function
from mysql_healthcheck.comm import __runAndReturn

def __isKeyringOn(myprint=True, session=None) :
    import mysqlsh
    shell = mysqlsh.globals.shell

    if session is None:
        session = shell.get_session()
        if session is None:
            print("No session specified. Either pass a session object to this "
                  "function or connect the shell to a database")
            return

    result = session.run_sql("""
        select * from information_schema.plugins where plugin_name like 'keyring%';
    """)

    if (result.get_warnings_count() > 0):
        # Bail out and print the warnings
        print("Warnings occurred - bailing out:")
        print(result.get_warnings())
        return False
    
    import mysqlsh
    shell = mysqlsh.globals.shell
    if myprint:
        rows = shell.dump_rows(result)
        if rows > 0:
            return True
        else:
            return False
    else:
        rows = shell.fetch_all()
        if len(rows) > 0:
            return True
        else:
            return False

def __listEncryptedTables(session=None) :
    import mysqlsh
    shell = mysqlsh.globals.shell

    if session is None:
        session = shell.get_session()
        if session is None:
            print("No session specified. Either pass a session object to this "
                  "function or connect the shell to a database")
            return

    result = session.run_sql("""
        SELECT TABLE_SCHEMA, TABLE_NAME, CREATE_OPTIONS FROM INFORMATION_SCHEMA.TABLES WHERE CREATE_OPTIONS like '%ENCRYPTION=%Y%';
    """)

    if (result.get_warnings_count() > 0):
        # Bail out and print the warnings
        print("Warnings occurred - bailing out:")
        print(result.get_warnings())
        return False
    
    import mysqlsh
    shell = mysqlsh.globals.shell

    rows = shell.dump_rows(result)
    if rows > 0:
        return True
    else:
        return False
    


def __isAuditOn(myprint=True, session=None):

    import mysqlsh
    shell = mysqlsh.globals.shell

    if session is None:
        session = shell.get_session()
        if session is None:
            print("No session specified. Either pass a session object to this "
                  "function or connect the shell to a database")
            return

    result = session.run_sql("""
        select * from information_schema.plugins where plugin_name = 'audit_log';
    """)

    if (result.get_warnings_count() > 0):
        # Bail out and print the warnings
        print("Warnings occurred - bailing out:")
        print(result.get_warnings())
        return False
    
    import mysqlsh
    shell = mysqlsh.globals.shell

    if myprint :
        rows = shell.dump_rows(result)
        if rows > 0:
            return True
        else:
            return False
    else:
        rows = shell.fetch_all()
        if len(rows) > 0:
            return True
        else:
            return False

def __isFirewallOn(myprint=True, session=None):

    import mysqlsh
    shell = mysqlsh.globals.shell

    if session is None:
        session = shell.get_session()
        if session is None:
            print("No session specified. Either pass a session object to this "
                  "function or connect the shell to a database")
            return

    result = session.run_sql("""
        select * from information_schema.plugins where plugin_name like '%firewall';
    """)

    if (result.get_warnings_count() > 0):
        # Bail out and print the warnings
        print("Warnings occurred - bailing out:")
        print(result.get_warnings())
        return False
    
    import mysqlsh
    shell = mysqlsh.globals.shell


    if myprint :
        rows = shell.dump_rows(result)
        if rows > 0:
            return True
        else:
            return False
    else:
        rows = shell.fetch_all()
        if len(rows) > 0:
            return True
        else:
            return False

