#!/usr/bin/python3
par_dir=''

with open(f'{par_dir}error.log', 'w')as err_f:
        err_f.write('')
#libs
try:
    import traceback
    import os
    import sys
    import json
    import socket
    import subprocess
    from threading import Thread
    import time
    from datetime import datetime
    import random
    import re
    import threading
    from better_profanity import profanity
    import simple_term_menu as stm
    import pwinput
    import secrets
    from PIL import ImageColor
    from cryptography.fernet import Fernet
    import yaml
    from glob import glob
except Exception as e:
    print('[error] check error.log for info')
    with open(f'{par_dir}error.log', 'w')as err_f:
        err_f.write('lib\n'+str(e))

#initialize
try:
    class cli:
        def quit():
            try:
                os.system('clear')
                quit()
            except:
                False
    def res_color():
        return '\033[0m'
    def color(fg, background=False):
        r, g, b=ImageColor.getcolor(str(fg), 'RGB')
        return '\033[{};2;{};{};{}m'.format(48 if background else 38, r, g, b)
    
    class log:
        def info(txt):
            print(f"{color('#21c500')}[INFO] {color('#fff')}{txt}")
        def warn(txt):
            print(f"{color('#b5cd00ff')}[WARN] {color('#fff')}{txt}")
        def error(txt):
            print(f"{color('#cb0000')}[ERROR] {color('#fff')}{txt}")

    def tprint(text, delay=.05):
        for c in text:
            print(c, end='', flush=True)
            time.sleep(delay)
    
    def tinput(text='', sep=': ', delay=.05):
        for c in f"{text}{sep}":
            print(c, end='', flush=True)
            time.sleep(delay)
        return input()
    
    def ptinput(text='', sep=': ', delay=.05):
        for c in f"{text}{sep}":
            print(c, end='', flush=True)
            time.sleep(delay)
        return pwinput.pwinput('')

    last_menu=''
    class menus:
        LOGIN='login'
        ROOT='root'
        SETTINGS='settings'
        SRV='srv_menu'
        D_TOOLS='direct_tools'
        def add(menu_name, command):
            str11[str(menu_name)]=command
            str12.append(menu_name)
    srv_list = []
    for srv_file in os.listdir(f'{par_dir}servers'):
        if srv_file.endswith('.json'):
            srv_list.append(srv_file.replace('.json', ''))
    
    theme_list=[]
    for x in glob(f'{par_dir}themes/*/', recursive=True):
        theme_list.append(str(x).split('/')[1])
        
    #print(theme_list)
    str11 = {"select server": 'srv_menu()', "select theme": "sel_theme()", "settings": "settings()", "direct tools": 'direct_tools()', 'quit': 'cli.quit()'}
    str12 = ['select server', 'select theme', "settings", 'direct tools', 'quit']
    with open(f'{par_dir}config.yml', 'rb')as ff:
        configs=yaml.load(ff, Loader=yaml.FullLoader)
    with open(f'{par_dir}config.yml', 'rb')as ff:
        nconfigs=yaml.load(ff, Loader=yaml.FullLoader)
    filter_cuss = configs['filter_cuss']
    mods_enabled = configs['scripts']

    
    with open(f"{par_dir}themes/{str(configs['theme']).split('.')[0]}/{str(configs['theme']).split('.')[-1]}.json")as theme_file:
        theme = json.load(theme_file)
except Exception as e:
    with open(f'{par_dir}error.log', 'w')as err_f:
        print(traceback.format_exc())
        err_f.write(str(traceback.format_exc()))

