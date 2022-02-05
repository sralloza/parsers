# Parsers

Finds new anime and manga chapters and sends a notification via telegram.

## Docker

```shell
docker buildx build -t sralloza/parsers:2.0.0 --platform=linux/arm/v7,linux/amd64 --push .
```

To run:

```shell
docker run --env-file ENV_FILE --rm sralloza/parsers:2.0.0 parse
```

Remember to add `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` env vars.
