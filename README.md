# LaSuite-Automations

With this folder structure you can then open the `docs/laSuiteAuto.code-workspace` workspace file with vscode to have all three folders open at once.
```
-LaSuite-Automations
-drive
-converstaions
```

> :warning: unauthenticated rate limit

You need to login to the podman cli, you can create a dockerhub account that then use that to login. If you auth with github for the account, on dockerhub there is a section to reset the password, do that so you can login after. 

```bash
podman login dockerhub.io
```

## Drive

[github.com/suitenumerique/drive](https://github.com/suitenumerique/drive)

Once cloned do a `make bootstrap`

You might need to modify a line the makefile to get postgres to launch

The compose command, right at the top of the file should be like this::w

```makefile
COMPOSE                 = docker compose
```

## Help launching Conversations

[github.com/suitenumerique/conversations](https://github.com/suitenumerique/conversations)

Once cloned do a `make build`

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