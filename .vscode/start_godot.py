import sys, subprocess,time, socket, debugpy,os
print("start godot")
if(os.path.exists("locked_debug")):
    os.remove("locked_debug")
res = subprocess.Popen('"C:/Users/nikla/Downloads/Godot_v3.5.1-stable_win64.exe(1)/Godot_v3.5.1-stable_win64.exe" --path C:/Users/nikla/OneDrive/Dokumente/repositories/py4godot---Open-Project',
                        shell=True, creationflags=subprocess.CREATE_NEW_PROCESS_GROUP|subprocess.DETACHED_PROCESS)

while True:
    time.sleep(0.1)
    print(os.getcwd())
    if(os.path.exists("locked_debug")):
        os.remove("locked_debug")
        break
sys.exit(0)
