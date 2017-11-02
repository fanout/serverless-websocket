# Serverless WebSocket example

This is an example of how to send and receive WebSocket messages using a serverless stack. The WebSocket connections are managed by a GRIP-compatible proxy such as Pushpin or Fanout Cloud, and the backend logic is handled by a function backend such as Microcule or AWS Lambda.

Any message sent from a client is relayed to all other connected clients.

## Setup using Pushpin and Microcule

Set up virtualenv:

```sh
$ virtualenv venv
$ . venv/bin/activate
$ pip install -r requirements.txt
```

Run the backend:

```sh
$ microcule handler.py
```

Run pushpin:

```sh
$ pushpin -m --route "* localhost:3000,over_http"
```

Connect:

```sh
$ wscat -c ws://localhost:7999
connected (press CTRL+C to quit)
> hello
  < hello
```

## Setup using Fanout Cloud and AWS Lambda

First create a realm in Fanout Cloud and note the realm ID and key.

Set up virtualenv:

```sh
$ virtualenv venv
$ . venv/bin/activate
$ pip install -r requirements.txt
```

Create the deployment package:

```sh
$ ./make-lambda-package.sh
```

Upload `lambda-package.zip` to AWS Lambda, using the Python 2.7 runtime, and `handler-lambda.handler` as the handler. Also, set the `GRIP_URL` environment variable containing Fanout Cloud settings, of the form:

```
https://api.fanout.io/realm/your-realm?iss=your-realm&key=base64:your-realm-key
```

Next, set up an API and resource in AWS API Gateway to point to the Lambda function, using a Lambda Proxy Integration, and add `application/websocket-events` as a Binary media type.

Finally, edit the Fanout Cloud domain origin server (SSL) to point to the host and port of the AWS API Gateway Invoke URL.

Connect:

```sh
$ wscat -c ws://{your-fanout-domain}/{your-api-gateway-path}/
connected (press CTRL+C to quit)
> hello
  < hello
```
