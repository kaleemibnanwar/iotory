from helpers import threadlister, http_checker,http_checker_nout,file_to_list,lister, stopper, file_to_ips,cidr_to_ips,range_to_ips
import threading,sys
from tqdm import tqdm
import urllib3
from os import system
from time import sleep
import argparse
from colorama import Fore
from argparse import RawTextHelpFormatter
ips=[]
banner=Fore.GREEN+"""
                 hunt them!
            _-_ 
           [∅‿∅]
         <+/.  ,======>
           | _ |          _ _
           |   |  ` _____('-')
            U U    {`-+:-+)   
            L L     l l l >
	@kaleemibnanwar @cyberinspects
	"""
parser = argparse.ArgumentParser(description=banner+Fore.YELLOW,formatter_class=RawTextHelpFormatter)
parser.add_argument('-r','--range', type=str,required=False,help='Network range using with ip addresses like [192.168.0.1-192.168.0.100]')
parser.add_argument('-c','--cidr',type=str, help='Network CIDR as target like 192.168.0.1/24')
parser.add_argument('-f','--file',type=str, help='Text file containing target ranges, cidrs or ip addresses')
parser.add_argument('-p','--ports',type=str, help='Ports to http servers')
parser.add_argument('-P','--ports_list',type=str, help='Ports list for http servers')
parser.add_argument('-t','--threads',type=int, help='Number of threads to work at a single time like 100 or 1000 depending upon your system. The more number threads means more speed')
parser.add_argument('-o','--output',type=str, help='Output file path')
parser.add_argument('-T','--timeout',type=int, help='Set timeout for requests.')
parser.add_argument('-F','--failed',action='store_true', help='You can pass this parameter to see failed attempts.')
args = parser.parse_args()

tes=300
try:
	if args.threads:
		tes=int(args.threads)
	if args.file:
		ips=file_to_ips(file_to_list(args.file,'r'))
	if args.range:
		ips=range_to_ips(args.range)
	if args.cidr:
		ips=cidr_to_ips(args.cidr)
except: 
	pass

if len(ips)==0:
	parser.error(Fore.RED+'No Ip addresses could be generated, make sure you are providing target ranges accurately.')
	sys.exit()

failed=False
if args.failed:
	failed=True
timeout=10
if args.timeout:
	timeout=args.timeout
if args.output:
	output_file=open(args.output,'w+')
	output_file.write('Title,Server,Port,Address\n')

ports=['80','8080']
if args.ports:
	ports=args.ports.split(',')
if args.ports_list:
	ports=file_to_list(args.ports_list,'r')

urllib3.disable_warnings()
output_data=[]
threads = []
system('rm -rf __pycache__')
thread_lists=lister(ips,tes)
no_threads=len(thread_lists)

print(Fore.GREEN+banner)
try:
	print(Fore.YELLOW+f'[{no_threads}] threads are going to start scaning')
	sleep(3)
	total=len(ips)*len(ports)
	com=0

	scan=''
	for i in range(no_threads):
		if args.output:
			t = threading.Thread(target=http_checker, args=(thread_lists,i,ports,output_file,scan,failed,timeout))
		else:
			t = threading.Thread(target=http_checker_nout, args=(thread_lists,i,ports,scan,failed,timeout))
		threads.append(t)
	for thread in threads:
		thread.start()
	for thread in threads:
		thread.join()
except KeyboardInterrupt:
	print(Fore.RED+"Termination interrupt called")
	stopper()
