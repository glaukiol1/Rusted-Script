# Copyright (c) Rusted Studio
# Licensed under APGL-3.0 license. Read LiCENSE.txt for more info
#Developers:
# CertifiedRice - Lead Developer
# Rusted Studio - Development Studio
# Rusted Script Github Repository Contributors - Developers

import sys
import rustedscript

run_line=True

def checkForComments(line):
	indexOfComment = int( line.find("//") )
	if indexOfComment == -1:
		indexOfComment = int( line.find("#") )
	if indexOfComment == -1:
		indexOfComment = int( line.find("/*") )
	if indexOfComment != -1:
		if indexOfComment == 0:
			remove=0
		else:
			remove=1
		newline=line[0:indexOfComment-remove]
	else:
		newline=line
	return newline


with open(sys.argv[1]) as rustedfile: # open the rusted file
	print("    Running {}".format(sys.argv[1])+'...\n')
	lines = rustedfile.readlines()
	cnt=0
	for line in lines:
		if int(line.find('/*')) != -1 and run_line is True:
			run_line = False
		if len(checkForComments(line))>0:
			if run_line is False:
				if int(line.find('*/')) != -1:
					if len(line)==1:
						remove=0
					else:
						remove=1
					run_line=True
			else:
				if int(line.find('use("')) != -1:
					start=int(line.find('("'))
					end=int(line.find('")'))
					try:
						fileToInclude=open(line[start+2:end],'r')
					except FileNotFoundError:
						print("FATAL: File {} not found.".format(line[start+2:end]))
						sys.exit(1)
					linesOfFileToInclude = fileToInclude.readlines()
					run_extened_file=True
					for line in linesOfFileToInclude:
						if int(line.find('/*')) != -1 and run_extened_file is True:
							run_extened_file = False
						if len(checkForComments(line))>1:
							if run_extened_file is False :
								if int(line.find('*/')) >= 0:
									if len(line)==1:
										remove=0
									else:
										remove=1
									run_extened_file=True
									break
							elif run_extened_file is True:
								if len(checkForComments(line))==1:
									remove=0
								else:
									remove=1
								if len(checkForComments(line))>1 and int(checkForComments(line).find('*/')) == -1:
									result, error = rustedscript.run('<stdin>', checkForComments(line)[0:len(line)-remove])
									if error:
										print(error.as_string())
										print("\n---- \n FATAL: Process exited with non-zero exit code")
										sys.exit(1)
				if len(checkForComments(line))==1:
					remove=0
				else:
					remove=1
				if len(checkForComments(line))>1:
					# check for module includes
					if int(checkForComments(line).find('use_module("'))!=-1:
						start = int(line.find('("'))
						end = int(line.find('")'))
						try:
							moduleToInclude=open('../rusted_modules/'+line[start+2:end]+'/index.rusted', 'r')
						except FileNotFoundError:
							print("FATAL: File ../rusted_modules/{}/index.rusted not found.".format(line[start+2:end]))
							sys.exit(1)
						linesOfModuleToInclude=moduleToInclude.readlines()
						for line_ in linesOfModuleToInclude:
							if int( line_.find('use("') ) != -1:
								start = int(line_.find('("'))
								end = int(line_.find('")'))
								try:
									fileToInclude_ =open(line_[start+2:end], 'r')
								except FileNotFoundError:
									print("FATAL: File ../rusted_modules/{}/index.rusted not found.".format(line_[start+2:end]))
									sys.exit(1)
								for line__ in fileToInclude_.readlines():
									if len(checkForComments(line__))>1:
										if len(checkForComments(line))==1:
											remove_=1
										else:
											remove_=2
										result_, error_ = rustedscript.run('<stdin>', checkForComments(line)[0:len(line__)-remove_])
										if error_:
											print(error_.as_string())
											print('\n There is a problem with the "{}" package.'.format(line[start+2:end]))
											sys.exit(1)
										elif result_:
											print(result_)
							elif int( line_.find('use("') ) == -1:
								if len(checkForComments(line_))>1:
									len_of_line=len(checkForComments(line_))
									if len_of_line==1:
										remove__=1
									else:
										remove__=2
									result____, error____ = rustedscript.run('<stdin>', checkForComments(line_)[0:len(checkForComments(line_))-remove])
									if error____:
										print(error____.as_string())
										print("\n---- \n FATAL: Process exited with non-zero exit code ||||||")
										sys.exit(1)
									elif result____:
										print(result____)
					elif int( line.find('use_module') ) == -1:
						result, error = rustedscript.run('<stdin>', checkForComments(line)[0:len(line)-remove])
						if error:
							print(error.as_string())
							print("\n---- \n FATAL: Process exited with non-zero exit code")
							sys.exit(1)
						elif result:
							print(result)
						cnt+=1
	print("\n---- \n SUCCESS: {} ran successfully".format(sys.argv[1]))



