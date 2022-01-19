from mysqlsh.plugin_manager import plugin, plugin_function
from mysql_healthcheck.comm import __runAndReturn


def __isThreadPoolOn(myprint=True, session=None):

    import mysqlsh
    shell = mysqlsh.globals.shell

    if session is None:
        session = shell.get_session()
        if session is None:
            print("No session specified. Either pass a session object to this "
                  "function or connect the shell to a database")
            return

    result = session.run_sql("""
        select * from information_schema.plugins where plugin_name like 'thread_pool%';
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