try:
    config_list=[]
    for x in configs:
        config_list.append(x)
    config_dsp=[]
    for x in configs:
        config_dsp.append(f'{x}: {configs[x]}')
    #the direct tools
    tools_list=os.listdir(f'{par_dir}tools')
    def open_direct_tool(direct_tool_name):
        with open(f"{par_dir}tools/{direct_tool_name}")as dtf:
            dts = dtf.read()
        
        if str(direct_tool_name).endswith('.py'):
            exec(dts)
        elif str(direct_tool_name).endswith('.dll'):
            exec(dts)
        elif str(direct_tool_name).endswith('.sh'):
            os.system(dts)
        elif str(direct_tool_name).endswith('.bat'):
            os.system(dts)
        time.sleep(1)
        os.system('clear')
        direct_tools()

    def direct_tools():
        x=menu(tools_list, 'Execute a direct tool', type=menus.D_TOOLS)
        if x==None:
            root()
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
            time.sleep(.7)
            s.send(uname.encode())
            print(f'[CLIENT] connected')
            new_data = s.recv(1024).decode()
            message_s = str(re.findall(r'\[.*?\]', new_data)[0])
            message = new_data.replace(f'{message_s}', '')
            print(get_color_escape(main_theme['client'][0]['server color']['red'],main_theme['client'][0]['server color']['green'],main_theme['client'][0]['server color']['blue'])+message_s,get_color_escape(main_theme['theme'][0]['fg']['red'],main_theme['theme'][0]['fg']['green'],main_theme['theme'][0]['fg']['blue']),message)
            print(get_color_escape(main_theme['client'][0]['client color']['red'], main_theme['client'][0]['client color']['green'], main_theme['client'][0]['client color']['blue']))
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
                time.sleep(1)
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
        if not configs['sticky select']:
            themex=0
        themex=menu(theme_list, 'Choose a theme', cursor_index=themex)
        if themex==None:
            root()
        else:
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

    def srv_menu():
        x=menu(srv_list, 'select a server', menus.SRV)
        if x==None:
            root()
        else:
            quickjoin(srv_list[x])

    def settings():
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
        sel_opt=menu(config_dsp, 'change the value of an option', menus.SETTINGS)
        if sel_opt==None:
            with open(f'{par_dir}config.yml', 'rb')as ff:
                configs=yaml.load(ff, Loader=yaml.FullLoader)
            with open(f'{par_dir}config.yml', 'rb')as ff:
                nconfigs=yaml.load(ff, Loader=yaml.FullLoader)
            root()
        elif config_dsp[sel_opt]=='[*] Apply':
            with open(f'{par_dir}config.yml', 'w')as cnf:
                yaml.dump(nconfigs, cnf, indent=2)
            global new_opt
            configs[config_list[sel_opt]]=new_opt
            nconfigs[config_list[sel_opt]]=new_opt
            settings()
        else:
            new_opt=tinput(config_list[sel_opt], delay=.03)
            if new_opt=='':
                settings()
            elif new_opt==config_list[sel_opt]:
                settings()
            else:
                if str(new_opt).lower()=='true':
                    new_opt=True
                if str(new_opt).lower()=='false':
                    new_opt=False
                del [config_dsp[sel_opt]]
                config_dsp.insert(sel_opt, f'{config_list[sel_opt]}: {new_opt}')
                nconfigs[config_list[sel_opt]]=new_opt
                settings()
    
     #create menu modifier
    def menu(items, title, type=menus.ROOT, cursor_index=0, clear=True):
        global theme
        global last_menu
        global menu_out
        cli=stm.TerminalMenu(items, title=title, menu_highlight_style=(theme['highlight']),
        menu_cursor_style=theme['cursor-color'], cursor_index=cursor_index,
        menu_cursor=theme['cursor'], clear_screen=clear)
        return cli.show()

    #load mods if needed
    if bool(mods_enabled) == True:
        print('loading mods')
        nr1 = 0
        nr2 = 0
        module_l = []
        modules_s = os.listdir(f"{par_dir}scripts")
        modules_s.remove('upbox.py')
        for modules_ss in modules_s:
            print(f"loading mod '{modules_ss}'")
            with open(f'{par_dir}scripts/{modules_ss}')as module_fd:
                module_sd = module_fd.read()
            exec(module_sd.split("':::'")[0])
            module_l.append(module_sd)
            print('mod loaded')
            str12.remove('quit')
            str12.append('quit')
    else:
        module_l = ''
    
    #the root menu
    root_index=0
    def root():
        global root_index
        global str11
        global str12
        if not configs['sticky select']:
            root_index=0
        x=menu(str12, 'Choose an option', cursor_index=root_index)
        if x==None:
            root()
        else:
            root_index=x
            exec(f'{str11[str12[x]]}')
    
    login_tries=0
    def sign_up():
        while True:
            user=tinput('Enter a name to continue', delay=.016)
            usr_key=True
            if usr_key==True:
                passw=ptinput('Enter a password to create the account', delay=.016)
                passw=ptinput('Repeat password to create the account', delay=.016)
                return {"name": user, "password": passw}
                break
            else:
                tprint('Please enter a name to create a account\n', delay=.016)
                sign_up()
    
    def new_login():
         while True:
            user=tinput('\nEnter the username to continue', delay=.016)
            usr_key=True
            if usr_key==True:
                passw=ptinput('Enter the password to the account', delay=.016)
                if passw=='':
                    tprint('Please enter at least 5 digit password\n', delay=.016)
                    ulogin()
                else:
                    return {"name": user, "password": passw}
                break
            else:
                login_tries=1
                tprint('Please username to login\n')
                ulogin()

    def login():
        while True:
            passw=ptinput('Enter the password', delay=.017)
            if passw=='':
                tprint('Please enter at least 5 digit password\n', delay=.016)
                login_tries=1
                login()
            else:
                return {"password": passw}
            break

    time.sleep(3)
    os.system('clear')
    print(f"""
{color('#ff0000')} _    _       ____                 ___   __ 
{color('#ffee00')}| |  | |     |  _ \               |__ \ /_ |
{color('#1eff00')}| |  | |_ __ | |_) | _____  ________ ) | | |
{color('#0048ff')}| |  | | '_ \|  _ < / _ \ \/ /______/ /  | |
{color('#7300ff')}| |__| | |_) | |_) | (_) >  <      / /_ _| |
{color('#00a2ff')} \____/| .__/|____/ \___/_/\_\    |____(_)_|
       | |                                  
       |_|
{color(theme['fg'])}{res_color()}                                  
Creator: Klesty
youtube: @Klesty
Github: @Klesty""")

except:
    log.error('check error.log for info')
    with open(f'{par_dir}error.log', 'w')as err_f:
        err_f.write(str(traceback.format_exc()))

#run
try:
    login()
    root()
except:
    log.error('check error.log for info')
    with open(f'{par_dir}error.log', 'w')as err_f:
        err_f.write(str(traceback.format_exc()))