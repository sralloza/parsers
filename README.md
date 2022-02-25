# Parsers

Finds new anime and manga chapters and sends a notification via telegram.

## Production

Required settings:

- `TELEGRAM_BOT_TOKEN`: telegram bot token to send telegram notifications.
- `TELEGRAM_CHAT_ID`: telegram chat id to send messages to.
- `S3_BUCKET_NAME`: AWS S3 bucket name to store the processed chapters.
- `AWS_ACCESS_KEY_ID`: AWS access key ID.
- `AWS_SECRET_ACCESS_KEY` AWS secret access key.

Optional settings:

- `MANGA_CONFIG_PATH`: full path to the `manga.json` file. Must be the container's path, not the host's path.
- `PARSE_ONE_PIECE_ANIME`: boolean, false by default. It enables the one piece anime parsing. **WARNING: one piece anime parsing is currently broken, do not enable it**.
- `TODOIST_TOKEN`: todoist token to enable todoist integration.
- `TODOIST_PROJECT_ID`: todoist project id.
- `TODOIST_DUE_STR`: string, `today` by default. Set the due string for the todoist tasks.

## Development

```shell
docker buildx build -t sralloza/parsers:2.0.1 --platform=linux/arm/v7,linux/amd64 --push .
```

To run:

```shell
docker run --env-file ENV_FILE --rm sralloza/parsers:2.0.1 parse
```

To parse mangas, create a file `mangas.json`:

```json
{
  "manga-name": "first-chapter-uuid"
}
```

Then launch the `docker run` command appending the `mangas.json` file as a volume. The `MANGA_CONFIG_PATH` environment variable must be set accordingly

**Note: the manga name in the json file must be written as lowercase without spaces. The name will be title-cased later.**

### AWS-cli utils

- Create bucket: `aws s3api create-bucket --bucket $BUCKET`
- Delete bucket: `aws s3api delete-bucket --bucket $BUCKET`
- List buckets: `aws s3api list-buckets`
- Show data in bucket: `aws s3api list-objects --bucket $BUCKET --query 'Contents[].{Key: Key, Size: Size}'`
- Remove file in bucket: `aws s3 rm s3://$BUCKET/$FILE`
- Download file from bucket: `aws s3 cp s3://$BUCKET/$FILE ./`
- Upload file to bucket: `aws s3 cp $FILE s3://$BUCKET/$FILE`
