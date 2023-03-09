## Backend Worker


Build 

`
docker build -t backend-worker .
`

Run dev

`
docker run -p 8000:80 backend-worker
`

Run prod

`
docker run -dp 8000:80 backend-worker
`