# WSL

WSL, Windows Subsystem for Linux, can be seen as virtual machine running
Linux. Windows runs as the Host OS and Linux as the Guest OS. WSL takes care
of integration between Host and Guest. The datacollection tools run nicely on WSL 2, 
and mirrored network mode. Mirrored network mode allows the Windows host and Linux 
virtual machine to share the same external IP address. This makes it possible that 
services inside the Linux guest are reachable from outside.

Mirrored mode is enabled by creating a configfile. 
To get there, type %UserProfile% in the Windows Explorer location bar.

Here, create a file `.wslconfig`:

```ini
[wsl2]
networkingMode = mirrored
```

## Installation
- Enable WSL by opening cmd.exe or Powershell as Administrator and type `wsl
  --install`
- Install a Linux distribution through Microsoft app store. Recommended is Ubuntu 24.04 because the AxoSyslog instructions match that version.
- Note: After download, in case your windows configuration uses another drive
  than C: for your Downloads folder, you will run into a problem when starting Linux. If so, after download immediately move the app to C:. This is a simple task, go to Installed Apps, select the Linux app and chose ‘Move’.
- If you haven't done yet, configure mirrored networking (see above)
- Start WSL by double clicking the Ubuntu icon

## Connectivity check
**Important:** One gotcha is that despite the mirroring, he
Linux side is not reachable on the Windows side using the external IP address. You need to use
127.0.0.1 (localhost) instead. From other machines however, one can reach the
services running in the WSL Linux without problem, using the IP address of the
Windows host.

Do a basic connectivity check directly after install so that we can rule out this part later. On Ubuntu, use Python to start an ad-hoc webserver. It makes sense to use
port 5080 as that is the port that will be used by Openobserve. But any port will do, as long as you use the same number on the Windows side. For "well known" portnumbers, like 80 for web, you need to type ```sudo``` in front of the command.
```
python3 -m http.server -b 0.0.0.0 5080
```

On the Windows host, open Windows Powershell and try:

```cmd
curl http://127.0.0.1:5080
```

Or use the browser and type the url there. This should yield some filelist content of the
directory where the http server was started. When there is an error instead, try to
solve this first. Then try the same from another host, now using the
external IP address of the Windows device.









