import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:provider/provider.dart'; // Import the provider package
import '../main.dart';
import 'package:lovebug/networking.dart' as networking;
import 'package:shared_preferences/shared_preferences.dart';
class Settings extends StatefulWidget {
  const Settings({super.key});
  @override

  State<Settings> createState() => _SettingsState();
}

class _SettingsState extends State<Settings> {
  String _notifBoxValue = 'On';
  late ThemeProvider themeProvider; // Declare a ThemeProvider variable
  var prefs;

  @override
  void initState() {
    super.initState();
    setupPrefs();
  }
  @override
  void didChangeDependencies() {
    super.didChangeDependencies();

    // Access the ThemeProvider using the context provided by the build method
    themeProvider = Provider.of<ThemeProvider>(context);
  }


  Future<Map<String, Object>> setupPrefs() async {
    prefs = await SharedPreferences.getInstance();
    Map<String, Object> data = {};
    for(String key in prefs.getKeys()) {
      data[key] = prefs.get(key)!;
    }
    return data;
  }

  @override
  Widget build(BuildContext context) {
    return FutureBuilder(
        future: setupPrefs(),
        builder: (BuildContext context, AsyncSnapshot snapshot) {
          if (snapshot.hasData) {
            return Scaffold(
              body: SingleChildScrollView(
                  padding: const EdgeInsets.all(20),
                  child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                      children: [
                        Align(
                          alignment: Alignment.center,
                          child: Text('Your Bug Code: ${_BugCode.BugCode}', style: const TextStyle(fontSize: 20)),
                        ),
                        const SizedBox(height: 20),
                        Row(
                          crossAxisAlignment: CrossAxisAlignment.center,
                          mainAxisAlignment: MainAxisAlignment.end,
                          children: [
                            const Text('Notifications', style: TextStyle(fontSize: 30)),
                            const SizedBox(width: 20),
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
                                  prefs.setString('notifications', newValue!);
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
                            const SizedBox(width: 20),
                            SizedBox(width: 250, height: 70, child:
                            InputDecorator(
                                decoration: InputDecoration(
                                  border:
                                  OutlineInputBorder(borderRadius: BorderRadius.circular(5.0)),
                                ), child:
                            DropdownButtonHideUnderline(
                              child: DropdownButton<String>(
                                icon: const Icon(Icons.color_lens_outlined),
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
                            const SizedBox(width: 20),
                            SizedBox(
                                width: 250,
                                child: TextField(
                                  autocorrect: false,
                                  controller: TextEditingController(text: prefs.getString('name')),
                                  decoration: const InputDecoration(
                                    border: OutlineInputBorder(),
                                    hintText: 'Your name',
                                  ),
                                  onSubmitted: (String value) async {
                                    prefs.setString('name', value);
                                  },
                                )),
                          ],),
                        const SizedBox(height: 20),
                        Row(
                          crossAxisAlignment: CrossAxisAlignment.center,
                          mainAxisAlignment: MainAxisAlignment.end,
                          children: [
                            const Text('Partner\'s Bug Code', style: TextStyle(fontSize: 30)),
                            const SizedBox(width: 20),
                            SizedBox(
                                width: 245,
                                child: TextField(
                                  controller: TextEditingController(text: prefs.getString('partnerBugCode')),
                                  autocorrect: false,
                                  inputFormatters: [FilteringTextInputFormatter.digitsOnly],
                                  decoration: const InputDecoration(
                                    border: OutlineInputBorder(),
                                    hintText: 'Partner\'s bug code',
                                  ),
                                  onSubmitted: (String value) async {
                                    prefs.setString('partnerBugCode', value);
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
                              const SizedBox(width: 20),
                              SizedBox(
                                  width: 250,
                                  child: TextField(
                                    controller: TextEditingController(text: prefs.getString('steamID')),
                                    autocorrect: false,
                                    decoration: const InputDecoration(
                                      border: OutlineInputBorder(),
                                      hintText: 'Your Steam ID',
                                    ),
                                    onSubmitted: (String value) async {
                                      prefs.setString('steamID', value);
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
                              const SizedBox(width: 20),
                              SizedBox(
                                  width: 250,
                                  child: TextField(
                                    controller: TextEditingController(text: prefs.getString('steamAPIKey')),
                                    autocorrect: false,
                                    decoration: const InputDecoration(
                                      border: OutlineInputBorder(),
                                      hintText: 'Your Steam API Key',
                                    ),
                                    onSubmitted: (String value) async {
                                      prefs.setString('steamAPIKey', value);
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
                              const SizedBox(width: 20),
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
                              const SizedBox(width: 20),
                              SizedBox(
                                  width: 250,
                                  child: TextFormField(
                                    controller: TextEditingController(text: prefs.getString('additionalGames')),
                                    autocorrect: false,
                                    minLines: 6,
                                    maxLines: 10 ,
                                    decoration: const InputDecoration(
                                      border: OutlineInputBorder(),
                                      hintText: 'Enter as many games as you want, seperated by commas',
                                    ),
                                    onFieldSubmitted: (String value) async {
                                      prefs.setString('additionalGames', value);
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
                              const SizedBox(width: 20),
                              SizedBox(
                                  width: 250,
                                  child: TextField(
                                    controller: TextEditingController(text: prefs.getString('RemoteURL')),
                                    autocorrect: false,
                                    decoration: const InputDecoration(
                                      border: OutlineInputBorder(),
                                      hintText: 'Remote Server URL',
                                    ),
                                    onSubmitted: (String value) async {
                                      prefs.setString('RemoteURL', value);
                                    },
                                  )),
                            ]),
                        ButtonBar(
                          alignment: MainAxisAlignment.center,
                          children: [
                            ElevatedButton(
                              onPressed: () {
                                Map<String, Object> data = {};
                                for(String key in prefs.getKeys()) {
                                  data[key] = prefs.get(key)!;
                                }

                                print(data);
                                if(networking.RTC.channel != null) {
                                  networking.RTC.send({"EventType": "SettingsUpdate", "Settings": data, "Code": _BugCode.BugCode});
                                }
                              },
                              child: const Text('Save', style: TextStyle(fontSize: 30)),
                            ),
                          ],
                        ),
                      ])

              ),
            );;
          } else if (snapshot.hasError) {
            return Center(child: Icon(Icons.error_outline));
          } else {
            return Center(child: CircularProgressIndicator());
          }
        });
  }
}


mixin _BugCode {
  static String BugCode = '123456';
}