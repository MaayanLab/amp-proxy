# Ma'ayan Lab HAProxy

### Introduction

This project has two main components:

1. An HAProxy server that is responsible for routing all requests from `http://amp.pharm.mssm.edu/` to the correct web applications.

2. A small web server that dynamically rebuilds the [HAProxy](http://www.haproxy.org/) configuration file and restarts HAProxy using the [Marathon](https://mesosphere.github.io/marathon/) API.

### HAProxy

There is not much a developer must know about the HAProxy component. The `Dockerfile` uses the latest HAProxy image, and we start HAProxy using MHW. Specifically, in the `haproxy` module, there is a function called `reload` that handles building the HAProxy configuration file and then starting HAProxy. This application must run port `80` on `charlotte`.

### Marathon-HAProxy webhook

This component is responsible for responding to Marathon updates, rebuilding the configuration file, and then restarting HAProxy. It runs in the same Docker container as HAProxy so that it can easily reconfigure and restart the proxy server. This application listens on port `52496`, which is not exposed. **_Do not confuse HAProxy with the Marathon-HAProxy web hook. They are two separate servers. HAProxy listens on port 80. The Marathon-HAProxy webhook listens on port 52496._**

To see the current HAPRoxy configuration, go to: [http://charlotte:52496/marathon-haproxy-webhook](http://charlotte:52496/marathon-haproxy-webhook). This GET request should only work if you have the correct hosts file mapping for `charlotte`.

Importantly, we use the [Marathon Event Bus](https://mesosphere.github.io/marathon/docs/event-bus.html). Marathon allows developers to register a callback endpoint to which Marathon will POST events in JSON format. To see the list of currently registered callbacks, go to: [http://elizabeth:8080/v2/eventSubscriptions](http://elizabeth:8080/v2/eventSubscriptions). To register a new callback, see the `eventSubscriptions` endpoint in the [Marathon API documentation](https://mesosphere.github.io/marathon/docs/generated/api.html).