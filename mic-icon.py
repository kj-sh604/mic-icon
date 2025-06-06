#!/usr/bin/env python3

import sys
import pulsectl
import gi

gi.require_version('Gtk', '3.0')
gi.require_version('AppIndicator3', '0.1')

from gi.repository import Gtk, GLib, AppIndicator3

# ICON NAMES from the default Adwaita icon set:
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

        quit_item = Gtk.MenuItem(label='Quit')
        quit_item.connect('activate', self.quit)
        menu.append(quit_item)
        menu.show_all()

        self.ind.set_menu(menu)

        self.pulse = pulsectl.Pulse('mic-icon')

        GLib.timeout_add_seconds(1, self.update_icon)

    def update_icon(self):
        try:
            default_name = self.pulse.server_info().default_source_name
            source = self.pulse.get_source_by_name(default_name)
            muted = source.mute
        except Exception as e:
            muted = False

        icon = ICON_MUTED if muted else ICON_UNMUTED
        self.ind.set_icon_full(icon, icon)
        return True

    def quit(self, _):
        Gtk.main_quit()
        sys.exit(0)


if __name__ == "__main__":
    MicIcon()
    Gtk.main()
