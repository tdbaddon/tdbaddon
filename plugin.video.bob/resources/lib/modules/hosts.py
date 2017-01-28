import sys #used to get commandline arguments
import re #used for regular expressions
import xbmcgui
import xbmc
nhl_host_name = 'mf.svc.nhl.com'
nhl_ip_address = '104.251.218.27'


def host_in_host_file(host_name):
    try:
        if 'darwin' in sys.platform:
            file_name = '/private/etc/hosts'
        elif 'linux' in sys.platform:
            file_name = '/etc/hosts'
        elif 'win' in sys.platform:    
            file_name = 'c:\windows\system32\drivers\etc\hosts'
        else:
            return
        f = open(file_name, 'r')
        host_file_data = f.readlines()
        f.close()
        for item in host_file_data:
            if host_name in item:
                return True
        return False
    except:
        return

def update_host_file(ip_address, host_name):
    try: 
        if 'darwin' in sys.platform:
            try:
                file_name = '/private/etc/hosts'
                output_file = open(file_name, 'a')
                entry = "\n" + ip_address + "\t" + host_name + "\n"
                output_file.writelines(entry)
                output_file.close()
                return
            except:
                cmd = "echo '%s\t%s\n' | sudo tee -a /etc/hosts" % (nhl_ipaddress, nhl_hostname)
                os.system(cmd)
                return
        elif 'linux' in sys.platform:
            file_name = '/etc/hosts'
        elif 'win' in sys.platform:    
            file_name = 'c:\windows\system32\drivers\etc\hosts'
        else:
            return
        output_file = open(file_name, 'a')
        entry = "\n" + ip_address + "\t" + host_name + "\n"
        output_file.writelines(entry)
        output_file.close()
    except:
        return

def is_valid_ip_adress(ip_address):
    try: 
        parts = ip_address.split(".")
        if len(parts) != 4:
            return False
        if ip_address[-2:] == '.0': return False
        if ip_address[-1] == '.': return False
        for item in parts:
            if not 0 <= int(item) <= 255:
                return False
        return True
    except:
        return

def is_valid_host_name(host_name):
    try:  
        if len(host_name) > 255:
            return False
        if host_name[0].isdigit(): return False
        if host_name[-1:] == ".":
            host_name = host_name[:-1]
        allowed = re.compile("(?!-)[A-Z\d-]{1,63}(?<!-)$", re.IGNORECASE)
        return all(allowed.match(x) for x in host_name.split("."))
    except:
        return

def main():
    if xbmcgui.Dialog().yesno("BoB", "This will modify your Hosts file",
                              "Select [B]Yes[/B] to Continue, or [B]No[/B] to Cancel"):
        try:
            try:
                if not is_valid_ip_adress(nhl_ip_address):
                    sys.exit(2)

                if not is_valid_host_name(nhl_host_name):
                    sys.exit(2)

                if host_in_host_file(nhl_host_name):
                    sys.exit(2)

                update_host_file(nhl_ip_address, nhl_host_name)
            except:
                return
        except:
            pass

if __name__ == '__main__':
    main()
