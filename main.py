#!sudo python
par_di1=__file__.split('/')[1:][:-1]
par_dir='/'
for dir1 in par_di1:
    par_dir=f'{par_dir}{dir1}/'
print(par_dir)
with open(f'{par_dir}error.log', 'w')as err_f:
        err_f.write('')
#libs
import traceback
import os
import sys
import json
import socket
import subprocess
from threading import Thread
import time
from time import sleep as delay
from datetime import datetime
import re
import threading
from better_profanity import profanity
from PIL import ImageColor
from cryptography.fernet import Fernet
import yaml
from zipfile import ZipFile
import pygetwindow as gw
from getpass import getpass


#initialize
try:
    def color(fg, bg=False):
        r, g, b=ImageColor.getcolor(str(fg), 'RGB')
        return '\033[{};2;{};{};{}m'.format(48 if bg else 38, r, g, b)
    class log:
        def info(txt):
            print(f"{color('#21c500')}[INFO] {color('#fff')}{txt}")
        def warn(txt):
            print(f"{color('#b5cd00ff')}[WARN] {color('#fff')}{txt}")
        def error(txt):
            print(f"{color('#cb0000')}[ERROR] {color('#fff')}{txt}")
        def xy(x, y, text):
            sys.stdout.write("\x1b7\x1b[%d;%df%s\x1b8" % (x, y, text))
            sys.stdout.flush()
    
    log.info('Loading encryption key')
    with ZipFile(f'{par_dir}x64a.upf')as f:
        dll_key=f.read('dll.key')
        appdata=json.loads(f.read('data.json'))
    dll=Fernet(dll_key)

    dll_list = []
    for dll_file in os.listdir(par_dir):
        if dll_file.endswith('.dll'):
            dll_list.append(dll_file)
    
    for dll_file in dll_list:
        log.info(f'Loading {dll_file}')
        with open(f'{par_dir}{dll_file}')as dllf:
            dll_code=dllf.read()
        dll_output=''
        for c in dll_code.split('\n'):
            if not c=='':
                dll_output=f'{dll_output}{dll.decrypt(c.encode()).decode()}\n'
        delay(1)
        exec(dll_output)
    
    log.info('Opening words.json')
    with open(f"{par_dir}words.json")as f:
        bad_words=json.load(f)
    
    class cli:
        def quit():
            try:
                os.system('clear')
                quit()
            except:
                False
    def res_color():
        return '\033[0m'
    
    #create a key listener
    kk=''
    is_released=False
    def getkey():
        return str(str(os.popen(f'node {par_dir}getkey.js').read()).lower()).replace('\n', '')

    last_menu=''
    srv_list = []
    for srv_file in os.listdir(f'{par_dir}servers'):
        if srv_file.endswith('.json'):
            srv_list.append(srv_file.replace('.json', ''))
    
    theme_list=os.listdir(f"{par_dir}themes")
 

    with open(f'{par_dir}config.yml', 'rb')as ff:
        configs=yaml.load(ff, Loader=yaml.FullLoader)
    with open(f'{par_dir}config.yml', 'rb')as ff:
        nconfigs=yaml.load(ff, Loader=yaml.FullLoader)
    config_list=[]
    for x in configs:
        config_list.append(x)
    config_dsp=[]
    for x in configs:
        config_dsp.append(f'{x}: {configs[x]}')
    
    with open(f"{par_dir}themes/{str(configs['theme']).split('.')[0]}/{str(configs['theme']).split('.')[-1]}.json")as theme_file:
        theme = json.load(theme_file)
except Exception as e:
    with open(f'{par_dir}error.log', 'w')as err_f:
        print(traceback.format_exc())
        err_f.write(str(traceback.format_exc()))
    quit()

