
def configureCheck(components):
    comp = removeCommand(components)
    channel_type = ['text', 'voice']
    for i in comp:
        if(comp.index(i) == 0):
            if not(i == 'text' or i == 'voice'):
                return False
    return True


def removeCommand(components):
    comp = components[::-1]
    comp.pop()
    comp = comp[::-1]
    return comp

def retrieveServer(servers, channel):
    for i in servers:
        for j in i.channels:
            if j.id == channel.id:
                return i

def cleanID(iD):
    ID = list(iD)
    ID = ID[::-1]
    ID.pop()
    ID.pop()
    ID.pop()
    ID = ID[::-1]
    ID.pop()
    return "".join(ID)
