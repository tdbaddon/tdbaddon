import subprocess
import os

proxy_hack_process = None

__script_dir__ = os.path.dirname(os.path.realpath(__file__))
__jar_file_path__ = os.path.join(__script_dir__, 'FuckNeulionV2.jar')


def run_proxy_hack(game_id, team_type):
    global proxy_hack_process

    kill_proxy_hack()

    #######
    # Run proxy hack process
    #######

    # Hides the command window in Windows
    startupinfo = None
    if os.name == 'nt':
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW

    # Run the command
    try:
        command = ['java', '-jar', __jar_file_path__, game_id, team_type]
        log('Command: ' + str(command))
        proxy_hack_process = subprocess.Popen(command,
                                              stdout=subprocess.PIPE,
                                              stderr=subprocess.STDOUT,
                                              startupinfo=startupinfo)
    except:
        command = 'java -jar "%s" %s %s' % (__jar_file_path__, game_id, team_type)
        log('Command failed, trying again in shell: ' + command)
        proxy_hack_process = subprocess.Popen(command,
                                              stdout=subprocess.PIPE,
                                              stderr=subprocess.STDOUT,
                                              startupinfo=startupinfo,
                                              shell=True)


    output = proxy_hack_process.stdout.readline().strip()
    success = output == 'HOUSTON, WE HAVE LIFT OFF.'

    return success, output


def kill_proxy_hack():
    global proxy_hack_process

    # Kill already running process, if any
    if proxy_hack_process is not None:
        proxy_hack_process.kill()
        proxy_hack_process.wait()

def log(msg):
    print 'proxyhack: ' + msg