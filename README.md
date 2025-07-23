# Geometas
## Compile with Tailwindcss
`npm install`
`npx tailwindcss -i static/css/input.css -o static/css/main.css --watch`

## Sync DB structure & move images from airtable to S3
`python3 manage.py import_from_airtable`

...this command can be found under `/quiz/management/commands`.

## Run site locally
`python3 manage.py runserver`

## API
There is a simple API for fetching metas.

Country example: `GET https://geometas.com/api/metas/countries/germany`
Category example: `GET https://geometas.com/api/metas/categories/bollards`