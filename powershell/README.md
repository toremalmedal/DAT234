How to run scripts in docker-container (avoid powershell contamination on linux distro):

```
docker run -v "$(pwd)"/scripts:/tmp/containerdata -it --rm mcr.microsoft.com/powershell pwsh /tmp/containerdata/caesars.ps1
docker run -v "$(pwd)"/scripts:/tmp/containerdata -it --rm mcr.microsoft.com/powershell pwsh /tmp/containerdata/scytale.ps1

#The ping-script wants some input right away, my dude:
docker run -v "$(pwd)"/scripts:/tmp/containerdata -it --rm mcr.microsoft.com/powershell pwsh /tmp/containerdata/ping.ps1 127.0.0.1/24
```

This mounts the volume scripts to /tmp/containerdata, then runs the container interactively ( -i for keeping stdin open) with a terminal (-t).
The docker image used is mcr.microsoft.com/powershell, and it uses its pwsh-command to run the powershell-script.
