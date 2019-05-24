from pexpect import popen_spawn

child = popen_spawn.PopenSpawn('ssh root@10.100.200.75')
i = child.expect(['Permission denied', 'Terminal type', '[#\$] '])
if i == 0:
    print('Permission denied on host. Can\'t login')
    child.kill(0)
elif i == 1:
    print('Login OK... need to send terminal type.')
    child.sendline('vt100')
    child.expect('[#\$] ')
elif i == 2:
    print('Login OK.')
    print('Shell command prompt', child.after)
