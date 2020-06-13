import win32con, win32api, win32security
import wmi, sys, os

def get_process_privileges(pid):
    try: 
        hproc = win32api.OpenProcess(win32con.PROCESS_QUERY_INFORMATION,False,pid)
        htok = win32security.OpenProcessToken(hproc,win32con.TOKEN_QUERY)
        privs = win32security.GetTokenInformation(htok, win32security.TokenPrivileges)
        priv_list = ""
        for i in privs:
            if i[1] == 3: priv_list += "%s|" % win32security.LookupPrivilegeName(None,i[0])
        return priv_list
    except: pass

def log_to_file(message):
    with open("process_monitor_log.csv", "a") as arq:
        arq.write(f"{message}")
    return

#CRIA INTERFACE
c = wmi.WMI()

#CRIA MONITOR PROCESSOS
processo_monitor = c.Win32_Process.watch_for("creation")

while True:
    try:
        new_process = processo_monitor()
        proc_owner = new_process.GetOwner()
        proc_owner = "{}\\{}".format(proc_owner[0], proc_owner[2])
        create_date = new_process.CreationDate
        executable = new_process.ExecutablePath
        cmdline = new_process.CommandLine
        pid = new_process.ProcessId
        parent_pid = new_process.ParentProcessId
        privileges = "N/A"
        process_log_message = "{},{},{},{},{},{},{}\r\n" .format(create_date, 
                proc_owner, executable, cmdline, pid, parent_pid, privileges)
        print(process_log_message)
        print(f"PRIVILEGIOS: {get_process_privileges(pid)}")
        log_to_file(process_log_message)
    except Exception as erro: print(f"ERRO ENCONTRADO {erro}")