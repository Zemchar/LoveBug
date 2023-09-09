import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:provider/provider.dart'; // Import the provider package
void main() {
  runApp(ChangeNotifierProvider(
    create: (_) => ThemeProvider(),
    child: MyApp(),
  ));
}
class ThemeProvider extends ChangeNotifier {
  Color currentTheme = Colors.pink;

  void changeTheme(Color newTheme) {
    currentTheme = newTheme;
    notifyListeners(); // Notify listeners of the change
  }
}

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    final themeProvider = Provider.of<ThemeProvider>(context);

    return MaterialApp(
      title: 'Love Bug',
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: themeProvider.currentTheme),
        useMaterial3: true,
      ),
      home: MainPage(title: 'Love Bug'),
    );
  }
}



mixin theming {
  static Color currentTheme = Colors.pink;
  static var themeMapping = {
    'Pink': Colors.pink,
    'Green': Colors.green,
    'Blue': Colors.blue,
    'Purple': Colors.purple,
    'Orange': Colors.orange,
    'Red': Colors.red,
  };
  static String currentThemeName = 'Pink';
}

// Main Page
class MainPage extends StatefulWidget {
  const MainPage({super.key, required this.title});

  final String title;

  @override
  State<MainPage> createState() => _MainPageState();
}

class _MainPageState extends State<MainPage> {
  final List<Widget> _children = [
    const Home(),
    const Games(),
    const Gallery(),
    Settings()
  ];
  int _index =
      0; // Make sure this is outside build(), otherwise every setState will change the value back to 0

  @override
  @mustCallSuper
  void initState() {
    print('MainPage InitState');
    super.initState();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
        appBar: AppBar(
          title: const Text('Love Bug'),
          centerTitle: true,
          backgroundColor: Theme.of(context).colorScheme.inversePrimary,
        ),
        body: _children[_index],
        bottomNavigationBar: BottomNavigationBar(
            onTap: (tappedItemIndex) => setState(() {
                  _index = tappedItemIndex;
                }),
            currentIndex: _index,
            items: [
              BottomNavigationBarItem(
                  icon: const Icon(Icons.home_outlined),
                  label: 'Home',
                  backgroundColor: Theme.of(context).colorScheme.scrim),
              BottomNavigationBarItem(
                  icon: const Icon(Icons.gamepad_outlined),
                  label: 'Games',
                  backgroundColor: Theme.of(context).colorScheme.scrim),
              BottomNavigationBarItem(
                  icon: const Icon(Icons.photo_album_outlined),
                  label: 'Gallery',
                  backgroundColor: Theme.of(context).colorScheme.scrim),
              BottomNavigationBarItem(
                  icon: const Icon(Icons.settings_outlined),
                  label: 'Settings',
                  backgroundColor: Theme.of(context).colorScheme.scrim),
            ]));
  }
}

// Home Page
class Home extends StatelessWidget {
  const Home({super.key});

  @override
  Widget build(BuildContext context) {
    return Center(
      child: Container(
        margin: const EdgeInsets.all(10),
        padding: const EdgeInsets.all(10),
        decoration: BoxDecoration(
          color: Theme.of(context).colorScheme.primary,
          borderRadius: BorderRadius.circular(10),
        ),
        child: const Text('Home Page'),
      ),
    );
  }
}

// Games Page
class Games extends StatelessWidget {
  const Games({super.key});

  @override
  Widget build(BuildContext context) {
    return const Center(
      child: Text('Games Page'),
    );
  }
}

// Gallery Page
class Gallery extends StatelessWidget {
  const Gallery({super.key});

  @override
  Widget build(BuildContext context) {
    return const Center(
      child: Text('Gallery Page'),
    );
  }
}

// Settings Page
class Settings extends StatefulWidget {
  Settings({super.key});
  @override
  State<Settings> createState() => _SettingsState();
}

