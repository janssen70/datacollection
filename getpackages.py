#!/usr/bin/env python3
import subprocess
import sys
import os
import shutil
from pathlib import Path

def run(cmd, capture_output=False, check=True):
    """Run a shell command safely."""
    result = subprocess.run(cmd, shell=True, text=True,
                            capture_output=capture_output)
    if check and result.returncode != 0:
        raise subprocess.CalledProcessError(result.returncode, cmd)
    return result

def is_real_package(pkg):
    """Return True if pkg is a real package, False if virtual/unavailable."""
    try:
        result = run(f"apt-cache show {pkg}", capture_output=True, check=False)
        for line in result.stdout.splitlines():
            if line.startswith("Package:"):
                return True
        return False
    except Exception:
        return False

def already_downloaded(pkg, target_dir):
    """Check if a .deb for this package already exists."""
    path = Path(target_dir)
    for f in path.glob(f"{pkg}_*.deb"):
        return True
    return False

def download_package(pkg, target_dir):
    """Download a real package using apt-get download."""
    try:
        print(f"Downloading {pkg}...")
        run(f"apt-get download {pkg}", check=True)
        return True
    except subprocess.CalledProcessError:
        print(f"Failed to download {pkg}, skipping.")
        return False

def main():
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <package> [target_dir]")
        sys.exit(1)

    package = sys.argv[1]
    target_dir = Path(sys.argv[2] if len(sys.argv) > 2 else ".").resolve()
    target_dir.mkdir(parents=True, exist_ok=True)

    if shutil.which("apt-rdepends") is None:
        print("Installing apt-rdepends...")
        run("sudo apt-get update")
        run("sudo apt-get install -y apt-rdepends")

    # Get recursive dependency list
    print(f"Resolving dependencies for {package}...")
    try:
        result = run(f"apt-rdepends {package}", capture_output=True)
        deps = sorted(set(line.strip() for line in result.stdout.splitlines()
                          if line.strip() and not line.startswith(" ")))
    except subprocess.CalledProcessError:
        print(f"Error: could not resolve dependencies for {package}")
        sys.exit(1)

    # Download each package
    failed_packages = []
    for pkg in deps:
        if not is_real_package(pkg):
            print(f"Skipping virtual or unavailable package {pkg}")
            continue
        if already_downloaded(pkg, target_dir):
            print(f"Skipping {pkg} (already downloaded)")
            continue
        success = download_package(pkg, target_dir)
        if not success:
            failed_packages.append(pkg)

    if failed_packages:
        print("\nSome packages failed to download:")
        for pkg in failed_packages:
            print(f"  {pkg}")
    else:
        print("\nAll downloadable packages saved successfully.")

    print(f"Downloaded packages are in: {target_dir}")

if __name__ == "__main__":
    main()
