# LaSuite-Automations

## Drive

[github.com/suitenumerique/drive](https://github.com/suitenumerique/drive)


## Help launching Conversations

[github.com/suitenumerique/conversations](https://github.com/suitenumerique/conversations)

To get it to build, you need to modify the compose.yml so it's cmpatible with podman, which we have on forty2 computers.

At the bottom of the `compose.yml` copypast this to include the default network, which apparently does not come with podman by default..

```
networks:
  default:
    driver: bridge

  lasuite:
    name: lasuite-network
    driver: bridge
```