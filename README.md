# angelhack

A Telegram chat bot to interact with user, asking for their preferences to suggest travel destinations via Expedia's API.

### How it works

- User and bot greet each other
- Bot asks user for their location, which is obtained via a location-tag sent via Telegram (mobile)
- Bot asks for number of people, budget, departure date and durattion of stay
- Backend uses Expedia's API to fetch top 'X' cities (according to popularity of airports) for each continents, creating a common database. Then, features for each city are obtained (tourist spots worth visiting in that area, average hotel rating, duration of flight, savings on total cost, total cost of package).
- IBM Watson's Tradeoff Analytics API is used to find athe best possible travel destinations (with packages), which are displayed to the user for direct purchase.


### How to run it

- `python server.py` to run backgroundback0end server
- `python telegram_bot.py ` to run chat-bot (on same machine)
- Open Telegram on mobile on the same network, search for 'Angel hiraa bot' (or sth similar)
- Interact with the bot 
