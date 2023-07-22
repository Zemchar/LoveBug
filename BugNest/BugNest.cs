using System.Data;
using System.Data.SqlClient;
using System.Text;
using System.Net;
using System.Net.Sockets;
using System.Numerics;
using System.Reflection.Metadata;
using System.Text.Json.Nodes;
using System.Text.RegularExpressions;
using System.Web;
using Newtonsoft.Json;
using Microsoft.Extensions.Configuration;
using MySqlConnector;
using Newtonsoft.Json.Linq;
using NetCoreServer;

namespace BugNest
{
    class BugNest
    {
        public static HttpListener listener;
        static JObject config;
        
        public static PartnerProfile PartnerLoadJson(int code)
        {
            string json = File.ReadAllText($"partners/{code}.json");
            PartnerProfile profile = JsonConvert.DeserializeObject<PartnerProfile>(json);
            return profile;
        }

        public static async Task HandleIncomingConnections()
        {
            bool runServer = true;
            // While a user hasn't visited the `shutdown` url, keep on handling requests
            while (runServer)
            {
                // Will wait here until we hear from a connection
                HttpListenerContext ctx = await listener.GetContextAsync();

                // Peel out the requests and response objects
                HttpListenerRequest req = ctx.Request;
                HttpListenerResponse resp = ctx.Response;

                JsonObject content = new JsonObject();
                Console.WriteLine($"[WEBSERVER] Request to Webserver\n==> ({req.HttpMethod}) {req.Url}\n==> {req.RemoteEndPoint}");

                //convert this to an endpoint 
                switch (req.HttpMethod)
                {
                    case "GET":
                        if (req.Url.AbsolutePath == "/newLoad")
                        {
                            try{
                                var json = PartnerLoadJson(Int32.Parse(HttpUtility.ParseQueryString(req.Url.Query).Get("PartnerCode")));
                                try
                                {
                                    byte[] img = System.IO.File.ReadAllBytes(json.profile);
                                    json.pfp = img;
                                }
                                catch (DirectoryNotFoundException e)
                                {
                                    Console.WriteLine($"[WEBSERVER][ERROR] Looked for {json.profile} but it was not found");
                                }
                                content.Add("status", "success");
                                content.Add("responseType", "partnerInfo");
                                content.Add("data", JsonConvert.SerializeObject(json));
                            }
                            catch(Exception e){
                                content.Add("status", "failure");
                                content.Add("data", e.Message);
                                resp.StatusCode = 400;
                            }
                        }

                        if (req.Url.AbsolutePath == "/resource")
                        {
                            Console.WriteLine($"Resource Requested\n===> {HttpUtility.ParseQueryString(req.Url.Query).Get("ResourceType")}");

                            if (HttpUtility.ParseQueryString(req.Url.Query).Get("ResourceType") == "customGame")
                            {
                                try
                                {
                                    content.Add("status", "success");
                                    content.Add("responseType", "R_GamePlaceholder");
                                    content.Add("data", Convert.ToBase64String(File.ReadAllBytes("partners/images/CUSTOM.jpg")));
                                }
                                catch (Exception e)
                                {
                                    Console.WriteLine(e);
                                    content.Add("status", "failure");
                                    content.Add("data", e.Message);
                                }
                            }
                        }
                        if (req.Url.AbsolutePath == "/reqWS")
                        {
                            content.Add("status", "success");
                                content.Add("responseType", "WSInfo");
                                Dictionary<string, string> d = new Dictionary<string, string>();
                                d.Add("Host", (string)config["Host"]);
                                d.Add("Port", ((int)config["Ports"]["WebSocket"]).ToString());
                                content.Add("data", JsonConvert.SerializeObject(d));
                                //TODO: Query databse here for missed messages

                        }
                        break;
                    case "POST":
                        if (req.Url.AbsolutePath == "/resource")
                        {
                            var body = new StreamReader(ctx.Request.InputStream).ReadToEnd();
                            var b2 = JsonConvert.DeserializeObject<Dictionary<string, string>>(body);
                            b2["Data"] = b2["Data"].Substring(2, b2["Data"].Length - 3);
                            byte[] imageData = Convert.FromBase64String(b2["Data"]);
                            await QueryDB($"UPDATE UserProfiles SET Image = @Image WHERE Code = @Code", new Dictionary<string, object>(){{"Image", imageData}, {"Code", b2["Code"]}}, SqlMethods.Execute);
                            content.Add("status", "success");
                            content.Add("responseType", "ImageUpload");

                        }
                        break;
                }
                // Write the response info
                string disableSubmit = !runServer ? "disabled" : "";
                byte[] data = Encoding.UTF8.GetBytes(content.ToString());
                resp.ContentType = "application/json";
                resp.ContentEncoding = Encoding.UTF8;
                resp.ContentLength64 = data.LongLength;
                

                // Write out to the response stream (asynchronously), then close it
                await resp.OutputStream.WriteAsync(data, 0, data.Length);
                resp.Close();
            }
        }

