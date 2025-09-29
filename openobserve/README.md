# Openobserve

## Install

See: https://openobserve.ai/downloads/ and https://openobserve.ai/docs/getting-started/ Use, option 2: Self-hosted option)

I installed by running this command in `/home/erik/datacollection/openobserve`:

```sh
curl -L -o openobserve-ee-v0.15.1-linux-amd64.tar.gz https://downloads.openobserve.ai/releases/o2-enterprise/v0.15.1/openobserve-ee-v0.15.1-linux-amd64.tar.gz && tar -xzf openobserve-ee-v0.15.1-linux-amd64.tar.gz
```

This way the location matches the paths in the .service file. You may want to use the simd binary instead. The simd version ran fine on my laptop under WSL but not on my older bare metal server (4th gen Core i7).
Note, installed this way Openobserve stores its data under the local user account which may not be what you want.

## Run

Adapt `..\settings.env` and `openobserve.service` to your local situation. You can testdrive interactively as follows:

```sh
. ..\settings.env
export ZO_ROOT_USER_EMAIL
export ZO_ROOT_USER_PASSWORD
./openobserve
```
Test the availability of the webserver on port 5080. Use Ctrl-C to shut it down. When openobserve runs correctly you can install the service file.

```sh
sudo cp openobserve.service /etc/systemd/system
sudo systemctl daemon-reload
sudo systemctl start openobserve
sudo systemctl status openobserve
sudo systemctl enable openobserve
```