class _SettingsState extends State<Settings> {
  String _notifBoxValue = 'On';
  final TextEditingController _nameController = TextEditingController();
  late ThemeProvider themeProvider; // Declare a ThemeProvider variable

  @override
  void didChangeDependencies() {
    super.didChangeDependencies();

    // Access the ThemeProvider using the context provided by the build method
    themeProvider = Provider.of<ThemeProvider>(context);
  }


  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(20),
        child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            mainAxisAlignment: MainAxisAlignment.spaceEvenly,
          children: [
            Align(
              alignment: Alignment.center,
              child: Text('Your Bug Code: ${_BugCode.BugCode}', style: TextStyle(fontSize: 20)),
            ),
            const SizedBox(height: 20),
            Row(
              crossAxisAlignment: CrossAxisAlignment.center,
              mainAxisAlignment: MainAxisAlignment.end,
              children: [
                const Text('Notifications', style: TextStyle(fontSize: 30)),
                SizedBox(width: 20),
                SizedBox(width: 250, height: 70, child:
                InputDecorator(
                    decoration: InputDecoration(
                      border:
                      OutlineInputBorder(borderRadius: BorderRadius.circular(5.0)),
                    ), child:
                DropdownButtonHideUnderline(
                  child: DropdownButton<String>(
                    icon: const Icon(Icons.notifications_active_outlined),
                    value: _notifBoxValue,
                    onChanged: (String? newValue) {
                      print(newValue);
                      _notifBoxValue = newValue!;
                      setState(() {
                        _notifBoxValue;
                      });
                    },
                    items: <String>['On', 'Off']
                        .map<DropdownMenuItem<String>>((String value) {
                      return DropdownMenuItem<String>(
                        value: value,
                        child:
                            Text(value, style: const TextStyle(fontSize: 20)),
                      );
                    }).toList(),
                  ),
                ))),
                ],),
            const SizedBox(height: 20),
            Row(
              crossAxisAlignment: CrossAxisAlignment.center,
              mainAxisAlignment: MainAxisAlignment.end,
              children: [
                const Text('Theme', style: TextStyle(fontSize: 30)),
                SizedBox(width: 20),
                SizedBox(width: 250, height: 70, child:
                InputDecorator(
                    decoration: InputDecoration(
                      border:
                      OutlineInputBorder(borderRadius: BorderRadius.circular(5.0)),
                    ), child:
                DropdownButtonHideUnderline(
                  child: DropdownButton<String>(
                    icon: const Icon(Icons.notifications_active_outlined),
                    value: theming.currentThemeName,
                    onChanged: (String? newValue) {
                      theming.currentTheme = theming.themeMapping[newValue!]!;
                      theming.currentThemeName = newValue;
                      setState(() {
                        theming.currentTheme;
                        theming.currentThemeName;
                      });
                      themeProvider.changeTheme(theming.currentTheme);
                    },
                    items: <String>['Pink', 'Green', 'Blue', 'Purple', 'Orange', 'Red']
                        .map<DropdownMenuItem<String>>((String value) {
                      return DropdownMenuItem<String>(
                        value: value,
                        child:
                        Text(value, style: const TextStyle(fontSize: 20)),
                      );
                    }).toList(),
                  ),
                ))),
              ],),
            const SizedBox(height: 20),
                Row(
                  crossAxisAlignment: CrossAxisAlignment.center,
                  mainAxisAlignment: MainAxisAlignment.end,
                  children: [
                    const Text('Name', style: TextStyle(fontSize: 30)),
                    SizedBox(width: 20),
                    SizedBox(
                    width: 250,
                    child: TextField(
                      autocorrect: false,
                      controller: _nameController,
                      decoration: const InputDecoration(
                        border: OutlineInputBorder(),
                        hintText: 'Your name',
                      ),
                      onSubmitted: (String value) async {
                        print(value);
                      },
                    )),
                  ],),
            const SizedBox(height: 20),
            Row(
              crossAxisAlignment: CrossAxisAlignment.center,
              mainAxisAlignment: MainAxisAlignment.end,
              children: [
                const Text('Partner\'s Bug Code', style: TextStyle(fontSize: 30)),
                SizedBox(width: 20),
                SizedBox(
                width: 245,
                child: TextField(
                  autocorrect: false,
                  inputFormatters: [FilteringTextInputFormatter.digitsOnly],
                  decoration: const InputDecoration(
                    border: OutlineInputBorder(),
                    hintText: 'Partner\'s bug code',
                  ),
                  onSubmitted: (String value) async {
                    print(value);
                  },
                )),
          ],
            ),
            const SizedBox(height: 20),
            //Steam Id
            Row(
              crossAxisAlignment: CrossAxisAlignment.center,
              mainAxisAlignment: MainAxisAlignment.end,
              children: [
                const Text('Steam ID', style: TextStyle(fontSize: 30)),
                SizedBox(width: 20),
                SizedBox(
                width: 250,
                child: TextField(
                  autocorrect: false,
                  decoration: const InputDecoration(
                    border: OutlineInputBorder(),
                    hintText: 'Your Steam ID',
                  ),
                  onSubmitted: (String value) async {
                    print(value);
                  },
                )),
          ]),
            //Steam API Key
            const SizedBox(height: 20),
            Row(
              crossAxisAlignment: CrossAxisAlignment.center,
              mainAxisAlignment: MainAxisAlignment.end,
              children: [
                const Text('Steam API Key', style: TextStyle(fontSize: 30)),
                SizedBox(width: 20),
                SizedBox(
                width: 250,
                child: TextField(
                  autocorrect: false,
                  decoration: const InputDecoration(
                    border: OutlineInputBorder(),
                    hintText: 'Your Steam API Key',
                  ),
                  onSubmitted: (String value) async {
                    print(value);
                  },
                )),
          ]),
            // profile picture
            const SizedBox(height: 20),
            Row(
              crossAxisAlignment: CrossAxisAlignment.center,
              mainAxisAlignment: MainAxisAlignment.end,
              children: [
                const Text('Profile Picture', style: TextStyle(fontSize: 30)),
                SizedBox(width: 20),
                SizedBox(
                width: 250,
                child: ButtonBar(
                  alignment: MainAxisAlignment.start,
                  children: [
                    TextButton(
                      onPressed: () {},
                      child: const Text('Upload'),
                    ),
                    TextButton(
                      onPressed: () {},
                      child: const Text('Remove'),
                    ),
                  ],
                )),

        ]),
            // Additional Games
            const SizedBox(height: 20),
            Row(
              crossAxisAlignment: CrossAxisAlignment.center,
              mainAxisAlignment: MainAxisAlignment.end,
              children: [
                const Text('Additional Games', style: TextStyle(fontSize: 30)),
                SizedBox(width: 20),
                SizedBox(
                width: 250,
                child: TextFormField(
                  autocorrect: false,
                  minLines: 6,
                  maxLines: 10 ,
                  decoration: const InputDecoration(
                    border: OutlineInputBorder(),
                    hintText: 'Enter as many games as you want, seperated by commas',
                  ),
                  onFieldSubmitted: (String value) async {
                    print(value);
                  },
                )),
          ]),
            //Server URL
            const SizedBox(height: 20),
            Row(
              crossAxisAlignment: CrossAxisAlignment.center,
              mainAxisAlignment: MainAxisAlignment.end,
              children: [
                const Text('Server URL', style: TextStyle(fontSize: 30)),
                SizedBox(width: 20),
                SizedBox(
                width: 250,
                child: TextField(
                  autocorrect: false,
                  decoration: const InputDecoration(
                    border: OutlineInputBorder(),
                    hintText: 'Remote Server URL',
                  ),
                  onSubmitted: (String value) async {
                    print(value);
                  },
                )),
          ]),
      ])
      ),
    );
  }
}

mixin _BugCode {
  static String BugCode = '123456';
}