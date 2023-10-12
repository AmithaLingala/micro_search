# micro search

A self-hostable search engine for sites supporting microformats2

## How to use?

This service exposes two api endpoints
1. `/crawl` -> This is a `PUT` request that indexes all sites defined in the environment file.
2. `/search` -> This is a `GET` request that takes two parameters `query` and `site`.
    1. The parameter `query` is mandatory, not providing a query will return an empty result.
    2. `site` the site url, you could also provide some arbitary text here, this will match all urls containing the provided the text.

### Example

```sh
curl -X PUT http://localhost:8000/crawl # crawls all sites defined in the .env file
curl http://localhost:8000/search?query=example # Search for a text

curl http://localhost:8000/search?query=example&site=example.com # Search for a text in example.com

```

## How to run?

1. Clone this repository
2. Copy the `env.sample` to a file named `.env`
3. Edit the newly created `.env` file and add the sites you want to index in the `SITES` variable.
4. If you want to crawl multiple sites, seperate them with commas (`SITES=https://example.com,https://anotherexample.com`)
5. Create a new python virtual environment and activate it (`python3 -m venv .venv && source .venv/bin/activate`)
6. Install all requirements (`pip install -r Requirements.txt`)
7. Run the program `flask --app micro_search run`
8. profit!