        public static async Task Main(string[] args)
        {
            MySqlConnection conn;

            config = JObject.Parse(File.ReadAllText("appsettings.json"));
            conn = new MySqlConnection($"Server={config["DB"]["Host"]};Database={config["DB"]["Database"]};Uid={config["DB"]["User"]};Pwd={config["DB"]["Password"]};");
            try
            {
                Console.WriteLine("[SQL] Connecting to DB");
                await conn.OpenAsync();
                Console.WriteLine($"[SQL] Connected to DB {conn.Database} as {config["DB"]["User"]}");

                await QueryDB("CREATE TABLE IF NOT EXISTS `UserProfiles` (Code int not null primary key, Name text null, SteamID bigint null, Mood text null, Image longtext null, AdditionalGames text null);CREATE TABLE IF NOT EXISTS `Interactions` (Code int not null, EventType text null, data text null, Epoch bigint not null, constraint Interactions_UserProfiles_code_fk foreign key (Code) references UserProfiles (Code))",
                    null, SqlMethods.Execute);

            }
            catch(Exception e)
            {
                Console.WriteLine("DB ERROR");
                Console.WriteLine(e.Message);
            }

            conn.CloseAsync();
            Thread webServer = new Thread(CreateWebserver);
            Thread webSocket = new Thread(CreateWebSocket);
            webSocket.Start();
            webServer.Start();


        }
        private static void CreateWebSocket()
        {
            var server = new SocketServer(IPAddress.Parse((string)config["Host"]), (int)config["Ports"]["WebSocket"]);
            server.Start();
            Console.WriteLine($"[WEBSOCKET] WebSocket server listening on {server.Address}...");
        }

        public static async Task<MySqlDataReader> QueryDB(string sql, Dictionary<string, object>? parameters, SqlMethods method)
        {
            MySqlConnection conn = new MySqlConnection($"Server={config["DB"]["Host"]};Database={config["DB"]["Database"]};Uid={config["DB"]["User"]};Pwd={config["DB"]["Password"]};");
            if(conn.State != ConnectionState.Open)
                await conn.OpenAsync();
            using (var cmd = new MySqlCommand())
            {
                cmd.Connection = conn;
                cmd.CommandText = sql;
                if (parameters is not null)
                {
                    foreach (var parameter in parameters)
                    {
                        cmd.Parameters.AddWithValue(parameter.Key, parameter.Value);
                    }
                }
                
                switch (method)
                {
                    case SqlMethods.Execute: //Used for INSERT, UPDATE, DELETE
                        await cmd.ExecuteNonQueryAsync();
                        Console.WriteLine($"[SQL] Executed query {cmd.CommandText.Remove(50) + "..."}");
                        break;
                    case SqlMethods.Retrieve: //Used for SELECT
                        Console.WriteLine($"[SQL] Retrieved query {cmd.CommandText.Remove(50) + "..."}");
                        return await cmd.ExecuteReaderAsync();
                }
                
            }

            await conn.CloseAsync();
            return null;
        }


        private static void CreateWebserver()
        {
            var url = $"{config["Method"]}{config["Host"]}:{config["Ports"]["StaticApp"]}/";
          // Create a Http server and start listening for incoming connections
            listener = new HttpListener();
            listener.Prefixes.Add(url);
            listener.Start();
            Console.WriteLine("[WEBSERVER] Listening for connections on {0}", url);

            // Handle requests
            Task listenTask = HandleIncomingConnections();
            listenTask.GetAwaiter().GetResult();

            // Close the listener
            listener.Close();
        }
    }

    internal enum SqlMethods
    {
        Execute,
        Retrieve
    }
    internal class PartnerProfile
    {
        public string profile { get; set; }
        public byte[] pfp;
        public int Code { get; set; }
        public BigInteger SteamID { get; set; }
        public string Name { get; set; }
        public string Mood { get; set; }
        public string AdditionalGames { get; set; }
    }
    
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
        public override async void OnWsReceived(byte[] buffer, long offset, long size)
        {
            string message = Encoding.UTF8.GetString(buffer, (int)offset, (int)size);
            Console.WriteLine($"[WEBSOCKET][INCOMING] {message} \n==> {Id}");
            WsServer server = ((WsServer)Server);
            var data =JsonConvert.DeserializeObject<Dictionary<string, string>>(message);
            var response = new Dictionary<string, List<Dictionary<string, string>>>();
            if (data["EventType"] == "init")
            {
                var z =await BugNest.QueryDB("SELECT * FROM Interactions WHERE Code = @Code AND Epoch < @Epoch ORDER BY Epoch DESC LIMIT 20", new Dictionary<string, object>(){{"Code", data["Code"]}, {"Epoch", DateTimeOffset.UtcNow.ToUnixTimeSeconds().ToString()}}, SqlMethods.Retrieve);
                if (z.HasRows)
                {
                    while (z.Read())
                    {
                        try
                        {
                            var d = new Dictionary<string, string>();
                            d.Add("EventType", z.GetString("EventType"));
                            d.Add("Data", z.GetString("Data"));
                            d.Add("Epoch", z.GetInt64("Epoch").ToString());
                            if (response.ContainsKey("MsgUpdate"))
                            {
                                response["MsgUpdate"].Add(d);
                            }
                            else
                            {
                                response.Add("MsgUpdate", new List<Dictionary<string, string>>(){d});
                            }
                        }
                        catch (Exception e)
                        {
                            Console.WriteLine(e);
                        }
                    }
                }
            }
            else
            {
                await BugNest.QueryDB("INSERT INTO Interactions (Code, EventType, Data, Epoch) VALUES (@Code, @EventType, @Data, @Epoch)", new Dictionary<string, object>(){{"Code", data["Code"]}, {"EventType", data["EventType"]}, {"Data", data["Data"]}, {"Epoch", DateTimeOffset.UtcNow.ToUnixTimeSeconds().ToString()}}, SqlMethods.Execute);
            }
            server.MulticastText(JsonConvert.SerializeObject(response));
        }
        protected override void OnError(SocketError error)
        {
            Console.WriteLine($"Chat WebSocket session caught an error with code {error}");
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