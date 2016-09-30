### API docs

endpoint: `https://seed-project-v1.appspot.com/api/v1`
all json except `/images`

#users:
`POST /users`
params:  email, password

`GET /users/{id}`

#tokens:
`POST /tokens`
params: email, password
set the token to header with X-WALKER-ACCESS-TOKEN

#images:
`POST /images`
params: image
