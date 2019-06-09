#!/usr/bin/python3
import os
import time
import spur

host_list = []
user_pass_list = [ ('root', 'root'), ('pi', 'raspberry'), ('admin', 'admin'), ('administrator', 'admin'), ('debian', 'debian'), ('ubuntu', 'ubuntu')]
good_cred_list = []
quit = False

def list_to_string(lst, sort=False):
    if sort == True:
        lst.sort()
    
    s = ''
    for item in lst:
        # append item to string:
        s += item
        # add comma if not last item in list:
        if item != lst[-1]:
            s += ','
    return s

def status():
    strstat = ''
    strstat += 'Host List:  '
    strstat += list_to_string(host_list) + '\n'
    strstat += 'User/Pass List:  '
    
    #for user, passwd in user_pass_list:
    tlist = [n1 + ':' + n2 for (n1, n2) in user_pass_list]
    strstat += list_to_string(tlist)
    
    return strstat
    
class cred(object):
    def __init__(self, host='', user='', passwd=''):
        self.host = host
        self.user = user
        self.passwd = passwd
    
def main():
    
    done = False
    while (done == False):
        host = input('Please type a target host (name or ip), press enter when done:  ')
        if host != '':
            host_list.append(host)
        else:
            done = True
            
    print(status())
    
    #while(quit == False):
    for host in host_list:
        print ('Target host: ' + host)
        for user, passwd in user_pass_list:
            print (user + ':' + passwd + '...')
            with spur.SshShell(hostname=host, username=user, password=passwd) as shell:
                try:
                    result = shell.run(["echo", "-n", "OK"])
                    print(result.output)
                    good_cred_list.append(cred(host, user, passwd))
                except Exception as ex:
                    if 'Authentication failed' in str(ex):
                        print('-- bad user/pass:')
                time.sleep(.5)    

    print(str(len(good_cred_list)) + ' working credential(s) found.')

if __name__ == '__main__':
    main()