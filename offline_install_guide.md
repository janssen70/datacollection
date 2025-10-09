# Downloading packages for offline use

For offline systems we need to prepare the set of
required files up-front. This instruction assumes
Debian package management. Of course, some file sharing mechanism must be
present to make the files available on the target.

**Important:** Replacing rsyslog using offline install is not as easy as installing axosyslog in the normal way

Outline:

- Prepare a system with identical distro. Run `cat /etc/os-release` on the
  target system to find out which one.
- Collect the packages for each required tool mentioned in the main README. Use
  the provided Python script. For example:
  ```sh
  cd 
  mkdir packages
  python3 datacollection/getpackages.py mosquitto packages
  python3 datacollection/getpackages.py axosyslog packages
  ```
- Get the packages- _and_ datacollection folder transferred to target system. You can zip them into a single archive:
  ```sh
  zip -r files.zip datacollection/ packages/
  ```
- Follow instructions below to install 

# Installing Collected .deb Packages on an offline System


## Option 1: Use `dpkg -i` directly

If you have the `.deb` files in a directory:

```bash
cd /path/to/deb-packages
sudo dpkg -i *.deb
```

- Installs all `.deb` files in the folder.
- **Limitation:** `dpkg` doesn’t resolve dependencies automatically. If some
  dependencies are missing, it may fail.
- To fix missing dependencies:

```bash
sudo dpkg -i *.deb
sudo apt-get install -f
```

- `apt-get install -f` will attempt to fix broken dependencies (requires
  network if missing packages are not available locally).


## Option 2: Make a local “APT repository” (recommended)

1. **Create a folder for the repo:**

```bash
mkdir -p ~/offline-repo
cp /path/to/deb-packages/*.deb ~/offline-repo/
cd ~/offline-repo
```

2. **Generate the package index:**

```bash
dpkg-scanpackages . /dev/null | gzip -9c > Packages.gz
```

- You may need `dpkg-dev`:

```bash
sudo apt-get install dpkg-dev
```

3. **Add the local repo to APT:**

```bash
sudo nano /etc/apt/sources.list.d/offline.list
```

Add a line:

```
deb [trusted=yes] file:/home/user/offline-repo ./
```

- Replace `/home/user/offline-repo` with your path.
- `[trusted=yes]` avoids signing the repo.

4. **Update APT:**

```bash
sudo apt-get update
```

5. **Install packages normally:**

```bash
sudo apt-get install curl vim
```

- APT will use your offline repo and resolve dependencies automatically.

---

## Option 3: Use APT cache with `--no-download`

```bash
sudo cp /path/to/deb-packages/*.deb /var/cache/apt/archives/
sudo apt-get install --no-download <package>
```

- Uses only cached `.deb` files.
- Works if all dependencies are already present.

---

### Recommended Approach

- **Single system / small package set:** Option 1 is fastest.
- **Multiple packages or multiple systems:** Option 2 (local repo) is cleaner
  and fully integrates with APT.

---

### Summary

| Method | Description | Notes |
|--------|------------|-------|
| `dpkg -i` | Install all `.deb` directly | May need multiple passes if dependencies are missing |
| Local APT repo | Use `dpkg-scanpackages` and add to APT | Clean, handles dependencies, offline-friendly |
| APT cache | Copy `.deb` to `/var/cache/apt/archives/` and install | Simple, but requires all dependencies to be present |


