import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:web_socket_channel/web_socket_channel.dart' as ws;
import 'package:shared_preferences/shared_preferences.dart';
import 'package:lovebug/main.dart' as main;

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
}