try:
    #create menu modifier
    def menu(items, title=False, cursor_index=0, hotkeys={4: lambda: quit()}, clear_onkey=True):
        cursor=theme['cursor']
        x=cursor_index+1
        items_c=len(items)
        y=1
        if not title==False:
            items_c+=1
            y=2
            x+=1
        while True:
            while True:
                os.system('clear')
                if not title==False:
                     print(f"{color(theme['menu-fg'])}{title}")
                for item in items:
                     print(f"{' '*len(cursor)}{item}")
                if items==[]:
                    log.xy(y, 1, f"{'' if theme['cursor-bg'].lower()=='false' else color(theme['cursor-bg'], bg=True)}{color(theme['cursor-fg'])}{cursor}")
                else:
                    log.xy(x, 1, f"{'' if theme['cursor-bg'].lower()=='false' else color(theme['cursor-bg'], bg=True)}{color(theme['cursor-fg'])}{cursor}{'' if str(theme['menu-highlight']).lower()=='false' else color(theme['menu-highlight'], bg=True)}{color(theme['menu-hfg'])}{items[x-2]}")
                # delay(.1)
                key=getkey()
                if key=='return':
                    return x-y
                    break
                elif key=='escape':
                    os.system('clear')
                    return None
                if key=='up':
                    if not x==y:
                        x-=1
                    else:
                        x=items_c
                elif key=='down':
                    if not x==items_c:
                        x+=1
                    else:
                          x=y
                else:
                    for i in hotkeys.keys():
                        if str(key)==str(i):
                            if clear_onkey:
                                os.system('clear')
                            hotkeys[i]()

    #the direct tools
    tools_list=os.listdir(f'{par_dir}tools')
    def open_direct_tool(direct_tool_name):
        with open(f"{par_dir}tools/{direct_tool_name}")as dtf:
            dts = dtf.read()
        
        if str(direct_tool_name).endswith('.py'):
            exec(dts)
        elif str(direct_tool_name).endswith('.dll'):
            exec(dll.decrypt(dts.encode()))
        elif str(direct_tool_name).endswith('.sh'):
            os.system(dts)
        elif str(direct_tool_name).endswith('.bat'):
            os.system(dts)
        delay(1)
        os.system('clear')
        direct_tools()

    def direct_tools():
        x=menu(tools_list, 'Execute a direct tool')
        if x==None:
            menu_root()
        else:
            open_direct_tool(tools_list[int(x)])
    
    def add_direct_tool():
        False

    #client server join
    def join_srv(nm, addr, port ,sud):
        class msg:
            def out(msg):
                print(msg)
            def send(smsg):
                print()
        def connect():
            global s
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((host,port))
            s.send({"token": "", "version": 2.1}.encode())
            delay(.7)
            s.send(uname.encode())
            print(f"{color(theme['self-color'])}[CLIENT] {theme['fg']}connected")
            new_data = s.recv(1024).decode()
            print(f"{color(theme['srv-color'])}[{new_data['from']}]{new_data['to']}")
            for cx0 in range(len(module_l)):
                exec(module_l[cx0].split("':::'")[3])
        connect()
        clientRunning = True
        def echo_data(sock):
           serverDown = False
           lio = False
           while clientRunning and (not serverDown):
              try:
                data = sock.recv(1024).decode()
                if filter_cuss == 'true':
                    data['msg'] = profanity.censor(data['msg'])
                    data['from'] = profanity.censor(data['from'])
                    data['to'] = profanity.censor(data['to'])

                if data['type']=='cmd-out':
                    exec(data['msg'])
                else:
                    print(f"{data['from']} {data['msg']}")
                            
              except Exception as e:
                print(f'[CLIENT] You are Disconnected. Quitting to main menu... [ERRCODE] {e}')
                serverDown = True
                delay(1)
                menu1()
        threading.Thread(target=echo_data, args = (s,)).start()
        while clientRunning:
            try:
                msg=input()
                if len(msg) == 0:
                    data = {"from": nm, "to": "#all", "msg": msg, "type": "msg"}
                    s.send(data.encode())
                else:
                    if msg[0] == '?':
                        if msg == '?q':
                            menu1()
                        elif msg == '?r':
                            s.close()
                            connect()
                        elif msg == '?info':
                            print(f"name: {sud['name']}\nip: {sud['address']}\nport: {sud['port']}\ndescription: {sud['description']}")
                    else:
                        if msg[0]=='@':
                            data = {"from": nm, "to": msg.split(' ')[0], "msg": msg, "type": "whisper"}
                        data = {"from": nm, "to": "#all", "msg": msg, "type": "msg"}
                        if msg[0]=='/':
                            {"from": nm, "to": "#srv", "msg": msg, "type": "cmd"}
                        s.send(data.encode())
            except Exception as e:
                print(e)
        s.close()

    def quickjoin(srv_name):
        with open(f'{par_dir}servers/{srv_name}.json', 'rb')as f:
            srv_json=json.load(f)
        join_srv(name, srv_json['address'], srv_json['port'], srv_json)

    themex=0
    #menus
    def sel_theme():
        global x
        global theme
        global themex
        if themex==None:
            themex=0
        if not configs['sticky-select']:
            themex=0
        themex=menu(theme_list, 'Choose a theme', cursor_index=themex)
        if themex==None:
            menu_root()
        elif not themex==None:
            with open(f'{par_dir}themes/{theme_list[themex]}/theme.yml')as thm_f:
                themedesc=dict(yaml.load(thm_f, Loader=yaml.FullLoader))
            theme_dir_list=os.listdir(f'{par_dir}themes/{theme_list[themex]}')
            theme_dir_list.remove('theme.yml')
            x=menu(theme_dir_list, f"[{themedesc['name']}] {themedesc['description']}")
            if x==None:
                sel_theme()
            else:
                with open(f'{par_dir}themes/{theme_list[themex]}/{theme_dir_list[x]}')as thf:
                    theme=json.load(thf)
                configs['theme']=f"{theme_list[themex]}.{theme_dir_list[x].split('.')[0]}"
                nconfigs['theme']=f"{theme_list[themex]}.{theme_dir_list[x].split('.')[0]}"
                with open(f'{par_dir}config.yml', 'w')as f:
                    yaml.dump(configs, f)
                sel_theme()

    def menu_srv():
        x=menu(srv_list, 'select a server')
        if x==None:
            menu_root()
        else:
            quickjoin(srv_list[x])

    def menu_configs():
        """
        the configs menu for UpBox
        """
        global configs
        global nconfigs
        if not configs==nconfigs:
            if not config_dsp[0]=='[*] Apply':
                config_dsp.insert(0, '[*] Apply')
            else:
                config_dsp.remove('[*] Apply')
        else:
            if config_dsp[0]=='[*] Apply':
                config_dsp.remove('[*] Apply')
        sel_opt=menu(config_dsp, 'change the value of an option')
        if sel_opt==None:
            with open(f'{par_dir}config.yml', 'rb')as ff:
                configs=yaml.load(ff, Loader=yaml.FullLoader)
            with open(f'{par_dir}config.yml', 'rb')as ff:
                nconfigs=yaml.load(ff, Loader=yaml.FullLoader)
            menu_root()
        elif config_dsp[sel_opt]=='[*] Apply':
            with open(f'{par_dir}config.yml', 'w')as cnf:
                yaml.dump(nconfigs, cnf, indent=2)
            global new_opt
            configs[config_list[sel_opt]]=new_opt
            nconfigs[config_list[sel_opt]]=new_opt
            menu_configs()
        else:
            new_opt=input(f'{config_list[sel_opt]}: ')
            if new_opt=='':
                menu_configs()
            elif new_opt==config_list[sel_opt]:
                menu_configs()
            else:
                if str(new_opt).lower()=='true':
                    new_opt=True
                if str(new_opt).lower()=='false':
                    new_opt=False
                del [config_dsp[sel_opt]]
                config_dsp.insert(sel_opt, f'{config_list[sel_opt]}: {new_opt}')
                nconfigs[config_list[sel_opt]]=new_opt
                menu_configs()


    
    #the root menu
    root_index=0
    def menu_root():
        global root_index
        global root_dict
        global root_list
        if not configs['sticky-select']:
            root_index=0
        x=menu(root_list, 'Choose an option', cursor_index=root_index)
        if x==None:
            menu_root()
        elif not x==None:
            root_index=x
            root_dict[root_list[x]]()
    
    def censor(word, rep="*"):
        if bool(configs['filter-cuss']):
            for i in bad_words:
                word=str(word).replace(i, rep*len(i))
                
        return word
    
    def shell():
        script_lst=os.listdir(f"{par_dir}commands")
        script_list=[]
        for script in script_lst:
            if str(script).endswith(".ush"):
                script_list.append(script)

        while True:
            cmd=input('UpBox > ')
            if cmd=="exit":
                break
            if not cmd.endswith('.ush'):
                cmd+='.ush'
            if cmd=='.ush':
                continue
            elif os.path.exists(f"{par_dir}commands/{cmd}"):
                with open(f"{par_dir}commands/{cmd}")as cmd_f:
                    cmd_out = cmd_f.read()
                cmd_ord = cmd_out.split("\n")[0][2:].split(',')
                cmd_order = []
                for order in cmd_ord:
                    cmd_order.append([order.split(">")[0].replace(' ', ''), int(order.split(">")[1])])
                cmd_shell = cmd_out.split("#?shell")
                cmd_py = cmd_out.split("#?py")
                cmd_py_lam = cmd_out.split("#?py-lam")
                cmd_js = cmd_out.split("#?js")
                for i in cmd_order:
                    if i[0]=='py':
                        exec(cmd_py[i[1]].split('#>?split')[0])
                    if i[0]=='py-lam':
                        eval(cmd_py_lam[i[1]].split('#>?split')[0])()
                    elif i[0]=='shell':
                        for x in cmd_shell[i[1]].split('#>?split')[0].split('\n'):
                            os.system(x)
                    elif i[0]=='js':
                        with open(f"{par_dir}load.js", 'w')as f:
                            f.write(cmd_js[i[1]].split('#>?split')[0])
                        os.system(f"node '{par_dir}load.js'")
            else:
                log.error("Command does not exist")
        menu_root()
    
    login_tries=0
    def sign_up():
        while True:
            user=input('Enter a username to continue')
            usr_key=True
            if usr_key==True:
                passw=getpass('Enter a password to create the account: ')
                passw=getpass('Repeat password to create the account: ')
                return {"name": user, "password": passw}
                break
            else:
                print('Please enter a name to create a account\n')
                sign_up()
    
    def new_login():
         while True:
            user=getpass('\nEnter the username to continue')
            usr_key=True
            if usr_key==True:
                passw=getpass('Enter the password to the account: ')
                if passw=='':
                    print('Please enter at least 5 digit password\n')
                    ulogin()
                else:
                    return {"name": user, "password": passw}
                break
            else:
                login_tries=1
                print('Please username to login\n')
                ulogin()

    def login():
        while True:
            passw=getpass('Enter the password: ')
            lgn_sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            lgn_sock.connect(("127.0.0.1",2434))
            lgn_sock.send(json.dumps({"appdata": appdata, "userdata": {"usr": configs['username'], "psw": passw}}).encode())
            backdata=json.loads(lgn_sock.recv(1024).decode())
            if backdata['app']==True:
                if backdata['usr']:
                    break
                else:
                    log.error("Password incorrect")
            else:
                log.error("Please reinstall UpBox and try again")

    root_dict = {"select server": menu_srv, "select theme": sel_theme,
    "configs": menu_configs, "direct tools": direct_tools, "shell": shell, "quit": cli.quit}
    root_list = ['select server', 'select theme', "configs", 'direct tools', 'shell', 'quit']
    def add_menu(menu_name, command):
        root_dict[str(menu_name)]=command
        root_list.append(menu_name)
    
    #load mods if needed
    if bool(configs['scripts']):
        print('loading mods')
        nr1 = 0
        nr2 = 0
        module_l = []
        modules_s = os.listdir(f"{par_dir}scripts")
        modules_s.remove('upbox.py')
        for modules_ss in modules_s:
            log.info(f"loading mod '{modules_ss}'")
            with open(f'{par_dir}scripts/{modules_ss}')as module_fd:
                module_sd = module_fd.read()
            exec(censor(module_sd.split("':::'")[0], "_"))
            module_l.append(censor(module_sd))
            root_list.remove('quit')
            root_list.append('quit')
            delay(3)
    else:
        module_l=''

    os.system('clear')
    print(f"""{color(theme['fg'])}
 _    _       ____              ___   __ 
| |  | |     |  _ \            |__ \ /_ |
| |  | |_ __ | |_) | _____  __    ) | | |
| |  | | '_ \|  _ < / _ \ \/ /   / /  | |
| |__| | |_) | |_) | (_) >  <   / /_ _| |
 \____/| .__/|____/ \___/_/\_\ |____(_)_|
       | |                               
       |_|                               
                    
Creator: Klesty
youtube: @Klesty
Github: @Klesty""")
    
except:
    log.error('check error.log for info')
    with open(f'{par_dir}error.log', 'w')as err_f:
        err_f.write(str(traceback.format_exc()))
    quit()

#run
try:
    login()
    menu_root()
except:
    log.error('check error.log for info')
    with open(f'{par_dir}error.log', 'w')as err_f:
        err_f.write(str(traceback.format_exc()))
    quit()