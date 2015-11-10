#! /usr/bin/env python
# -*- coding: utf-8 -*-
#Author:pako
#Email:zealzpc@gmail.com
import re
# from pexpect import *
class ssh_win32:
    def __init__(self, user, host, password=None,systemroot='c',papath='',timeout=5,verbose=0):

        self.user = user#监控机器的username
        self.host = host#监控机器的ip
        self.verbose = verbose
        self.password = password#密码
        self.timeout=timeout#执行命令的timeout
        self.systemroot=systemroot#windows 所安装的盘符
        if not papath:#powershell.exe的路径
            self.powershell_path=self.systemroot+':/WINDOWS/system32/WindowsPowerShell/v1.0/powershell.exe '
        self.key = [
            'authenticity',
            'assword:',
            '@@@@@@@@@@@@',
            'Command not found.',
            EOF,
            ]
        
        self.f = open('ssh.out','w')

    def ssh(self,command):
        cmd='ssh -l %s %s %s'%(self.user,self.host,command)
        print "cmd:",cmd
        con=spawn(cmd,timeout=self.timeout)
        seen=con.expect(self.key)
        if seen == 0:
            con.sendline('yes')
            seen = con.expect(self.key)
        if seen == 1:
    #        if not self.password:
    #            self.password = getpass.getpass('Remote password: ')
            con.sendline(self.password)
            try:
                res=con.read()
            except Exception ,e:
                res=con.before
#            print "res:",res
        return res
    def ssh_disk(self):
        cmd=self.powershell_path+"Get-WmiObject win32_logicaldisk"
        res=self.ssh(cmd)
        disk={}
        if res:
            res=res.split('No such file or directory')[-1].replace('\r','').split('\n')
            res=[c for c in res if c]
#            print 'res:',res
        predisk='C'
        for d in res:
#            print d
            key,value=d.split(':',1)
#            print d
#            print 'key:',key,'value:',value
            key=key.strip()
            value=value.strip()
            if key=='DeviceID' and value not in disk.keys():
                predisk=value
                disk[predisk]={}
                disk[predisk][key]=value
            else:
                if key in ['FreeSpace','Size']:
                    if value:
                        value=int(value)/1024/1024/1024
                disk[predisk][key]=value
        for d in disk.keys():
            if disk[d]['DriveType']!='3':
                disk.pop(d)
#        print 'disk:',disk
        return disk
    
    def ssh_cpu(self): 
        cmd=self.powershell_path+'gwmi -computername localhost win32_Processor'
        res=self.ssh(cmd)
        res=res.split('No such file or directory')[-1].replace('\r','').split('\n')
        res=[r for r in res if r]
#        print res
        cpu={}
        for i in res:
#            print '='*10
#            print i
            i=i.split(':')
        #    print i
            if len(i)==2:
                key,value=i
            else:
                continue
            key=key.strip()
            value=value.strip()
#            print 'key:',key
#            print 'value:',value
            cpu[key]=value
        return cpu
    
    def ssh_memory(self):
        totalmem=self.powershell_path+'Get-WmiObject win32_OperatingSystem TotalVisibleMemorySize'
        freemem=self.powershell_path+'Get-WmiObject win32_OperatingSystem FreePhysicalMemory'
        memory={}
        for cmd in [totalmem,freemem]:
            res=self.ssh(cmd)
            if 'Win32_OperatingSystem' in res:
                res=res=res.replace('\r','').split('\n')
                res=[m for m in res if m][-1]
                print 'res:',res
                key,value=res.split(':')
                key=key.strip()
                value=value.strip()
                memory[key]=value
            else:
                print "not return data"
                return None
        return memory
    def ssh_ping(self,host):
        cmd='ping -n 1 %s'%host
        patt=r'.+?(\d*)% loss.*'
        res=self.ssh(cmd).replace('\r','').replace('\n','')
        print res
        m=re.match(patt,res)
        if m:
            lost_percent=m.group(1)
            print 'lost_percent:',lost_percent
            return int(lost_percent)
        else:
            return None
        
    def ssh_ps(self):
        cmd=self.powershell_path+'ps'
        res=self.ssh(cmd)
        ps=[]
        if '-- -----------' in res:
            res=res.replace('\r','').split('-- -----------')[-1].split('\n')
            res=[d for d in res if d.strip()]
            for p in res:
                process={}
                row=[para for para in p.split(' ') if para.strip()]
                process['handles']=row[0]
                process['npm']=row[1]
                process['pm']=row[2]
                process['ws']=row[3]
                process['vm']=row[4]
                process['cpu']=row[5]
                process['id']=row[6]
                process['process_name']=row[-1]
                ps.append(process)
#            print ps
            return ps
        else:
            return None
    def ssh_netstat(self):
        cmd='netstat -ao'
        res=self.ssh(cmd)
        netstat=[]
        if 'PID' in res:
            res=res.replace('\r','').split('PID')[-1].split('\n')
            res=[d for d in res if d.strip()]
            for p in res:
                process={}
                row=[para for para in p.split(' ') if para.strip()]
                process['proto']=row[0]
                process['local_address']=row[1]
                process['foreign_address']=row[2]
                process['state']=row[3]
                process['pid']=row[-1]
                netstat.append(process)
#            print netstat
            return netstat
        else:
            return None
if __name__ == "__main__":
    cmd="c:/WINDOWS/system32/WindowsPowerShell/v1.0/powershell.exe ps"
    user='admin'
    host='192.168.123.105'
    password='123456'
    ssh=ssh_win32(user,host,password,systemroot='c',timeout=5)
#    print ssh.ssh_cpu()
#    print "\n\n\n\n"
#    print ssh.ssh_disk()
#    print "\n\n\n\n"
#    print ssh.ssh_memory()
#    print ssh.ssh_ping(host)
#    print ssh.ssh_ps()
#    print ssh.ssh_netstat()