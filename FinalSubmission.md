# Final Submission
## 1. Team
643645 Filippo Vimini
428514 Carl Bostrom
660835 Laxmi Thebe
## Features implemented **[Feature (points)] => description**
Let's describe the feature in more details :)
1. Authentication (200) => We implemented authentication using Django Auth - and
  email validation is required before the account is activated. We used SMTP for
  deployment whereas console for the test purpose. Third party login is developed
  and it currently works with Google - the only downfall of the solution at the
  moment is it keeps on asking to update either a user is a developer or a player
  which implies that a user can be both player and developer if he chooses once
  player and next developer (Many-To-Many between User Group relationship)
2. Basic Player Functionalities (300) => Basic player functionalities are
  implemented well - a user can play the game and save the state of the game or
  load the game. A game is only available for play once you purchase the game.
3. Basic Developer Functionalities (200) => A developer can upload a game - and
  he can play his own game as well.
4. Game/service interaction (200) => GameService interaction is fully implmeneted
  to our understanding. A user has to save the state manually though (when a user
  closes the browser tab, it does not  automatically save for example)
5. Quality of Work (90)
6. Non-functional requirements (175)
7. Save/load and resolution feature (100)
8. 3rd party login (100)
9. RESTful API (70)
10. Own Game (0)
11. Mobile Friendly(50)
12. Social Media Sharing (40) - Social Media sharing works and the detail of the
  games are posted as well.

## 3 Task Division
Task division was more about communication than planning after we decided how to
approach in the beginning. We used Slack for the communication. And discussed
our issue in the slack. For example, we proposed like - hey, I am now going to
implement this feature - and the person would be responsible for that feature.
There were some aspects we were more focused definitely as we found it easier to
proceed that way due to the difference on in what phase of the project we can
commit. For example, Filippo was traveling in the beginning of our start while
two other of us were on holiday and thought of spending on doing something. But,
still we managed to get ourselves involved in all technology stacks.
Was there any difficulties?
As a team, probably not really - because we were supporting each other and
communicating well. What one could not handle, could have been handled by another
member. But, personally, I think we had some problems though.

## Instructions to use app
1. Username for developer: gamehub_dev => **geoShip**
2. Username/Password for player: gamehub_player => **geoShip**
2. [Link to the game] (http://gamehub-aalto.herokuapp.com "GameHub@Heroku")
