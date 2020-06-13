import tempfile, threading, win32api, win32con, os, win32file
import re

# DIRETORIO DE ESCUTA
dirs_to_monitor = ["C:\\WINDOWS\\Temp", tempfile.gettempdir()]
print(dirs_to_monitor)

# ATRIBUTOS
FILE_CREATED = 1
FILE_DELETED = 2
FILE_MODIFIED = 3
FILE_RENAMED_FROM = 4
FILE_RENAMED_TO = 5

def start_monitor(path_to_watch):
    FILE_LIST_DIRECTORY = 0x0001
    h_directory = win32file.CreateFile(path_to_watch, FILE_LIST_DIRECTORY, 
    win32con.FILE_SHARE_READ | win32con.FILE_SHARE_WRITE | win32con.FILE_SHARE_DELETE,
        None, win32con.OPEN_EXISTING, win32con.FILE_FLAG_BACKUP_SEMANTICS, None)
    while True:
        try:
            results = win32file.ReadDirectoryChangesW(h_directory, 1024, True,
            win32con.FILE_NOTIFY_CHANGE_FILE_NAME | win32con.FILE_NOTIFY_CHANGE_DIR_NAME |
            win32con.FILE_NOTIFY_CHANGE_ATTRIBUTES | win32con.FILE_NOTIFY_CHANGE_SIZE |
            win32con.FILE_NOTIFY_CHANGE_LAST_WRITE | win32con.FILE_NOTIFY_CHANGE_SECURITY,
            None, None)
            for action,file_name in results:
                full_filename = os.path.join(path_to_watch, file_name)
                if action == FILE_CREATED: print(f"[ + ] Criando {full_filename}")
                elif(action == FILE_DELETED): print(f"[ - ] Deletando {full_filename}")
                elif(action == FILE_MODIFIED): 
                    print(f"[ * ] Modificando {full_filename}")
                    # exi(e o conteúdo do arquivo)
                    print("[vvv] Dumping conteudo...")
                    try:
                        exs = '.bat|.vbs|.ps'
                        if(re.search(exs, full_filename)):
                            with open(full_filename,"rb") as arq: contents = arq.read()
                            print(contents)
                            print("[^^^] Dump completo.")
                    except Exception as erro: print(f"[!!!] Falha. {erro}")
                elif(action == FILE_RENAMED_FROM): print( f"[ > ] Renomeando de: {full_filename}" )
                elif action == FILE_RENAMED_TO: print(f"[ < ] Renomeando para: {full_filename}")
                else: print(f"[???] Não Encontrado: {full_filename}")
        except Exception as erro: pass

def injectar_codigo(full_filename,extension,contents):
    file_types = {}
    if(file_types[extension][0] in contents): ...

for path in dirs_to_monitor:
    try:
        monitor_thread = threading.Thread(target=start_monitor,args=(path,))
        print(f"Spawning monitoring thread for path: {path}")
        monitor_thread.start()
    except Exception as erro: print(f"ERRO EM MONITORAR {path} -- {erro}")            