import os,shutil,re

def Checkfile(filepath):
    if os.path.isfile(filepath):
        return 1
    else:
        return 0

def Readfile(filepath,pattern):
    fp1=open(filepath,"r")
    fp2=open("ip2.txt","w")
    for line in open(filepath):
        line=fp1.readline()
        str=re.findall(pattern,line)
        for i in range(len(str)):
            print str[i]
            fp2.write(str[i]+'\n')
    fp2.close()
    fp1.close()
	
def main():
    pattern=re.compile(r'\b(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b')
    filepath=raw_input("Input file path:")
    if Checkfile(filepath):
        Readfile(filepath,pattern)
    else:
        return "ERROR"
			
if __name__ == "__main__":
	main()