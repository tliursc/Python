import subprocess

def MScheck():
	cmd='arp -a'
	p=subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE)
	result=p.stdout.read().strip().decode('gbk')
	print result
MScheck()