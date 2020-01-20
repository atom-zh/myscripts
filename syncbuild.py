# coding=utf-8
# python version should > 2.7.10
#shannon 2019.11.28

import os
import sys
import git
import time
import pexpect
import threading
from git import Git
import xml.dom.minidom
from xml.dom.minidom import parse
import pdb

#maxconnections = 8
#semlock = threading.BoundedSemaphore(maxconnections)

def get_time():
    return time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))

def update_ap_repository(codeaurora, repository, name):
    os.chdir(repository)
    print "Current Dir:"+os.getcwd()
    print get_time()+" | update repository: "+name+" Start \n"
    
    if "external/private_le" in repository:
        cmd = "git remote update"
        child = pexpect.spawn(cmd, timeout=1000)
        child.logfile = sys.stdout
        index = child.expect(["id_rsa_sdx55_asa':", pexpect.EOF, pexpect.TIMEOUT])
        if index == 0:
            child.sendline("136132\n")
            print "Repository:"+name+" input pwd over!"
            #semlock.release()
            child.wait()
            print get_time()+" | update repository: "+name+" Successful \n"
        else:
            print get_time()+" | update repository: "+name+" Error \n"
            #semlock.release()
        child.close()
    else:
        time.sleep(2)
        #semlock.release()
        os.system("git remote update")
        """
        cmd = "/usr/bin/git remote update"
        child = pexpect.spawn(cmd, timeout=1800)
        child.logfile = sys.stdout
        child.wait()
        child.close()
        """
        print get_time()+" | update repository: "+name+" Successful \n"

def creat_ap_repository(codeaurora, repository, name):
    print "Current Dir:"+os.getcwd()
    print get_time()+" | creat repository: "+name+" Start \n"
    if "external/private_le" in repository:
        cmd = "git clone --mirror  "+codeaurora+"/"+name+" "+repository
        child = pexpect.spawn(cmd, timeout=2000)
        child.logfile = sys.stdout
        index = child.expect(["id_rsa_sdx55_asa':", pexpect.EOF, pexpect.TIMEOUT])
        if index == 0:
            child.sendline("136132\n")
            print "Repository:"+name+" input pwd over!"
            
            index = child.expect(["Receiving objects:", pexpect.EOF, pexpect.TIMEOUT])
            if index == 0:
                #semlock.release()
                child.wait()
                print get_time()+" | creat repository: "+name+" Successful \n"
            else:
                print get_time()+" | creat repository: "+name+" timeout\n"
        else:
            #semlock.release()
            print get_time()+" | creat repository: "+name+" Error \n"
        child.close()
    else:
        """
        cmd = "git clone --mirror "+codeaurora+"/"+name+" "+repository
        child = pexpect.spawn(cmd, timeout=2000)
        child.logfile = sys.stdout
        index = child.expect(["Receiving objects:", pexpect.EOF, pexpect.TIMEOUT])
        if index == 0:
            #semlock.release()
            child.wait()
            print get_time()+" | creat repository: "+name+" Successful \n"
        else:
            print get_time()+" | creat repository: "+name+" timeout\n"
        child.close()
        """
        #semlock.release()
        os.system("git clone --mirror  "+codeaurora+"/"+name+" "+repository)
        print get_time()+" | creat repository: "+name+" Successful \n"
    
    print "creat repository:"+os.getcwd()

def update_modme_repository(modem_repository):
    repo_list = os.listdir(modem_repository)
    print repo_list
    for repository in repo_list:
        os.chdir(modem_repository+repository)
        print "Current Dir:"+os.getcwd()
        print get_time()+" | update repository: "+repository+" Start \n"
        
        #os.system("git remote update")  
        cmd = "git remote update"
        child = pexpect.spawn(cmd)
        child.logfile = sys.stdout
        index = child.expect(["Username for", pexpect.EOF, pexpect.TIMEOUT])
        if index == 0:
            child.sendline("asa.wang@quectel.com\n")
            index = child.expect(["Password for", pexpect.EOF, pexpect.TIMEOUT])
            if index == 0:
                child.sendline("Asa.wang@12\n")
                print "Repository:"+repository+" input pwd over!"
                child.wait()
                print get_time()+" | update repository: "+repository+" Successful \n"
            else:
                print get_time()+" | update repository: "+repository+" username Error\n"
                print "username error!" 
            child.close()
        else:
           print get_time()+" | update repository: "+repository+" timeout Error\n"
        
        print "-----------------------------------------------------------------------------\n"

def update_all_repository(projectlist_file):
    print "Update all repository ..."



