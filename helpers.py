import requests
import urllib3
from ipaddress import *
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import netaddr,sys
from colorama import Fore
from os import system
from bs4 import BeautifulSoup as soup
import urllib3

urllib3.disable_warnings()
def http_checker(thread_lists,list_index,ports,output_file,thname,failed,timeout):
	com=0
	for ip in thread_lists[list_index]:
		for port in ports:
			session = requests.Session()
			retry = Retry(connect=2, backoff_factor=0.5)
			adapter = HTTPAdapter(max_retries=retry)
			session.mount('http://', adapter)
			com+=1
			url=''
			scheme='http'
			try:
				if port=='443':
					scheme='https'					
				response = requests.get('{scheme}://{ip}:{port}/'.format(scheme=scheme,ip=ip,port=port),verify=False, timeout=timeout)
				page = response.content
				if 'Server' in response.headers:
					server=response.headers['Server'].strip().replace('\n','')
				page_soup = soup(page, "xml") 
				title = page_soup.find("title")
				title = title.text.strip()
				title.replace(',',' ')
				if title == '':
					title="[<blank>]"
				port=str(str(port).replace('\n',''))
				url=f'http://{ip}:{port}/'
				data = f'{title},{server},{port},{url}\n'
				pdata = f'{title} | {server} | {port} | http://{ip}:{port}/ | [{com}/{len(ports)*len(thread_lists[list_index])}]'
				print(Fore.GREEN+pdata)
				output_file.write(data)
			except:
				if failed==True:
					print(Fore.RED+f'Couldn\'t connect to http://{ip}:{port}'.replace('\n','')+'/')



def http_checker_nout(thread_lists,list_index,ports,thname,failed,timeout):
	com=0
	for ip in thread_lists[list_index]:
		for port in ports:
			session = requests.Session()
			retry = Retry(connect=2, backoff_factor=0.5)
			adapter = HTTPAdapter(max_retries=retry)
			session.mount('http://', adapter)
			com+=1
			url=''
			scheme='http'
			try:
				if port=='443':
					scheme='https'					
				response = requests.get('{scheme}://{ip}:{port}/'.format(scheme=scheme,ip=ip,port=port),verify=False, timeout=timeout)
				page = response.content
				if 'Server' in response.headers:
					server=response.headers['Server'].strip().replace('\n','')
				page_soup = soup(page, "xml") 
				title = page_soup.find("title")
				title = title.text.strip()
				title.replace(',',' ')
				if title == '':
					title="[<blank>]"
				port=str(str(port).replace('\n',''))
				url='http://{ip}:{port}/'
				data = f'{title},{server},{port},{url}\n'
				pdata = f'{title} | {server} | {port} | http://{ip}:{port}/ | [{com}/{len(ports)*len(thread_lists[list_index])}]'
				print(Fore.GREEN+pdata)
			except:
				if failed==True:
					print(Fore.RED+f'Couldn\'t connect to http://{ip}:{port}'.replace('\n','')+'/')


def lister(ips,thno):
	listlen=len(ips)
	thrd=thno
	items_for_one_thread=int(listlen/thrd)+1
	mainlist=[]
	index=0
	for sublist in range(thrd):
		a=[]
		for item in range(int(items_for_one_thread)):
			if index<listlen:
				a.append(ips[index])
				index=index+1
			else:
				break
		if a!= []:
			mainlist.append(a)
		else:
			break
	return mainlist

def stopper():
	try:
		sys.exit()
	except KeyboardInterrupt:
		stopper()


def file_to_list(path,mode):
	mylist=[]
	file=open(path,mode)
	for line in file.readlines():
		line.replace('\n','')
		mylist.append(line)
	return mylist

def cidr_to_ips(cidr):
	ips=[]
	net=ip_network(str(cidr.replace('\n','')))
	for ip in list(IPv4Network(net, False).hosts()):
			ips.append(ip)
	return ips

def ip(ip):
	ips=[]
	ips.append(IPv4Address(ip))

def range_to_ips(rang):
	ips=[]
	rang=rang.split('-')
	cidrs = netaddr.iprange_to_cidrs(rang[0], rang[1])
	for net in cidrs:
		for ip in IPv4Network(net):
			ips.append(ip)
	return ips

def file_to_ips(mylist):
	ips=[]
	for item in mylist:
		if ':' in item:
			pass
		else:
			if '-' in item:
				ips=ips+range_to_ips(item)
			if '/' in item:
				ips=ips+cidr_to_ips(item)
			if len(item.split('.'))==4 and '-' not in item and '/' not in item:
				ips=ips+ip(item)
	return ips


def threadlister(path,thno):
	listfromfile=[]
	with open(path,'r') as file:
		lines=file.readlines()
		for line in lines:
			line=line.replace('\n','')
			listfromfile.append(line)

	listlen=len(listfromfile)
	thrd=thno
	items_for_one_thread=int(listlen/thrd)+1
	mainlist=[]
	index=0
	for sublist in range(thrd):
		a=[]
		for item in range(int(items_for_one_thread)):
			if index<listlen:
				a.append(listfromfile[index])
				index=index+1
			else:
				break
		if a!= []:
			mainlist.append(a)
		else:
			break
	return mainlist




