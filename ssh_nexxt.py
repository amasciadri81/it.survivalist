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

SHOW_CMD = True     # True show expect commands
PASSWORD_PROMPT = '[Pp]ass[wo][wo]rd: *'
SERCOMM_PROMPT = '> '
COMMAND_PROMPT = '[\$#~] '
TERMINAL_PROMPT = r'Terminal type\?'
TERMINAL_TYPE = 'vt100'
SSH_NEWKEY = r'Are you sure you want to continue connecting \(yes/no\)\?'

def usage():
    print(sys.argv[0], " [ip address]")


def show_cmd(child):
    if SHOW_CMD:
        child.logfile_read = sys.stdout.buffer


def ssh_interact(child):
    child.logfile = None
    child.logfile_read = None
    child.interact()


def ssh_login(host, user, password, linux_shell=True):
    """
    host:           host ip
    user:           ssh username
    password:       ssh password, clear or base64 encrypted
    linux_shell:    True|False -> if DUT has sercomm shell, script will send 'sh' command
    """
    try:
        password = base64.b64decode(password).decode()
    except:
        None

    child = pexpect.spawn('ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -l %s %s'%(user, host))
    show_cmd(child)
    child = expect_prompt(child, linux_shell, password)
    return child


def expect_prompt(child, linux_shell, password=None):
    i = child.expect([pexpect.TIMEOUT, 'Permission denied', SSH_NEWKEY, TERMINAL_PROMPT, PASSWORD_PROMPT, SERCOMM_PROMPT, COMMAND_PROMPT, pexpect.EOF])
    if i == 0: # Timeout
        print('ERROR: SSH could not login. Here is what SSH said: ', child.before.decode(), child.after)
        sys.exit (1)
    if i == 1: # Permission denied
        print('Permission denied')
        sys.exit (1)
    if i == 2: # SSH does not have the public key. Just accept it.
        child.sendline ('yes')
        expect_prompt(child, linux_shell, password)
        return child
    if i == 3: # terminal prompt
        child.sendline (TERMINAL_TYPE)
        expect_prompt(child, linux_shell, password)
        return child
    if i == 4: # Password prompt
        child.sendline(password)
        expect_prompt(child, linux_shell, password)
        return child
    if i == 5: # sercomm prompt
        if linux_shell:
            child.sendline ('sh')
            a = child.expect (['Unknown command.', COMMAND_PROMPT])
            if a == 0:
                print('Linux shell not available')
                sys.exit (1)
            else:
                return child
        else:
            return child
    if i == 6: # linux prompt
        return child
    if i == 7: # EOF
        print('ERROR: ', child.before.decode().lstrip())
        sys.exit (1)

    print('ERROR: ', child.before.decode())
    sys.exit (1)

def ssh_login_args(host, user, password, linux_shell=True):
    """
    if script has 1 arg, set it as host 
    """

    if len(sys.argv) > 3 :
        usage()
        sys.exit (1)

    elif len(sys.argv) > 1:
        for v in range(1, len(sys.argv)): 
            if sys.argv[v] == 's':
                linux_shell = False
            try:
                socket.inet_aton(sys.argv[v])
                host = sys.argv[v]
            except socket.error:
                None

    return ssh_login(host, user, password, linux_shell)


def nexxt():
    child = ssh_login_args('192.168.1.254', 'ser_wan', 'UGljY2luNi1CcnV0dDYtTXV0Ng==', linux_shell=False)
    child.logfile_read = sys.stdout.buffer
    child.sendline('show sysinfo')
    child.expect(SERCOMM_PROMPT)
    child.sendline('sh')
    child.expect(COMMAND_PROMPT)
    child.logfile_read = None
    child.sendline()
    ssh_interact(child)


if __name__ == '__main__':
    nexxt()
