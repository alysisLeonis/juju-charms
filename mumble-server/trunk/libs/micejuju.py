# Copyright 2012, Kees Cook <kees@ubuntu.com>
# License: GPLv3

# Return the channel name path for the given channel index.
def getChanNameByIndex(server, index):
    chans = server.getChannels()
    names = []
    while index != 0:
        names.append(chans[index].name)
        index = chans[index].parent
    names.reverse()

# Return the channel index that has the given name path.
def getChanIndexByName(server, name):
    chans = server.getChannels()
    if name == '':
        return 0
    if '/' in name:
        names = name.split('/')
    else:
        names = [name]
    parent = 0
    try:
        while len(names):
            name = names.pop(0)
            chan_id = dict()
            for index in chans:
                if chans[index].parent == parent:
                    chan_id.setdefault(chans[index].name, index)
            parent = chan_id[name]
    except:
        return None
    return parent

# Return the list of channel indexes that have a given parent.
def getChansByParent(server, index):
    chans = server.getChannels()
    return [x for x in chans if chans[x].parent == index]
