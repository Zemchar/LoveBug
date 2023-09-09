import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:provider/provider.dart'; // Import the provider package
import '../main.dart';
import "dart:math";


// Games Page
class Games extends StatefulWidget {
  const Games({super.key});

  @override
  State<Games> createState() => _GamesState();

}
class _GamesState extends State<Games>{
  List<Game> games = [
    new Game('test2', 1),
    new Game('test3', 2),
    new Game('test4', 3),
    new Game('test5', 4),];
  var currentGame = null;

  @override
  Widget build(BuildContext context) {
    return Center(
      child: Column(
        children: [
          Container(
            margin: const EdgeInsets.all(10),
            padding: const EdgeInsets.all(10),
            decoration: BoxDecoration(
              color: Theme.of(context).colorScheme.primary,
              borderRadius: BorderRadius.circular(10),
            ),
          //TODO: Change to icon
          child: const Icon(Icons.gamepad, size: 100),
          ),
          Container(
            margin: const EdgeInsets.all(10),
            padding: const EdgeInsets.all(10),
            width: 300,
            decoration: BoxDecoration(
              border: Border.all(color: Theme.of(context).colorScheme.onPrimary),
              borderRadius: BorderRadius.circular(10),
            ),
            child: DropdownButtonHideUnderline(child: DropdownButton<Game>(
              value: (currentGame != null ) ? currentGame : games[0],
              icon: const Icon(Icons.games),
              iconSize: 24,
              elevation: 16,
                isExpanded: true,
              onChanged: (Game? newValue) {
                currentGame = newValue!;
                //TODO: Pull data from steam
                print(currentGame);
                setState(() {
                  currentGame;
                });
              },
              items: games.map<DropdownMenuItem<Game>>((Game value) {
                return DropdownMenuItem<Game>(
                  value: value,
                  child: Center(child: Text(value.name, style: TextStyle(fontSize: 20, color: Colors.black), textAlign: TextAlign.center)),
                );
              }).toList()
            ))
          ),
          Text("Or enter a custom game", style: TextStyle(fontSize: 20)),
          Container(
            margin: const EdgeInsets.all(10),
            padding: const EdgeInsets.all(10),
            decoration: BoxDecoration(
              color: Theme.of(context).colorScheme.primary,
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
                  print(currentGame);
                  setState(() {
                    currentGame;
                  });
                },
                child: const Text('Randomize', style: TextStyle(fontSize: 30)),
              ),
              ElevatedButton(
                onPressed: () {
                  print('Submit');
                },
                child: const Text('Submit', style: TextStyle(fontSize: 30)),
              ),
            ],
          ),
    ]));
  }
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