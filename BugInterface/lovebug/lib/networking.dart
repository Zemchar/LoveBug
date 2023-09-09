import 'package:http/http.dart' as http;
import 'package:web_socket_channel/web_socket_channel.dart' as ws;
class HTTP {
  static Future<http.Response> get(String url) async {
    http.Response res = await http.get(Uri.parse(url));
    return res;
  }
  // Specialized HTTP
}

class RTC {
  ws.WebSocketChannel? channel;
  Future<ws.WebSocketChannel> connect(String url) async {
    if(channel != null) {
      return channel!;
    }
    channel = ws.WebSocketChannel.connect(Uri.parse(url));
    return channel!;
  }
  Future<void> send(ws.WebSocketChannel channel, String message) async {
    channel.sink.add(message);
  }
  Future<void> close(ws.WebSocketChannel channel) async {
    channel.sink.close();
  }

}