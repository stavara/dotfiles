# Copyright (c) 2010 Aldo Cortesi
# Copyright (c) 2010, 2014 dequis
# Copyright (c) 2012 Randall Ma
# Copyright (c) 2012-2014 Tycho Andersen
# Copyright (c) 2012 Craig Barnes
# Copyright (c) 2013 horsik
# Copyright (c) 2013 Tao Sauvage
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import os
import subprocess
from libqtile import hook

# custom cmus
from functools import partial
from libqtile import pangocffi
from libqtile.widget import base

class Cmus(base.ThreadPoolText):

    defaults = [
        ("play_color", "fc5f5c", "Text colour when playing."),
        ("noplay_color", "6e7072", "Text colour when not playing."),
        ("update_interval", 0.5, "Update Time in seconds."),
    ]

    def __init__(self, **config):
        base.ThreadPoolText.__init__(self, "", **config)
        self.add_defaults(Cmus.defaults)
        self.status = ""
        self.local = None

        self.add_callbacks(
            {
                "Button1": self.play,
                "Button4": partial(subprocess.Popen, ["cmus-remote", "-n"]),
                "Button5": partial(subprocess.Popen, ["cmus-remote", "-r"]),
            }
        )

    def get_info(self):
        """Return a dictionary with info about the current cmus status."""
        try:
            output = self.call_process(["cmus-remote", "-C", "status"])
        except subprocess.CalledProcessError as err:
            output = err.output
        if output.startswith("status"):
            output = output.splitlines()
            info = {
                "status": "",
                "file": "",
                "artist": "",
                "album": "",
                "title": "",
                "stream": "",
            }

            for line in output:
                for data in info:
                    if data in line:
                        index = line.index(data)
                        if index < 5:
                            info[data] = line[len(data) + index :].strip()
                            break
                    elif line.startswith("set"):
                        return info
            return info

    def now_playing(self):
        """Return a string with the now playing info (Artist - Song Title)."""
        info = self.get_info()
        now_playing = ""
        if info:
            status = info["status"]
            if self.status != status:
                self.status = status
                if self.status == "playing":
                    self.layout.colour = self.play_color
                else:
                    self.layout.colour = self.noplay_color
            self.local = info["file"].startswith("/")
            title = info["title"]
            if self.local:
                artist = info["artist"]
                now_playing = "{0} - {1}".format(artist, title)
                if now_playing == " - ":
                    file_path = info["file"]
                    file_path = file_path.split("/")[-1]
                    now_playing = file_path
            else:
                if info["stream"]:
                    now_playing = info["stream"]
                else:
                    now_playing = title
            if now_playing:
                now_playing = "{0}".format(now_playing)
        return pangocffi.markup_escape_text(now_playing)

    def play(self):
        """Play music if stopped, else toggle pause."""
        if self.status in ("playing", "paused"):
            subprocess.Popen(["cmus-remote", "-u"])
        elif self.status == "stopped":
            subprocess.Popen(["cmus-remote", "-p"])

    def poll(self):
        """Poll content for the text box."""
        return self.now_playing()

#


from libqtile import bar, layout, widget
from libqtile.config import Click, Drag, Group, Key, Match, Screen, ScratchPad, DropDown
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal

from libqtile import qtile


#custom imports





def whereScreen(qtile, group_name):                                                
    if group_name  == qtile.current_screen.group.name:                                
        qtile.current_screen.set_group(qtile.current_screen.previous_group)     
        return                                                                  
    for i, group in enumerate(qtile.groups):                                    
        if group_name == group.name:                                            
            qtile.current_screen.set_group(qtile.groups[i])                     
            return 

mod = "mod4"
terminal = "alacritty"

# Mis configuraciones

colorTaskBarQtile = "#161616"
sizeBarQtile = 38
fontQtile = "Caskaydia Cove Nerd Font"
fontSizeQtile = 18

keys = [
    # A list of available commands that can be bound to keys can be found
    # at https://docs.qtile.org/en/latest/manual/config/lazy.html
    # Switch between windows
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    # Key([mod], "space", lazy.layout.next(), desc="Move window focus to other window"),
    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key([mod, "shift"], "h", lazy.layout.shuffle_left(), desc="Move window to the left"),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right(), desc="Move window to the right"),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),
    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key([mod, "control"], "h", lazy.layout.grow_left(), desc="Grow window to the left"),
    Key([mod, "control"], "l", lazy.layout.grow_right(), desc="Grow window to the right"),
    Key([mod, "control"], "j", lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),   
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),
    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key(
        [mod],
        "space",
        lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack",
    ),
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),
    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "w", lazy.window.kill(), desc="Kill focused window"),
    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    Key([mod], "r", lazy.spawncmd(), desc="Spawn a command using a prompt widget"),
    # Menu
    Key([mod], "m", lazy.spawn("rofi -show run"), desc="Launch rofi"),
    Key([mod, "shift"], "m", lazy.spawn("rofi -show"), desc="Launch rofi windows"),
    Key([mod], "b", lazy.spawn("firefox"), desc="Launch firefox"),
    Key([mod], "e", lazy.spawn("thunar"), desc="Launch thunar"),
    Key([], "XF86AudioLowerVolume", lazy.spawn("pactl set-sink-volume @DEFAULT_SINK@ -5%")),
    Key([], "XF86AudioRaiseVolume", lazy.spawn("pactl set-sink-volume @DEFAULT_SINK@ +5%")),
    Key([], "XF86AudioMute", lazy.spawn("pactl set-sink-mute @DEFAULT_SINK@ toggle")),
    Key([mod], "s", lazy.spawn("scrot")),
    Key([mod, "shift"], "s", lazy.spawn("scrot -s")),
    Key([mod, "shift"], "f", lazy.window.toggle_floating()),
    Key([mod], "t", lazy.spawn(os.path.expanduser("~/.config/qtile/toggleKeyMaps.sh"))),
]

