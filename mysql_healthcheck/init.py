from mysqlsh.plugin_manager import plugin, plugin_function
from mysql_healthcheck.comm import __runAndReturn, __isHeatWaveOnline, __isHeatWavePlugin, __listVariables, __printSection
from mysql_healthcheck.security import __isKeyringOn, __listEncryptedTables, __isAuditOn, __isFirewallOn
from mysql_healthcheck.threadpool import __isThreadPoolOn
from mysql_healthcheck import comm
from support.fetch import get_fetch_info
from check.schema import get_innodb_with_nopk
from check.trx import show_binlogs_io, show_binlogs, show_trx_size
from group_replication.gr import status

@plugin
class mysql_healthcheck:
    """
    health check Utils ...

    A collection of utils to do health check on MySQL 
    """


def __getUserDatabaseTableSize(session):

    stmt = """ SELECT table_schema "DB Name", ROUND(SUM(data_length + index_length) / 1024 / 1024, 1) "DB Size in MB" 
    FROM information_schema.tables  
    where table_type =  'BASE TABLE' 
    GROUP BY table_schema;
    """

    result = __runAndReturn(session, stmt)
    return result

# internal function to Load call sys.diagnostics(....) 
def __runDiagnostics(session):
   
    
    stmt = "call sys.diagnostics(20, 20, 'current')"
    stmt = stmt + ";"


    # Execute the query and check for warnings
    result = __runAndReturn(session, stmt)

    return result

def __printResult(rs):
    import mysqlsh
    shell = mysqlsh.globals.shell
    shell.dump_rows(rs)
    return
    


@plugin_function("mysql_healthcheck.run")
def run( session=None):
    """
    Wizard to run HealthCheck 

    Args:
        session (object): The optional session object

    """
    # Get hold of the global shell object
    import mysqlsh
    shell = mysqlsh.globals.shell

    if session is None:
        session = shell.get_session()
        if session is None:
            print("No session specified. Either pass a session object to this "
                  "function or connect the shell to a database")
            return

    __printSection("sys.diagnostics Report")
    print(__printResult(__runDiagnostics(session)))
    print("Database Size")
    print(__printResult(__getUserDatabaseTableSize(session)))

    __printSection("Support.fetchInfo()")
    get_fetch_info(True, False, True, False, session)

    __printSection("check.getInnoDBTablesWithNoPK")
    get_innodb_with_nopk(session)

    __printSection("check.showbinlogsIO / showTrxSize")
    show_binlogs_io(session)
    
    show_trx_size(None, session)

    __printSection("Group Replication")
    status(session)

    __printSection("Audit Log")
    if __isAuditOn(True, session):
         print("Audit Plugin is installed") 
         __listVariables('audit',session)   
    else:   
        print("Audit Plugin is not installed")


    __printSection("Enterprise Firewall")
    if __isFirewallOn(True, session):
         print("Enterprise Firewall Plugin is installed")   
         __listVariables('firewall', session)
    else:   
        print("Enterprise Firewall Plugin is not installed")


    __printSection("Transparent Data Encryption")
    if __isKeyringOn(True, session):
        print("TDE keyring is ON")
        __listEncryptedTables(session)
    else:
        print("TDE keyring is not installed")

    __printSection("Thread Pool")
    if __isThreadPoolOn(True, session):
        print("Thread Pool is installed")
        __listVariables('thread_pool', session)
    else:
        print("Thread Pool is notinstalled")

    
    return

