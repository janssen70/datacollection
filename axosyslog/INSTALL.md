# AxoSyslog

AxoSyslog is a fork of syslog-ng, made by the original author of syslog-ng. The install procedure will also understand that the standard Ubuntu uses rsyslog and uninstall it first. You will end up with a replaced syslog that comes with a default configuration that mimics a default rsyslog. This makes the migration transparent/harmless on a standard Ubuntu. 

See: https://axoflow.com/docs/axosyslog-core/install/debian-ubuntu/

# Installation and configuration

Run as superuser:

```sh 
#!/bin/sh 
wget -qO - https://pkg.axoflow.io/axoflow-code-signing-pub.asc | gpg --dearmor > /usr/share/keyrings/axoflow-code-signing-pub.gpg
echo "deb [signed-by=/usr/share/keyrings/axoflow-code-signing-pub.gpg] https://pkg.axoflow.io/apt stable ubuntu-noble" | tee --append /etc/apt/sources.list.d/axoflow.list
apt update
apt install axosyslog
```

Openobserve provides an outline for the AxoSyslog configuration. 
Login to Openobserve -> Data sources -> Custom -> Logs -> Syslog-Ng

You can copy/paste the d_openobserve_http definition into
`/etc/syslog-ng/syslog-ng.conf`. Note that there is a mistake in Openobserve
version 0.15.1: In the url() definition, the port number must be removed.

```conf
@include "scl.conf"
source s_net { default-network-drivers(); };

destination d_openobserve_http {
    openobserve-log(
        url("http://127.0.0.1") # <- No port here
        organization("default")
        stream("syslog-ng")
        user("xxxxxx")
        password("xxxxxxx")
    );
};

log {
    source(s_net);
    destination(d_openobserve_http);
    flags(flow-control);
};
```

Next, activate this configuration and check that it works:

```
sudo systemctl restart syslog-ng
sudo systemctl status syslog-ng
```

# Setup of axis devices

Modern Azxis OS versions have a [JSON API](https://developer.axis.com/vapix/network-video/remote-syslog/) available to set a remote syslog target. For
older devices, details vary, [described here](https://help.axis.com/en-us/axis-os-knowledge-base#syslog).
