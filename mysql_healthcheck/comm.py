mytrace = False

# internal function to execute SQL in the current session and return RESULTSET
def __runAndReturn(session, sqltext=None) :
    stmt = ""
    if sqltext is not None:
        stmt = sqltext;
        stmt = stmt + ";"

    # Execute the query and check for warnings
    result = session.run_sql(stmt)
    if (result.get_warnings_count() > 0):
        # Bail out and print the warnings
        print("Warnings occurred - bailing out:")
        print(result.get_warnings())
        return False

    return result;


def __getHeatWaveStatus(session=None):

    import mysqlsh
    shell = mysqlsh.globals.shell

    if session is None:
        session = shell.get_session()
        if session is None:
            print("No session specified. Either pass a session object to this "
                  "function or connect the shell to a database")
            return

    result = session.run_sql("""
        select 
            max(    case variable_name    when 'rapid_service_status' then variable_value    else ''    end ) as rapid_service_status, 
            max(    case variable_name    when 'rapid_cluster_status' then variable_value    else ''    end ) as rapid_cluster_status,
            max(    case variable_name    when 'rapid_plugin_bootstrapped' then variable_value    else ''    end ) as rapid_plugin_bootstrapped
        from performance_schema.global_status where variable_name like 'rapid%'
    """ )

    if (result.get_warnings_count() > 0):
        # Bail out and print the warnings
        print("Warnings occurred - bailing out:")
        print(result.get_warnings())
        return False


    rows = result.fetch_all()
    return rows

def __isHeatWaveOnline(session=None):

    rows = __getHeatWaveStatus(session)
    if len(rows) > 0 and rows[0][0] == "ONLINE":
        return True

    print("Heatwave is OFFLINE")
    return False

def __isHeatWavePlugin(session=None):

    rows = __getHeatWaveStatus(session)
    
    if len(rows) > 0 :
        if rows[0][2] == "NO":
            print("Heatwave Plugin not installed")
            return False
        else:
            return True

    return False

def __printSection(mytext=None):
    if mytext is None:
        return

    print("")
    print("")

    print("*" * 80)
    print("*" * 80)
    
    print("***" + "   " + mytext + " " * (80 - len(mytext) - 12) + "   ***")
    
    print("*" * 80)
    print("*" * 80)
    return

def __listVariables(variablePattern=None, session=None):

    import mysqlsh
    shell = mysqlsh.globals.shell

    if session is None:
        session = shell.get_session()
        if session is None:
            print("No session specified. Either pass a session object to this "
                  "function or connect the shell to a database")
            return

    if variablePattern is None:
        variablePattern="%"
    else:
        variablePattern="%" + variablePattern + "%"

    result = session.run_sql("""
        select * from performance_schema.variables_info where variable_name like '%s';
    """ % variablePattern)

    if (result.get_warnings_count() > 0):
        # Bail out and print the warnings
        print("Warnings occurred - bailing out:")
        print(result.get_warnings())
        return False
    
    import mysqlsh
    shell = mysqlsh.globals.shell
    rows = shell.dump_rows(result)
    if rows > 0 :
        return True
    else:
        return False


