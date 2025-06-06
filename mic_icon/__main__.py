#!/usr/bin/env python3

import sys
import threading
import subprocess
import signal

import pulsectl
import gi

gi.require_version('Gtk', '3.0')
gi.require_version('AppIndicator3', '0.1')
from gi.repository import Gtk, GLib, AppIndicator3

ICON_UNMUTED = "microphone"
ICON_MUTED = "gtk-cancel"


class MicIcon:
    def __init__(self):
        self.ind = AppIndicator3.Indicator.new(
            "mic-icon",
            ICON_UNMUTED,
            AppIndicator3.IndicatorCategory.APPLICATION_STATUS
        )
        self.ind.set_status(AppIndicator3.IndicatorStatus.ACTIVE)

        menu = Gtk.Menu()
        quit_item = Gtk.MenuItem(label="Quit")
        quit_item.connect("activate", self.quit)
        menu.append(quit_item)
        menu.show_all()
        self.ind.set_menu(menu)

        self.pulse = pulsectl.Pulse('mic-icon')

        self.p = subprocess.Popen(
            ["pactl", "subscribe"],
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            text=True, bufsize=1
        )

        thr = threading.Thread(
            target=self._pactl_subscribe_loop,
            name="Pactl-Subscribe-Reader",
            daemon=True
        )
        thr.start()

        GLib.unix_signal_add(
            GLib.PRIORITY_DEFAULT,
            signal.SIGINT,
            self.quit,
            None
        )

        self._update_icon()

    def _pactl_subscribe_loop(self):
        if not self.p.stdout:
            return

        for line in self.p.stdout:
            if " on source " in line:
                GLib.idle_add(self._update_icon, priority=GLib.PRIORITY_LOW)
        self.p.stdout.close()
        self.p.wait()

    def _update_icon(self):
        try:
            default_name = self.pulse.server_info().default_source_name
            src = self.pulse.get_source_by_name(default_name)
            muted = src.mute
        except Exception:
            muted = False

        icon = ICON_MUTED if muted else ICON_UNMUTED
        self.ind.set_icon_full(icon, icon)
        return False

    def quit(self, *args):
        if hasattr(self, 'p') and self.p.poll() is None:
            self.p.terminate()
        Gtk.main_quit()
        return False


def main():
    MicIcon()
    Gtk.main()
    sys.exit(0)


if __name__ == "__main__":
    main()
