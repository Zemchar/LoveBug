using System.Net;
using System.Net.Sockets;
using System.Text;
using NetCoreServer;
using Newtonsoft.Json;

namespace BugNest;

public abstract class Socket
{
    public class Nest : WsSession
    {
        public Nest(WsServer server) : base(server){ }
        
        public override void OnWsConnected(HttpRequest request)
        {
            Console.WriteLine($"[WEBSOCKET][NEW_CONNECTION] New session created\n==> {Id}");
            SendTextAsync("Connection Established");
        }
        public override void OnWsDisconnected()
        {
            Console.WriteLine($"[WEBSOCKET][CONNECTION_LOST] Client Disconnect\n==> {Id}");
        }

        private string CleanJsonData(string jsonData)
        {
            // Use Newtonsoft.Json to deserialize and then serialize the JSON data
            // This process will remove newlines and extra whitespace
            dynamic dataObject = JsonConvert.DeserializeObject(jsonData);
            return JsonConvert.SerializeObject(dataObject, Formatting.None);
        }

        public override async void OnWsReceived(byte[] buffer, long offset, long size)
        {
            string message = Encoding.UTF8.GetString(buffer, (int)offset, (int)size);
            Console.WriteLine($"[WEBSOCKET][INCOMING] {message} \n==> {Id}");
            WsServer server = ((WsServer)Server);   
            var data =JsonConvert.DeserializeObject<Dictionary<string, object>>(message);
            var response = new Dictionary<string, List<Dictionary<string, object>>>();
            if ((string)data["EventType"] == "init")
            {
                var z =await ISharedMethods.QueryDB("SELECT * FROM Interactions WHERE Code = @Code OR @PCode AND Epoch < @Epoch ORDER BY Epoch DESC LIMIT 20", new Dictionary<string, object>(){{"Code", data["Code"]}, {"PCode", data["PCode"]}, {"Epoch", DateTimeOffset.UtcNow.ToUnixTimeSeconds().ToString()}}, ISharedMethods.SqlMethods.Retrieve);
                if (z.HasRows)
                {
                    while (z.Read())
                    {
                        try
                        {
                            var d = new Dictionary<string, object>
                            {
                                { "EventType", z.GetString("EventType") },
                                { "Data", z.GetString("Data") },
                                { "Epoch", z.GetInt64("Epoch").ToString() }
                            };
                            if (response.TryGetValue("MsgUpdate", out var value))
                            {
                                value.Add(d);
                            }
                            else
                            {
                                response.Add("MsgUpdate", new List<Dictionary<string, object>>(){d});
                            }
                        }
                        catch (Exception e)
                        {
                            Console.WriteLine(e);
                        }
                    }
                }
            }
            else if ((string)data["EventType"] == "SettingsUpdate")
            {
                var set = JsonConvert.DeserializeObject<Dictionary<string, object>>(data["Settings"].ToString());
                Console.WriteLine("Settings Update");
                var sql = @"UPDATE UserProfiles SET SteamID = @SteamID, Name = @Name, AdditionalGames = @AdditionalGames WHERE Code = @Code";
                var p = new Dictionary<string, object>()
                {
                    {"SteamID" , set["SteamID"]},
                    {"Name", set["userName"]},
                    {"AdditionalGames", set["AdditionalGames"]},
                    {"Code", data["Code"]}
                };
                await ISharedMethods.QueryDB(sql, p, ISharedMethods.SqlMethods.Execute);
                response.Add("SettingsUpdate", new List<Dictionary<string, object>>(){data});
            }
            else if ((string)data["EventType"] == "SEND_MOOD")
            {
                var set = JsonConvert.DeserializeObject<Dictionary<string, object>>(data["Data"].ToString());
                var epoch = DateTimeOffset.UtcNow.ToUnixTimeSeconds().ToString();
                var sql = @"UPDATE UserProfiles SET Mood = @Mood WHERE Code = @Code";
                var p = new Dictionary<string, object>()
                {
                    {"Mood" , set["Mood"]},
                    {"Code", data["Code"]}
                };
                await ISharedMethods.QueryDB(sql, p, ISharedMethods.SqlMethods.Execute);
                await ISharedMethods.QueryDB("INSERT INTO Interactions (Code, EventType, Data, Epoch) VALUES (@Code, @EventType, @Data, @Epoch)", new Dictionary<string, object>(){{"Code", data["Code"]}, {"EventType", data["EventType"]}, {"Data", CleanJsonData(data["Data"].ToString())}, {"Epoch", epoch}}, ISharedMethods.SqlMethods.Execute);
                response.Add("NewComm", new List<Dictionary<string, object>>(){data});
            }
            else
            {
                var epoch = DateTimeOffset.UtcNow.ToUnixTimeSeconds().ToString();
                await ISharedMethods.QueryDB("INSERT INTO Interactions (Code, EventType, Data, Epoch) VALUES (@Code, @EventType, @Data, @Epoch)", new Dictionary<string, object>(){{"Code", data["Code"]}, {"EventType", data["EventType"]}, {"Data", CleanJsonData(data["Data"].ToString())}, {"Epoch", epoch}}, ISharedMethods.SqlMethods.Execute);
                data.Add("Epoch", epoch);
                response.Add("NewComm", new List<Dictionary<string, object>>(){data});
            }
            Console.WriteLine($"[WEBSOCKET][OUTGOING] {JsonConvert.SerializeObject(response)} \n==> {Id}");
            server.MulticastText(JsonConvert.SerializeObject(response));
        }
        protected override void OnError(SocketError error)
        {
            Console.WriteLine($"Chat WebSocket session caught an error with code {error}");
        }

        public static void CreateWebSocket()
        {
            Console.WriteLine((string)Program.config["Host"]);
            Console.WriteLine((int)Program.config["Ports"]["WebSocket"]);
            var server = new SocketServer(IPAddress.Parse((string)Program.config["Host"]), (int)Program.config["Ports"]["WebSocket"]);
            server.Start();
            Console.WriteLine($"[WEBSOCKET] WebSocket server listening on {server.Address}:{server.Port}");
        }
    }
    
    class SocketServer : WsServer
    {
        public SocketServer(IPAddress address, int port) : base(address, port) {}

        protected override TcpSession CreateSession() { return new Nest(this); }

        protected override void OnError(SocketError error)
        {
            Console.WriteLine($"Chat WebSocket server caught an error with code {error}");
        }
    }

}