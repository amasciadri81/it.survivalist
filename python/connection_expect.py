#!/usr/bin/python3
# 
# INSTALL PEXPECT
# sudo apt-get install python3-pexpect
#
# SET VI TAB FOR PYTHON
# set expandtab ts=4 sw=4 ai
#

import pexpect
import sys, base64, socket


IAD_PROMPT = r'> ?$'
COMMAND_PROMPT = r'[#\$~] ?$'

TERMINAL_PROMPT = r'Terminal type\?'
TERMINAL_TYPE = 'vt100'

SSH_NEWKEY = r'Are you sure you want to continue connecting \(yes/no\)\?'

USERNAME_PROMPT = '([Uu]ser)?[Nn]ame.*: ?$'
PASSWORD_PROMPT = '[Pp]ass[wo][wo]rd: ?$'


def usage():
    print(sys.argv[0], " [ip address]")


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
    return _connection(cmd, user, password, port, iad_cmd, show_login)


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

    i = child.expect([pexpect.TIMEOUT, '([Ff]ailed|[Ff]ail|[Df]enied)', SSH_NEWKEY, TERMINAL_PROMPT, USERNAME_PROMPT, PASSWORD_PROMPT, IAD_PROMPT, COMMAND_PROMPT, pexpect.EOF])

    if i == 0: # Timeout
        print('\n', 'ERROR: ', child.before.decode(), child.after)
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
        print('\n', 'ERROR: ', child.before.decode().lstrip(), child.after.decode().lstrip())
        sys.exit (1)

    else:
        print('\n', 'ERROR: ', child.before.decode().lstrip(), child.after.decode().lstrip())
        sys.exit (1)


def ssh_login_args(host, user, password, port=21, iad_cmd='sh'):
    """
    if script has 1 arg, set it as host 
    """

    if len(sys.argv) > 3 :
        usage()
        sys.exit (1)

    elif len(sys.argv) > 1:
        for v in range(1, len(sys.argv)): 
            if sys.argv[v] == 's':
                iad_to_prompt = False
            try:
                socket.inet_aton(sys.argv[v])
                host = sys.argv[v]
            except socket.error:
                None

    return ssh_login(host, user, password, port=port, iad_to_prompt=iad_to_prompt)


# -----------------------------------------------------------------------------------
"""
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

def example2():
    # connect to dev by ssh
    # launch 'show sysinfo' in iad_prompt
    # access to command_prompt and launch uptime command
    child = ssh('192.168.1.254', 'admin', 'password', port=21, show_login=False)
    show_cmds(child, True)
    child.sendline('show sysinfo')
    expect_prompt(child, iad_cmd='sh')
    child.sendline('uptime')
    expect_prompt(child)
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


if __name__ == '__main__':
    example1()


