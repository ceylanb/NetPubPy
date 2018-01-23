#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os
import ftplib
import json
from pprint import pprint
from datetime import datetime
try:
	from colorama import init
	from colorama import Fore, Back, Style
	init()
except ImportError:
	print('Colorama module is not found.')
	print('Command for installation: python -m pip install colorama')
	exit()

try:
	import ftputil
except ImportError:
	print("\n # FTPUtil module is not found.")
	print(' # Command for installation: python -m pip install ftputil')
	exit()

print(Style.BRIGHT + Fore.RED + "----------------------------------------")
print(" # Coded by Ceylan Bozogullarindan")
print(" # If you get Connection Error 10060, read the Microsoft fix: https://goo.gl/qwdTG5")
print("----------------------------------------" + Style.RESET_ALL)

baseDir = ""

def setBaseDir(directory):
	global baseDir
	baseDir = directory

def updateFTP(local_path, ftp_path, ftp_host, ftp_user, ftp_pass, excepted_dirs, excepted_files, upload_files, force, delete_bin_folder, upload_dirs):
	with ftputil.FTPHost(ftp_host, ftp_user, ftp_pass) as ftp_host:	
		def deleteBinDir(path):
			list = ftp_host.listdir(path)
			for fname in list:	
				if ftp_host.path.isdir(path + fname):
					try:
						ftp_host.rmtree(path + fname)
					except:
						print("# Error: " + path + fname)
					else:
						print("# " + Fore.WHITE + path + fname + Style.RESET_ALL + " is deleted." )
				else:
					if "App_" in fname:
						deleteFile(path + fname)
					else:
						print("# " + path + fname + " is not deleted.")
			print(Style.BRIGHT + Fore.RED + "\n----------------------------------------------------------")				
			print(" # All files which begin with 'App_' are deleted.")
			print(" # All directories in BIN directory are deleted.")
			print("----------------------------------------------------------\n" + Style.RESET_ALL)		

		def uploadDir(localDir, ftpDir):
			list = os.listdir(localDir)
			for fname in list:
				if os.path.isdir(localDir + fname):				
					if(ftp_host.path.exists(ftpDir + fname) != True and ftp_host.path.exists(ftpDir + fname.lower()) != True): # Case sensitivity is disabled
						try:
							if localDir + fname in [baseDir + directory for directory in excepted_dirs]:
								print("# " + Fore.RED + ftpDir + fname + Style.RESET_ALL + " is not created!")
							else:					
								ftp_host.mkdir(ftpDir + fname)
								print("# " +Fore.WHITE + ftpDir + fname + Style.RESET_ALL + " is created.")
								uploadDir(localDir + fname + "/", ftpDir + fname + "/")
						except ftplib.all_errors as e:
							print("# " + Fore.RED + ftpDir + fname + Style.RESET_ALL + " is not created! Error message: " + str(e))
					else:
						if fname == "bin":
							if delete_bin_folder == "1":
								deleteBinDir(ftp_path + "bin/")
							uploadDir(localDir + fname + "/", ftpDir + fname + "/")
						elif localDir + fname in [baseDir + directory for directory in excepted_dirs]:
							print("# " + Fore.RED + localDir + fname + Style.RESET_ALL + " is not uploaded.")
						else:
							uploadDir(localDir + fname + "/", ftpDir + fname + "/")
				else:
					if ftpDir == "bin":			
						if "App_" in fname:
							uploadFile(localDir + fname, ftpDir + fname)
						else:
							print("# " + Fore.WHITE + localDir + fname + Style.RESET_ALL + " is not uploaded.")
					else:							
						if (localDir + fname) in ([baseDir + file for file in excepted_files]):
							print("# " + Fore.RED + localDir + fname + Style.RESET_ALL + " is not uploaded.")							
						else:
							uploadFile(localDir + fname, ftpDir + fname)

		def deleteFile(target):
			try:
				ftp_host.remove(target)
			except:
				print("# Error: " + target)
			else:
				print("# " + Fore.WHITE + target + Style.RESET_ALL + " is deleted." )			

		def uploadFile(source, target):
			if force == "1":
				if(ftp_host.upload(source, target)):
					print("# " + Fore.WHITE + source + Style.RESET_ALL + " is uploaded.")
			else:
				try:
					if(ftp_host.upload_if_newer(source, target)):
						print("# " + Fore.WHITE + source + Style.RESET_ALL + " is uploaded.")
					else:
						print("# " + Fore.WHITE + target + Style.RESET_ALL + " has already been uploaded.")
				except ftplib.all_errors as e:
					print("# " + Fore.RED + target + Style.RESET_ALL + " is not uploaded! Error message: " + str(e))

		def uploadFiles(source, target):
			for fname in upload_files:
				uploadFile(source + fname, target + fname)

		def uploadDirs(source, target):
			for directory in upload_dirs:
				uploadDir(source + directory, target + directory)

		startTime = datetime.now()
		#uploadFile("app_offline.htm", ftp_path + "app_offline.htm")
		uploadDir(local_path, ftp_path)
		uploadFiles(local_path, ftp_path)
		uploadDirs(local_path, ftp_path)
		#deleteFile(ftp_path + "app_offline.htm")
		print(datetime.now() - startTime)
	print("Completed.")

with open('config.json') as data_file:    
	data = json.load(data_file)
	for ftp in data["ftps"]:
		local_path = ftp["local_path"]
		ftp_path = ftp["ftp_path"]
		ftp_host = ftp["ftp_host"]
		ftp_user = ftp["ftp_user"]
		ftp_pass = ftp["ftp_pass"]
		excepted_dirs = ftp["excepted_dirs"]
		excepted_files = ftp["excepted_files"]
		upload_files = ftp["upload_files"]
		force = ftp["force"]
		delete_bin_folder = ftp["delete_bin_folder"]
		upload_dirs = ftp["upload_dirs"]
		
		if ftp["active"] == "1":
			setBaseDir(local_path)			
			updateFTP(local_path, ftp_path, ftp_host, ftp_user, ftp_pass, excepted_dirs, excepted_files, upload_files, force, delete_bin_folder, upload_dirs)

