#!/usr/bin/python3

def except_manage():
    """
    raise cmd send back Exception
    """
    try:
        True
        #raise NameError('HiThere')
        #f = open('bh1.py', 'r')     # wrong file
        #a = 1/0                     # division by 0
        #a = '2' + 2                 # str + int
        a = int('ciccio')           # value error
    except (TypeError, ValueError):
        print ("--- Error ---")
        print("TypeError or ValueError")
        raise
    except BaseException as inst:
        print ()
        print ("--- Error ---")
        print ('INSTANCE: ', inst       )
        print ('TYPE:     ', type(inst) )
        print ('ARGS:     ', inst.args  )
        raise inst
    else:
        print ("--- NO Error ---")
        print()
    finally:
        print("finally: I works before try statment complete ")

if True:
    print()
    try: 
        except_manage()
    except BaseException as inst:
        print ()
        print ('--- Parent ---')
        print ('INSTANCE: ', inst       )
        print ('TYPE:     ', type(inst) )
        print ('ARGS:     ', inst.args  )
        print ('--------------')
        print ()

# -------------------------------------------------------------------------------------
# CHANGE EXCEPTION TYPE

def func():
    raise IOError

def err_manage_from():
    try:
        func()
    except IOError as exc:
        raise RuntimeError('Failed to open database') from exc

def err_manage_from_none():
    try:
        func()
    except IOError as exc:
        raise RuntimeError('Failed to open database') from None

if False:
    err_manage_from_none()
    err_manage_from()
# -------------------------------------------------------------------------------------


