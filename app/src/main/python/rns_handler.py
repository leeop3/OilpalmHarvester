import reticulum as RNS
import lxmf

identity = None
destination = None

def init_rns():
    global identity, destination
    RNS.Reticulum()
    identity = RNS.Identity()
    destination = lxmf.LXMFDestination(identity, app_name="PalmHarvester")

def send_lxmf(csv_payload):
    global identity, destination
    if identity is None: init_rns()
    message = lxmf.LXMessage(source=identity, destination=destination, content=csv_payload, fields=lxmf.LXMessage.TEXT_FIELD)
    message.sign()
    RNS.Transport.send(message)
    print(f"Message Sent: {csv_payload[:20]}...")
    return True