#groups = [Group(i) for i in [
#   "www", "dev", "doc", "file", "sys", "ost", "misc",
#]] Da igual si es asi o como abajo el loop funciona igual Xephyr

groups = [
    Group("www", matches=[Match(wm_class=['firefox'])], layout="max"),
    Group("dev", matches=[Match(wm_class=['code-oss'])], layout="monadtall"),
    Group("doc", matches=[Match(wm_class=['Zathura'])], layout="monadtall"),
    Group("file", matches=[Match(wm_class=['Thunar'])], layout="monadtall"),
    Group("sys", layout="monadtall"),
    Group("ost", spawn=[], layout="monadtall"),
    Group("misc", matches=[Match(wm_class=['Xephyr'])], layout="monadwide"),
]

groups.append(ScratchPad('dev_scratch', [
    DropDown('term', terminal, width=0.4, height=0.5, x=0.3, y=0.2, opacity=1),
    DropDown('expl', 'thunar', width=0.4, height=0.5, x=0.3, y=0.2, opacity=1),
]))

keys.extend([
    Key(["control"], "1", lazy.group['dev_scratch'].dropdown_toggle('term')),
    Key(["control"], "2", lazy.group['dev_scratch'].dropdown_toggle('expl')),
])

for i, group in enumerate(groups):
    zoneWork = str(i+1)
    keys.extend(
        [
            # mod1 + letter of group = switch to group
            Key(
                [mod],
                zoneWork,
                lazy.function(whereScreen, group.name),
                desc="Switch to group {}".format(group.name),
            ),
            # mod1 + shift + letter of group = switch to & move focused window to group
            Key(
                [mod, "shift"],
                zoneWork,
                lazy.window.togroup(group.name, switch_group=True),
                desc="Switch to & move focused window to group {}".format(group.name),
            ),
            # Or, use below if you prefer not to switch to that group.
            # # mod1 + shift + letter of group = move focused window to group
            # Key([mod, "shift"], i.name, lazy.window.togroup(i.name),
            #     desc="move focused window to group {}".format(i.name)),
        ]
    )

layout_conf = {
    'border_focus': '#d5d0c2',
    'border_normal': '#282828',
    'border_width': 3,
    'margin': 14,
}

layouts = [
    # layout.Columns(border_focus_stack=["#d75f5f", "#8f3d3d"], border_width=1),
    layout.Max(),
    # Try more layouts by unleashing below layouts.
    layout.Stack(num_stacks=2),
    layout.Bsp(**layout_conf),
    layout.Matrix(**layout_conf),
    layout.MonadTall(**layout_conf),
    layout.MonadWide(**layout_conf),
    # layout.RatioTile(),
    # layout.Tile(),
    # layout.TreeTab(),
    # layout.VerticalTile(),
    # layout.Zoomy(),
]

widget_defaults = dict(
    font= fontQtile,
    fontsize= fontSizeQtile,
    padding= 0,
)
extension_defaults = widget_defaults.copy()

# this_screen_border=value


# mouse callbacks

def toggleFunction():
    keymaps = os.path.expanduser('~/.config/qtile/toggleKeyMaps.sh')
    subprocess.run([keymaps])

screens = [
    Screen(
        top=bar.Bar(
            [   
                widget.Sep(
                    linewidth=0,
                    padding=10,
                ),
                widget.GroupBox(
                    active="4fcaee",
                    inactive="6e7073",
                    borderwidth=3,
                    highlight_method="text",
                    this_current_screen_border="ffc366",
                    margin_x=0,
                    padding_x=3,
                    disable_drag=True,
                ),
                widget.Prompt(),
                widget.TextBox(
                    text="| ",
                    fontsize=15,
                    padding=0,
                    foreground="ffffff",
                ),
                widget.CurrentLayout(
                    foreground="ffc366",
                ),
                widget.Sep(
                    linewidth=0,
                    padding=50,
                ),
                widget.WindowName(
                    foreground="a6e02e",
                    max_chars = 20,
                ),
		Cmus(
	            fmt=" {}",
		    fontsize=18,
	            max_chars=20,
                ),
                widget.TextBox(
                    text="  墳 ",
                    fontsize=18,
                    padding=0,
                    foreground="6e7073",
                ),
                widget.Volume(
                    foreground="ffc366",
                ),
                widget.TextBox(
                    text="   ",
                    fontsize=18,
                    padding=0,
                    foreground="6e7073",
                    mouse_callbacks={'Button1': toggleFunction},
                ),
                widget.KeyboardLayout(
                    foreground="ffc366",
                    padding=10,
                    mouse_callbacks={'Button1': toggleFunction},
                ),
                widget.TextBox(
                    text="  ",
                    fontsize=18,
                    padding=0,
                    foreground="6e7073",
                ),
                widget.Clock(
                    format="%a, %b %d %H:%M ",
                    foreground="ffc366",
                ),
                widget.Sep(
                    linewidth=0,
                    padding=10,
                ),
            ],
            sizeBarQtile,
            background=colorTaskBarQtile,
        ),
    ),
]

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(
    border_focus="a9b665",
    border_normal="#000000",
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry
    ]
)
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# When using the Wayland backend, this can be used to configure input devices.
wl_input_rules = None

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"

@hook.subscribe.startup_once
def autostart():
    home = os.path.expanduser('~/.config/qtile/autostart.sh')
    subprocess.Popen([home])

@hook.subscribe.startup_complete    
def changeStartGroup():
    qtile.current_screen.set_group(qtile.groups[1])
