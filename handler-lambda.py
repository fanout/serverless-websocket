import os
from base64 import b64encode, b64decode
import json
from pubcontrol import Item
from gripcontrol import GripPubControl, WebSocketEvent, \
	WebSocketMessageFormat, parse_grip_uri, decode_websocket_events, \
	encode_websocket_events

pub = GripPubControl(parse_grip_uri(os.environ['GRIP_URL']))

def handle_events(events):
	opening = False
	out = []
	for e in events:
		if e.type == 'OPEN':
			if not opening:
				opening = True

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
			pub.publish('room', Item(WebSocketMessageFormat(e.content)),
					blocking=True)

	return out

def handler(event, context):
	if event['httpMethod'] == 'POST':
		# read body as binary
		if event.get('isBase64Encoded'):
			body = b64decode(event['body'])
		else:
			body = event['body']
		if isinstance(body, unicode):
			body = body.encode('utf-8')

		# decode events
		in_events = decode_websocket_events(body);

		# process events
		out_events = handle_events(in_events);

		# encode output events
		out_body = encode_websocket_events(out_events);

		resp = {
			'isBase64Encoded': True,
			'statusCode': 200,
			'headers': {
				'Content-Type': 'application/websocket-events',
				'Sec-WebSocket-Extensions': 'grip'
			},
			'body': b64encode(out_body)
		}
		return resp
	else:
		resp = {
			'isBase64Encoded': False,
			'statusCode': 405,
			'headers': {'Content-Type': 'text/plain'},
			'body': 'Method Not Allowed\n'
		}
		return resp
