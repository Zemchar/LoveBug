import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:provider/provider.dart'; // Import the provider package
import 'package:shared_preferences/shared_preferences.dart';
import '../main.dart';
import "dart:math";
import 'package:lovebug/networking.dart' as networking;

// Games Page
class Games extends StatefulWidget {
  const Games({super.key});

  @override
  State<Games> createState() => _GamesState();
}

class _GamesState extends State<Games> {
  var currentGame = null;
  var prefs;
  late final Future popGame = populateGames();
  late List<Game> games = [];
  var gameImage;

  Future<List<Game>> populateGames() async {
    await setupPrefs();
    games;
    var finalRes;
    var res = await networking.Steam.getGameInfo(prefs.getString("steamAPIKey"),
        prefs.get("steamID"), context); // this should never fail
    try {
      var res2 = await networking.Steam.getGameInfo(
          prefs.getString("steamAPIKey"),
          prefs.get("partnerSteamID") ?? prefs.getString("steamID"),
          context);
      finalRes = await networking.Steam.intersection(res, res2);
    } catch (e) {
      showDialog<void>(
          context: context,
          barrierDismissible: false, // user must tap button!
          builder: (BuildContext context) {
            return AlertDialog(
                title: const Text('Steam Did not Respond'),
                content: SingleChildScrollView(
                    child: ListBody(children: <Widget>[
                  Text('Request failed when retrieving partner\'s games!'),
                  Text(
                      'You may still use this page as normal, but the games avaialble to you will not be filtered by your partner\'s games.'),
                  Text(
                      'You are most likely rate-limited. Try again in a few minutes.'),
                  Text('\nFULL ERROR: \n' + e.toString()),
                ])),
                actions: <Widget>[
                  TextButton(
                      child: const Text('OK'),
                      onPressed: () {
                        Navigator.of(context).pop();
                      }),
                ]);
          });
      finalRes = res;
    }
    //TODO: Maybe sort the output?
    for (var game in finalRes) {
      if (game['playtime_forever'] <= 0) {
        continue;
      }
      games.add(Game(game['name'], game['appid']));
    }
    if (currentGame != null) {
      gameImage = networking.Steam.getGameImage(currentGame.steamID);
    } else {
      gameImage = networking.Steam.getGameImage(games[0].steamID);
    }
    return games;
  }

  Future<Map<String, Object>> setupPrefs() async {
    prefs = await SharedPreferences.getInstance();
    Map<String, Object> data = {};
    for (String key in prefs.getKeys()) {
      data[key] = prefs.get(key)!;
    }
    return data;
  }

  @override
  void initState() {
    super.initState();
    WidgetsBinding.instance!.addPostFrameCallback((_) async {
      await setupPrefs();
    });
  }

  @override
  Widget build(BuildContext context) => FutureBuilder(
      future: popGame, // so we avoid getting rate-limited
      builder: (BuildContext context, AsyncSnapshot snapshot) {
        if (snapshot.hasData) {
          return Center(
              child: Column(children: [
            Container(
              margin: const EdgeInsets.all(10),
              padding: const EdgeInsets.all(10),
              height: 150,
              decoration: BoxDecoration(
                color: Theme.of(context).colorScheme.primary,
                borderRadius: BorderRadius.circular(10),
              ),
              child: gameImage ?? CircularProgressIndicator(),
            ),
            Container(
                margin: const EdgeInsets.all(10),
                padding: const EdgeInsets.all(10),
                width: 300,
                decoration: BoxDecoration(
                  border: Border.all(
                      color: Theme.of(context).colorScheme.onPrimary),
                  borderRadius: BorderRadius.circular(10),
                ),
                child: DropdownButtonHideUnderline(
                    child: DropdownButton<Game>(
                        value: (currentGame != null) ? currentGame : games[0],
                        icon: const Icon(Icons.games),
                        iconSize: 24,
                        elevation: 16,
                        isExpanded: true,
                        onChanged: (Game? newValue) {
                          currentGame = newValue!;
                          gameImage =
                              networking.Steam.getGameImage(newValue.steamID);
                          setState(() {
                            currentGame;
                          });
                        },
                        items: games.map<DropdownMenuItem<Game>>((Game value) {
                          return DropdownMenuItem<Game>(
                            value: value,
                            child: Center(
                                child: Text(value.name,
                                    style: TextStyle(
                                        fontSize: 20, color: Colors.black),
                                    textAlign: TextAlign.center)),
                          );
                        }).toList()))),
            Text("Or enter a custom game", style: TextStyle(fontSize: 20)),
            Container(
              margin: const EdgeInsets.all(10),
              padding: const EdgeInsets.all(10),
              decoration: BoxDecoration(
                color: Theme.of(context).colorScheme.secondaryContainer,
                borderRadius: BorderRadius.circular(10),
              ),
              child: const TextField(
                decoration: InputDecoration(
                  border: OutlineInputBorder(),
                  labelText: 'Custom Game',
                ),
              ),
            ),
            ButtonBar(
              alignment: MainAxisAlignment.center,
              children: [
                ElevatedButton(
                  onPressed: () {
                    var random = new Random();
                    currentGame = games[random.nextInt(games.length)];
                    gameImage =
                        networking.Steam.getGameImage(currentGame.steamID);
                    setState(() {
                      currentGame;
                      gameImage;
                    });
                  },
                  child:
                      const Text('Randomize', style: TextStyle(fontSize: 30)),
                ),
                ElevatedButton(
                  onPressed: () {
                    if (networking.RTC.isReady()) {
                      networking.RTC.send(currentGame.name);
                    }else{
                      networking.RTC.connect();
                    }
                  },
                  child: const Text('Submit', style: TextStyle(fontSize: 30)),
                ),
              ],
            ),
          ]));
          ;
        } else if (snapshot.hasError) {
          return Icon(Icons.error_outline);
        } else {
          return Center(child: CircularProgressIndicator());
        }
      });
}

class Game {
  String name;
  int steamID;
  Game(this.name, this.steamID);

  @override
  String toString() {
    return name;
  }

  static Game defaultGame() {
    return new Game('default', 0);
  }
}
