/*
MAIN FILE USED FOR INITALIZING APP. VIEWS ARE IN THE OTHER FOLDERS
*/
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:provider/provider.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'package:desktop_window/desktop_window.dart';
// Import the views
import 'package:lovebug/Views/Games.dart';
import 'package:lovebug/Views/Gallery.dart';
import 'package:lovebug/Views/Settings.dart';
import 'package:lovebug/Views/Home.dart';
void main() {
  runApp(ChangeNotifierProvider(
    create: (_) => ThemeProvider(),
    child: const MyApp(),
  ));
}
class ThemeProvider extends ChangeNotifier {
  Color currentTheme = Colors.pink;

  void changeTheme(Color newTheme) {
    currentTheme = newTheme;
    notifyListeners(); // Notify listeners of the change
  }
}

class MyApp extends StatefulWidget {
  const MyApp({super.key});

  State<MyApp> createState() => _MyAppState();
}

class _MyAppState extends State<MyApp> {
  @override
  Widget build(BuildContext context) {
    final themeProvider = Provider.of<ThemeProvider>(context);

    return MaterialApp(
      title: 'Love Bug',
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: themeProvider.currentTheme),
        useMaterial3: true,
      ),
      home: const MainPage(title: 'Love Bug'),
    );
  }
  @override
  void initState() {
    super.initState();
    WidgetsBinding.instance!.addPostFrameCallback((_) async {
      SharedPreferences prefs = await SharedPreferences.getInstance();
      if(prefs.containsKey('theme')) {
        theming.currentThemeName = prefs.getString('theme')!;
        theming.currentTheme = theming.themeMapping[theming.currentThemeName]!;
      }
      else {
        prefs.setString('theme', theming.currentThemeName);
      }
      DesktopWindow.setMinWindowSize(const Size(600, 600));
      DesktopWindow.setMaxWindowSize(const Size(600, 600));
      DesktopWindow.setWindowSize(const Size(600, 600));
    });
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
  void changeIndex(int newIndex) {
    setState(() {
      _index = newIndex;
    });
  }
  final List<Widget> _children = [
    const Home(),
    const Games(),
//    const Gallery(), removing for now, just need to focus on core functionality
  //TODO: Reimplement Gallery
    const Settings()
  ];
  int _index = 0; // Make sure this is outside build(), otherwise every setState will change the value back to 0

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
              // BottomNavigationBarItem(
              //     icon: const Icon(Icons.photo_album_outlined),
              //     label: 'Gallery',
              //     backgroundColor: Theme.of(context).colorScheme.scrim),
              BottomNavigationBarItem(
                  icon: const Icon(Icons.settings_outlined),
                  label: 'Settings',
                  backgroundColor: Theme.of(context).colorScheme.scrim),
            ]));
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
