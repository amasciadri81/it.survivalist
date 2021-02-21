#!/usr/bin/python3
# 
# INSTALL PEXPECT
# sudo apt-get install python3-pexpect
#
# SET VI TAB FOR PYTHON
# set expandtab ts=4 sw=4 ai
#

import pexpect
import sys, base64, socket, re


# trying to use $ to match the end of line would not work
IAD_PROMPT = r'> ?'
COMMAND_PROMPT = r'[#~\$] ?'

TERMINAL_PROMPT = r'Terminal type\?'
TERMINAL_TYPE = 'vt100'

SSH_NEWKEY = r'Are you sure you want to continue connecting \(yes/no\)\?'

USERNAME_PROMPT = r'([Uu]ser)?[Nn]ame.*: ?'
PASSWORD_PROMPT = r'[Pp]ass[wo][wo]rd: ?'


def usage():
    print()
    print(sys.argv[0], " <arg>" )
    print("      list : shows the list of saved ips")
    print("      ip address or saved name")
    print()
    sys.exit()


def show_cmds(child, show):
    """
    enable/disable showing on screen the commands of script and answers of server
       child: expect
       show:  boolean
    """
    if show:
        child.logfile_read = sys.stdout.buffer
    else:
        child.logfile_read = None


def interact(child):
    """
    before interact, disable output on screen to avoid showing the commands duplicated
    """
    show_cmds(child, False)
    child.interact()


def ssh(host, user=None, password=None, port=22, iad_cmd=None, show_login=False):
    # this option avoid ssh client to save/check hostkey of server
    # it avoids error when you connect to different devces with same ip
    options = '-o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null'

    cmd = 'ssh %s -p %s -l %s %s'%(options, port, user, host)
    return _connection(cmd, user, password, iad_cmd, show_login)


def telnet(host, user=None, password=None, port=23, iad_cmd=None, show_login=False):
    cmd = 'telnet %s %s'%(host, port)
    return _connection(cmd, user, password, iad_cmd, show_login)


def ftp(host, user=None, password=None, port=21, iad_cmd=None, show_login=False):
    cmd = 'ftp %s %s'%(host, port)
    return _connection(cmd, user, password, iad_cmd, show_login)


def _connection(client, user, password, iad_cmd, show_login):

    # decrypt if password is base64 encoded
    try:
        password = base64.b64decode(password).decode()
    except:
        None

    child = pexpect.spawn(client)
    show_cmds(child, show_login)
    expect_prompt(child, iad_cmd, user, password)
    show_cmds(child, False)
    return child


def expect_prompt(child, iad_cmd=None, username=None, password=None):
    """
    iad_cmd    cmd to pass from IAD_PROPMPT to COMMAND_PROMPT
    username   username
    password   password ASCII
    """
    timeout=10

    i = child.expect([pexpect.TIMEOUT, '([Ff]ailed|[Ff]ail|[Df]enied)', SSH_NEWKEY, TERMINAL_PROMPT, USERNAME_PROMPT, PASSWORD_PROMPT, IAD_PROMPT, COMMAND_PROMPT, pexpect.EOF], timeout=timeout)

    if i == 0: # Timeout
        print('\n', 'ERROR: TIMEOUT')
        sys.exit (1)

    elif i == 1: # fail denied
        print('\n', 'ERROR: ', child.before.decode().lstrip(), child.after.decode().lstrip())
        sys.exit (1)

    elif i == 2: # SSH does not have the public key. Just accept it.
        child.sendline ('yes')
        expect_prompt(child, iad_cmd, username, password)
        return

    elif i == 3: # terminal prompt
        child.sendline (TERMINAL_TYPE)
        expect_prompt(child, iad_cmd, username, password)
        return

    elif i == 4: # Username prompt
        child.sendline(username)
        expect_prompt(child, iad_cmd, username, password)
        return

    elif i == 5: # Password prompt
        child.sendline(password)
        expect_prompt(child, iad_cmd, username, password)
        return

    elif i == 6: # iad prompt
        if iad_cmd:
            child.sendline (iad_cmd)
            a = child.expect([COMMAND_PROMPT, 'Unknown command.'])
            if a != 0:
                print('\n', 'Prompt not available')
                sys.exit (1)
        return

    elif i == 7: # linux prompt
        return

    elif i == 8: # EOF
        print('\n', 'ERROR: ', child.before, child.after)
        sys.exit (1)

    else:
        print('\n', 'ERROR: ', child.before, child.after)
        sys.exit (1)


