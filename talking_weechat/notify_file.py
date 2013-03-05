# Author: Samuel Leathers <sbl5007@psu.edu>
# Version: 0.1
#
# Requires Weechat 0.3.0
# Released under GNU GPL v2
#

import weechat, string

weechat.register("notify_file", "disasm", "0.1", "GPL", "notify_file: writes highlights and priv msgs to file", "", "")

# script options
settings = {
    "show_hilights"             : "on",
    "show_priv_msg"             : "on",
    }


# Init everything
for option, default_value in settings.items():
  if weechat.config_get_plugin(option) == "":
    weechat.config_set_plugin(option, default_value)

# Hook privmsg/hilights
weechat.hook_print("", "irc_privmsg", "", 1, "notify_show", "")

# Functions
def notify_show(data, bufferp, uber_empty, tagsn, isdisplayed,
        ishilight, prefix, message):
    """Sends highlighted message to be printed on notification"""

    if (weechat.buffer_get_string(bufferp, "localvar_type") == "private" and
            weechat.config_get_plugin('show_priv_msg') == "on" and
            weechat.buffer_get_string(bufferp, "short_name") == prefix):
        write_notification(prefix, message)

    elif (ishilight == "1" and 
            weechat.config_get_plugin('show_hilights') == "on"):
        buffer = (weechat.buffer_get_string(bufferp, "short_name") or
                weechat.buffer_get_string(bufferp, "name"))
        write_notification(buffer,'(' + prefix + 
                weechat.config_get_plugin('nick_separator') + ') ' + message)

    return weechat.WEECHAT_RC_OK

def write_notification(channel,message):
  f = open('/home/disirc/.weechat/fnotify','a')
  if(channel == "private"):
    f.write(prefix + ' ' + message + "\n")
  else:
    f.write(channel + " " + message + "\n")
  f.close()
