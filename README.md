# Retraction dashboard
Keep track of retracted scientific publications in a dashboard.

## Requirements
- docker

## Installation

1. Clone the repository locally
`git clone https://github.com/rcortini/retraction-dashboard.git`

2. Set up your environment. Copy the `.env.example` to a `.env` file
`cp .env.example .env`

3. Get an OpenAlex API key (see [documentation](https://developers.openalex.org/guides/authentication)) and set it in the `OA_API_KEY` environment variable in your `.env` file

4. Run
`docker compose up --build`
to build the project. This step will initialize the database of retracted papers, so the first time you will run it it will take some time to execute.

5. Then point your browser to `localhost:8541` and enjoy the dashboard.