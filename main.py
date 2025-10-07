#!/usr/bin/env python3
import os
import subprocess
import textwrap
import sys

CRD_SSH_Code = input("Google CRD SSH Code : ").strip()
Pin = 123456

if os.geteuid() != 0:
    print("jalankan script ini sebagai root. keluar.")
    sys.exit(1)

os.environ["DEBIAN_FRONTEND"] = "noninteractive"

class CRDRootXFCE:
    def __init__(self):
        self.install_crd()
        self.install_xfce()
        self.ensure_run_user_for_root()
        self.configure_crd_session()
        self.finish()

    @staticmethod
    def install_crd():
        print("-> menginstall Chrome Remote Desktop...")
        subprocess.run(['wget', '-q', 'https://dl.google.com/linux/direct/chrome-remote-desktop_current_amd64.deb'])
        subprocess.run(['dpkg', '--install', 'chrome-remote-desktop_current_amd64.deb'])
        subprocess.run(['apt', 'install', '--assume-yes', '--fix-broken'])
        print("-> Chrome Remote Desktop terpasang")

    @staticmethod
    def install_xfce():
        print("-> menginstall XFCE4 full...")
        os.system("apt update -y && apt install --assume-yes xfce4 xfce4-goodies dbus-x11 dbus-user-session")
        print("-> XFCE4 full terpasang")

    @staticmethod
    def ensure_run_user_for_root():
        run_user_dir = "/run/user/0"
        if not os.path.exists(run_user_dir):
            os.makedirs(run_user_dir, exist_ok=True)
            os.chown(run_user_dir, 0, 0)
            os.chmod(run_user_dir, 0o700)
            print("-> dibuat /run/user/0 untuk session root")
        else:
            print("-> /run/user/0 sudah ada")

    @staticmethod
    def configure_crd_session():
        print("-> menulis /etc/chrome-remote-desktop-session (XFCE root session)...")
        session_script = textwrap.dedent("""\
        #!/bin/bash
        export XDG_RUNTIME_DIR=/run/user/0
        if [ -z "$DBUS_SESSION_BUS_ADDRESS" ]; then
          eval $(dbus-launch --sh-syntax --exit-with-session)
        fi
        exec /usr/bin/startxfce4
        """)
        with open('/etc/chrome-remote-desktop-session', 'w') as f:
            f.write(session_script)
        os.chmod('/etc/chrome-remote-desktop-session', 0o755)
        print("-> session XFCE root ditulis")

    @staticmethod
    def finish():
        print("-> restart dbus dan chrome-remote-desktop...")
        os.system("systemctl daemon-reload || true")
        os.system("service dbus restart || true")
        os.system("service chrome-remote-desktop restart || true")

        if CRD_SSH_Code:
            print("-> jalankan host setup...")
            os.system(f"{CRD_SSH_Code} --pin={Pin}")
        else:
            print("-> tidak ada CRD auth code, dilewati")

        print("\n✅ selesai. XFCE4 siap diakses via Chrome Remote Desktop sebagai root.")

if __name__ == "__main__":
    if CRD_SSH_Code.strip() == "":
        print("masukkan auth code dari Google CRD. keluar.")
        sys.exit(1)
    if len(str(Pin)) < 6:
        print("pin minimal 6 digit.")
        sys.exit(1)
    CRDRootXFCE()
