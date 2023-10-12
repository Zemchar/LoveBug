import 'dart:convert';
import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:web_socket_channel/web_socket_channel.dart' as ws;
import 'package:shared_preferences/shared_preferences.dart';
import 'package:lovebug/main.dart' as main;
import 'package:motion_toast/motion_toast.dart';

class HTTP {
  // General HTTP
  static late SharedPreferences prefs;
  static Future<http.Response> get(String endpoint, BuildContext context,
      {bool asFullUrl = false}) async {
    prefs = await SharedPreferences.getInstance();
    http.Response res;
    if (!asFullUrl) {
      try {
        endpoint = prefs.getString('RemoteURL')! + endpoint;
        res = await http.get(Uri.parse(endpoint));
        MotionToast.success(description: Text(res.body), title: Text('Success')).show(context);
        return res;
      } catch (e) {
        showDialog<void>(
          context: context,
          barrierDismissible: false, // user must tap button!
          builder: (BuildContext context) {
            return AlertDialog(
              title: const Text('No Connection'),
              content: SingleChildScrollView(
                child: ListBody(
                  children: <Widget>[
                    Text('Failed to connect to the remote server!'),
                    Text(
                        'Please Double Check what your remote URL is set to in settings!'),
                    Text('URL_TRIED: ' + endpoint),
                    Text('ERROR: ' + e.toString()),
                  ],
                ),
              ),
              actions: <Widget>[
                TextButton(
                    child: const Text('OK'),
                    onPressed: () {
                      Navigator.of(context).pop();
                    }),
              ],
            );
          },
        );
        throw Exception('Failed to connect to the remote server!');
      }
    } else {
      res = await http.get(Uri.parse(endpoint));
      return res;
    }
  }

  static Future<http.Response> post(
      String url, Map<String, String> body) async {
    http.Response res = await http.post(Uri.parse(url), body: body);
    return res;
  }
  // Specialized HTTP
}
class Steam implements HTTP {
  static Image getGameImage(int steamID) {
    return Image.network('https://steamcdn-a.akamaihd.net/steam/apps/$steamID/header.jpg');
  }

  static Future<List<dynamic>> getGameInfo(String key, String steamID, BuildContext context) async {
    try{
      var res = await http.get(Uri.parse("https://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key=$key&steamid=$steamID&include_appinfo=1&format=json&include_played_free_games=1"));
      var json = jsonDecode(res.body)['response']['games'];
      if(res.statusCode != 200 || res.body[0].isEmpty || json == null) {
        throw Exception("Steam did not respond!");
      }
      return json;
    }catch(e){
      throw Exception("Failed to get game info!\n$e");
    }
  }

  static List<dynamic> intersection (List<dynamic> a, List<dynamic>b) {
    var c = [];
    // I HATE THIS
    if(a.length > b.length){
      for(var game in a) {
        for(var game2 in b) {
          if(game['appid'] == game2['appid']) {
            c.add(game);
          }
        }
      }
    }else{
      for(var game in b) {
        for(var game2 in a) {
          if(game['appid'] == game2['appid']) {
            c.add(game);
          }
        }
      }
    }
    return c;
  }


}
class RTC {
  static ws.WebSocketChannel? channel;
  static Future<ws.WebSocketChannel> connect(String url) async {
    if (channel != null) {
      return channel!;
    }
    channel = ws.WebSocketChannel.connect(Uri.parse(url));
    return channel!;
  }

 static Future<void> send(Object message) async {
    channel?.sink.add(message);
  }

  static Future<void> close(ws.WebSocketChannel channel) async {
    channel.sink.close();
  }
}

class Loading implements HTTP {
  static Future<void> show(BuildContext context) async {
    showDialog(
      context: context,
      builder: (BuildContext context) {
        return const AlertDialog(
          content: SizedBox(
            height: 50,
            child: Center(
              child: CircularProgressIndicator(),
            ),
          ),
        );
      },
    );
  }
  static Future<void> hide(BuildContext context) async {
    Navigator.of(context).pop();
  }
}
