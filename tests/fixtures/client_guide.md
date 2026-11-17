# positronic-platform-client

The client guide, cut to a fixture.

## Registering

```bash
platform-register --alias=<display name>
```

## Eval plans

[Submit a policy image](../docs/submit-a-policy-image.md) says what the image serves.
[Registering](#registering) comes first. [PyPI](https://pypi.org/project/positronic/) has the package.

| Status | Fault |
|---|---|
| 1 | the caller |

## From the command line

```bash
platform-register --alias=<display name>            # in a checkout: uv run platform-register
uv run positronic eval run --eval=<name> --policy-image=org/policy@sha256:…
uv run positronic eval status --id=<hex id>
```
