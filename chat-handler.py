import sys
import json
from pubcontrol import Item
from gripcontrol import GripPubControl, WebSocketEvent, \
    WebSocketMessageFormat, decode_websocket_events, encode_websocket_events

pub = GripPubControl({'control_uri': 'http://localhost:5561'})

opening = False
out_headers = []
out = []
for e in decode_websocket_events(sys.stdin.read()):
    if e.type == 'OPEN':
        if not opening:
            opening = True

            # enable GRIP
            out_headers.append(('Sec-WebSocket-Extensions', 'grip'))

            # ack the open
            out.append(e)

            # subscribe connection to channel
            cm = {'type': 'subscribe', 'channel': 'room'}
            out.append(WebSocketEvent('TEXT', 'c:%s' % json.dumps(cm)))
    elif e.type == 'CLOSE':
        out.append(e) # ack
        break
    elif e.type == 'TEXT':
        # broadcast to everyone
        pub.publish('room', Item(WebSocketMessageFormat(e.content)))

out_headers.append(('Content-Type', 'application/websocket-events'))

for header in out_headers:
    cm = {
        'type': 'setHeader',
        'payload': {
            'name': header[0],
            'value': header[1]
        }
    }
    sys.stderr.write('%s\n' % json.dumps(cm))

sys.stdout.write(encode_websocket_events(out))
