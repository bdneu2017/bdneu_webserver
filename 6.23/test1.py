import os,shutil,re
def main():
    pattern=re.compile(r'^([01]?\d\d?|2[0-4]\d|25[0-5])\.([01]?\d\d?|2[0-4]\d|25[0-5])\.([01]?\d\d?|2[0-4]\d|25[0-5])\.([01]?\d\d?|2[0-4]\d|25[0-5])$')
    filepath=raw_input("Input file path:")
    if os.path.isfile(filepath)
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
    else:
        return "ERROR"
			
if __name__ == "__main__":
	main()