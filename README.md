# Fastapi-blogApp
Fastapi + MongoDB

Hosted on azure
### http://20.246.225.249/docs

## Authentication API
/auth/register - Create account with username, email and password

/auth/login - Login with username and password -> returns jwt encoded access_token

## User API
/users (get) - retrieve all users  default offset: 0  and limit: 10

/users/{id} (get) - retrieve user by id

## Post API
/posts(get) - get all posts with default offset: 0  and limit: 10

/posts/(post) - create post with title and content

/posts/{id} (get) - get post by id

/posts/{id} (update) - user can update their post using post id

/post/{id}  (delete) - user can delete their post using post id

## Comment API
/posts/{id}/comments - (get) get all comments on post using post id

/posts/{id}/comments - (post) to add comment on post using post id