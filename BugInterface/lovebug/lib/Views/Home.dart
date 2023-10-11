import 'package:flutter/material.dart';
import 'package:flutter/rendering.dart';
import 'package:flutter/services.dart';
import 'package:provider/provider.dart'; // Import the provider package
import '../main.dart';
import 'package:lovebug/networking.dart' as networking;

class Home extends StatelessWidget {
  const Home({super.key});

  @override
  Widget build(BuildContext context) {
    return Column(crossAxisAlignment: CrossAxisAlignment.center, children: [
      const SizedBox(height: 10),
      Row(
        mainAxisAlignment: MainAxisAlignment.center,
        crossAxisAlignment: CrossAxisAlignment.center,
        mainAxisSize: MainAxisSize.max,
        children: [
          Container(
            margin: const EdgeInsets.all(10),
            padding: const EdgeInsets.all(10),
            width: 300,
            alignment: Alignment.center,
            decoration: BoxDecoration(
              color: Theme.of(context).colorScheme.primary,
              borderRadius: BorderRadius.circular(10),
            ),
            child: const Icon(Icons.home, size: 100),
          ),
        ],
      ),
      const Text('Feeling Here',textAlign: TextAlign.center,style: TextStyle(fontSize: 23)),
      const SizedBox(height: 5),
      Row(
        mainAxisAlignment: MainAxisAlignment.center,
        crossAxisAlignment: CrossAxisAlignment.center,
        mainAxisSize: MainAxisSize.max,
        children: [
          ElevatedButton(
            onPressed: () => {},
            child: const Text('Think', style: TextStyle(fontSize: 30)),
          ),
          const SizedBox(width: 10),
          ElevatedButton(
            onPressed: () => {networking.HTTP.get('/newLoad', context)},
            child: const Text('Love', style: TextStyle(fontSize: 30)),
          ),
          const SizedBox(width: 10),
          ElevatedButton(
            onPressed: () => {},
            child: const Text('Kiss', style: TextStyle(fontSize: 30)),
          ),
        ],
      ),
      const SizedBox(height: 20),
    ListView(
      shrinkWrap: true,
      padding: const EdgeInsets.all(8),
      children: [
        Container(
          decoration: BoxDecoration(
            border: Border.all(color: Theme.of(context).colorScheme.onPrimary),
            borderRadius: BorderRadius.circular(10),
            color: Theme.of(context).colorScheme.secondaryContainer,
          ),
          height: 50,
          child: Text('Entry A' ,textAlign: TextAlign.left  ,style: TextStyle(fontSize: 23)),
        ),
      ],
    ),
    ]);
  }
}
