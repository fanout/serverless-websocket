# Serverless chat example

Run the backend:

```sh
$ stack chat-handler.py
```

Run pushpin:

```sh
$ pushpin -m --route "* localhost:3000,over_http"
```

Chat!

```sh
$ wscat -c ws://localhost:7999
connected (press CTRL+C to quit)
> hello
  < hello
```