def handle_gitlist_xml(config_xml):
    cafs={}
    codeaurora=None
    DOMTree = xml.dom.minidom.parse(config_xml)
    manifest = DOMTree.documentElement
    remote_list = manifest.getElementsByTagName("remote")
    default_list = manifest.getElementsByTagName("default")
    project_list = manifest.getElementsByTagName("project")
    base_path = os.getcwd()
   
    for remote in remote_list:
        cafs[remote.getAttribute("name")]=remote.getAttribute("fetch")
    print "CAF List: "+str(cafs)

    for default in default_list:
        if default.hasAttribute("remote"):
            caf = default.getAttribute("remote")
    print "Default CAF: "+caf
    
     
    for project in project_list:
        if project.hasAttribute("remote"):
            codeaurora = cafs[project.getAttribute("remote")]
        else:
            codeaurora = cafs[caf]

        if codeaurora.find('https') >= 0:
            codeaurora = codeaurora.replace('https','http')
        print "Codeaurora:"+codeaurora
        
        mid_path = codeaurora.split('/',3)[3]
        if mid_path and mid_path[-1] != '/':
            mid_path+='/'
        print "Mid path:"+mid_path
        
        #codeaurora
        if project.hasAttribute("name"):
            name = mid_path+project.getAttribute("name")+".git"
            repository = base_path+"/"+name
            print "Repository:"+repository
             
            os.chdir(base_path)
            #semlock.acquire()
            if os.path.exists(repository):
                #continue
                print "Repository name: "+name+" exist, Run git remote update ..."
                update_ap_repository(codeaurora, repository, name)
                #t = threading.Thread(target=update_ap_repository, args=(codeaurora, repository, name))
            else:
                print "Repository name: "+name+" none, Run git clone ..."
                creat_ap_repository(codeaurora, repository, name)
                #t = threading.Thread(target=creat_ap_repository, args=(codeaurora, repository, name))
            time.sleep(3)
            #t.start()

        time.sleep(5)
        print "-----------------------------------------------------------------------------\n"

def manifest_check(manifest):
    if os.path.exists(manifest):
        print "OK, Manifest file valid!"
        return
    else:
        print "Warning, manifest file not found!"
        print "try to update manifest..."
        os.chdir(os.path.dirname(manifest))
        print os.getcwd()
        os.system("git pull origin release")
        if os.path.exists(manifest):
            print "OK, File valid!"
            return
        else:
            print "ERROR, File valid!"
            print "A list of valid IDs can be found at Qualcomm manifest.git"
            sys.exit(1)

def sdx55_init(WKDIR):
    os.system("git config --global http.proxy 'socks5://127.0.0.1:9222'")
    os.system("git config --global https.proxy 'socks5://127.0.0.1:9222'")
    os.chdir("/home/git/.ssh/")
    os.system("sudo sslocal -c shawdowsocks.json -d stop")
    time.sleep(2)
    os.system("sudo sslocal -c shawdowsocks.json -d start")
    os.chdir(WKDIR)

def sdx55_deinit(WKDIR):
    os.chdir("/home/git/.ssh/")
    os.system("sudo sslocal -c shawdowsocks.json -d stop")
    os.system("git config --global --unset http.proxy")
    os.system("git config --global --unset https.proxy")
    os.chdir(WKDIR)


def usage(WKDIR):
	print "\nUsage:"
	print "We need atlest one arg"
	print "example: python git_update.py  LE.BR.1.2.1-99700-9x07 \n"

def main(argv):
    config_xml = None
    if len(argv) < 2:
        usage()
    
    WKDIR = os.getcwd()
    print WKDIR

    build_id = argv[1]
    
    #sdx55_deinit(WKDIR)
    if "9x07" in build_id:
        version = build_id.split('-')[1]
        if int(version) >= 61900:
            print "Pbulic Version : "+version
            manifest = WKDIR+"/quic/le/le/manifest/"+build_id+".xml"
            manifest_check(manifest)
        else:
            manifest = WKDIR+"/quic/le/mdm/manifest/"+build_id+".xml"
            manifest_check(manifest)
        
        print os.getcwd()
        print "9x07 config"
    
    if "AU_LINUX_QSDK_NHSS" in build_id:
        manifest = WKDIR+"/quic/qsdk/releases/manifest/qstak/"+build_id+".xml"
        manifest_check(manifest)
        
        print os.getcwd()
        print "QSDK config"

    if "SDX24" or "SDX20" in build_id:
        manifest = WKDIR+"/quic/le/le/manifest/"+build_id+".xml"
        manifest_check(manifest)
        
        print os.getcwd()
        print "SDX24 config"
    
    if "15m" in build_id:
        manifest = WKDIR+"/quic/le/le/manifest/"+build_id+".xml"
        manifest_check(manifest)
        
        print os.getcwd()
        print "SAM config"
    
    if "SDX55" in build_id:
        version = build_id.split('-')[1]
        if int(version) >= 4900:
            print "Pbulic Version : "+version
            manifest = WKDIR+"/quic/le/le/manifest/"+build_id+".xml"
            manifest_check(manifest)

        else:
            print "Private Version : "+version
            sdx55_init(WKDIR)
            manifest = WKDIR+"/external/private_le/le/manifest/"+build_id+".xml"
            manifest_check(manifest)
       
        print os.getcwd()
        print "sdx55 config"
    
    os.chdir(WKDIR)
    
    if "ALL" == build_id:
        projectslist_file = "../../projects.list"
        update_all_repository(projectslist_file)
    else:
        handle_gitlist_xml(manifest)
    
    if "SDX55" in build_id:
        sdx55_deinit(WKDIR)

    modem_repository = WKDIR+"/quectel-wireless-solutions-co-ltd/"
    update_modme_repository(modem_repository)

if __name__ == '__main__':
    main(sys.argv)
