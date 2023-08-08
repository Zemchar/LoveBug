# LoveBug
A little app for long distance lovers

# Anatomy
This app comprises of two different projects: [BugCore](#bugcore) and [BugNest](#bugnest)

## BugNest
This is the server component of this project. 

It provides both a static, webserver-like connection as well as a websocket for realtime interaction

Why do it this way? It seemed kinda fun to do both

You may configure the server in the "[appsettings.json](/BugNest/appsettings.json)" file 

### Configuration Options
| Option        | Description                                                                                           | Notes                                                                                                                                                                                                                                    |
|---------------|-------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Host          | The ip address the server will listen on  This also affects websockets                                | Use 0.0.0.0 for running inside a docker container                                                                                                                                                                                        |
| Method        | The method the server uses to listen (http or https)                                                  |                                                                                                                                                                                                                                          |
| Ports         | StaticApp - This is the port for the static webserver  WebSocket - This is the port for the Websocket | I recommend binding port 80 to whatever port you set for the staticapp value when running under docker, so users dont have to specify a port --- The users of your server never have to provide the websocket port, only the staticapp port |
| DB - Host     | The server that the database is running on                                                            | If running your db under docker, use the name of the service as outlined in the docker-compose file                                                                                                                                      |
| DB - User     | The user that you wish to connect to the DB as                                                        |                                                                                                                                                                                                                                          |
| DB - Password | The password for the user                                                                             |                                                                                                                                                                                                                                          |
| DB - Database | The database you would like to use                                                                    |                                                                                                                                                                                                                                          |
### API Endpoints
| Endpoint        | Description                                                                                  |
|-----------------|----------------------------------------------------------------------------------------------|
| newLoad         | Used to pull down all missed messages since last app launch, as well as update user profiles |
| resource - GET  | Used to get server-configured image files such as the image for a custom game                |
| resource - POST | Used for users to upload new profile pictures                                                |
| reqWS           | Returns info for connecting to the websocket, such as the port                               |

## BugCore
Bug core is the main user application. Mostly everything auto-configures itself on first startup. 

Partners only need to exchange BugCodes on the server they are connecting to to be connected.