def get_host(list_ip):
    """
    check the arguments of script
    check if arg is name of ip addres saved in list_ip
    return the ip address of host
    """
    # no args
    if len(sys.argv) == 1:
        usage()

    # list args
    elif sys.argv[1] == 'list':
        for k, v in sorted(list_ip.items()):
            #print(f'{k:18} {v}')
            print(k, v)
        print()
        sys.exit()

    # IP
    elif re.match('(\d{1,3}\.){3}\d{1,3}', sys.argv[1]):
        return sys.argv[1]

    # string not ip
    elif sys.argv[1] in list_ip:
        return list_ip[sys.argv[1]]

    else:
        usage()



# -----------------------------------------------------------------------------------
"""
this script expect 2 different prompt:
    IAD_PROMPT     : is the 1st prompt; 
                     from IAD_PROMPT you can access to COMMAND_PROMPT by iad_cmd
                     if IAD_PROPMPT is not matched, iad_cmd is ignored
    COMMAND_PROMPT : is the final prompt

functions: 
    show_cmds(child, True)     show/hide commands output
    interact(child)            allow user interacting wiht shell         

    expect_prompt(child)
        iad_cmd       cmd to pass from IAD_PROPMPT to COMMAND_PROMPT  [default: None]
        username      username  [default: None]
        password      password ASCII   [default: None]

    ssh, telnet, ftp
        host          host ip
        user          username  [default: None]
        password      password, ASCII or base64 encrypted "echo -n password | base64"  [default: None]
        port          host port  [default: protocol std port]
        iad_cmd       command access to prompt from iad shell  [default: None]
        show_login    True|False -> showing on screen the commands of script and answers of server  [default: False]
"""

def example1():
    # connect to dev by ssh - doesn't show login commands
    child = ssh('192.168.1.254', 'admin', 'cGFzc3dvcmQ=')
    interact(child)

def example2():
    # if iad_prompt exist, it connect to command_prompt. It shows the logging commands
    child = ssh('192.168.1.254', 'admin', 'cGFzc3dvcmQ=', port=1053, iad_cmd='sh', show_login=True)
    interact(child)

def example3():
    # connect to dev by ssh
    child = ssh('192.168.1.254', 'admin', 'password', port=21, show_login=False)
    show_cmds(child, True)
    # launch show sysinfo
    child.sendline('show sysinfo')
    # pass from iad_prompt to command_prompt
    expect_prompt(child, iad_cmd='sh')
    # launch uptime
    child.sendline('uptime')
    expect_prompt(child)
    # interact
    interact(child)

def example_ftp():
    child = ftp('192.168.1.1', 'usr', 'pwd', show_login=True)
    child.sendline('get file.txt')
    expect_prompt(child)
    child.sendline('exit')

def example_cisco():
    # connect by telnet to cisco switch and enter as admin
    child = telnet('192.168.1.1', 'cisco', 'cisco', show_login=True)
    child.sendline('en')
    expect_prompt(child, password='cisco')
    interact(child)

def example_list():
    ip_list = {
        'ip1': '192.168.1.1',
        'ip2': '192.168.1.2'
    }
    child = ssh(get_host(ip_list), 'admin', 'admin', show_login=True)
    interact(child)

def example_empty_list():
    child = ssh(get_host({}), 'pi', 'raspberrypi', show_login=True)
    child.sendline('uptime')
    expect_prompt(child)
    interact(child)



if __name__ == '__main__':
    example_empty_list()

