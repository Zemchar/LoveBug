using System.Text;
using System.Net;
using System.Net.Sockets;
using System.Numerics;
using System.Text.Json.Nodes;
using System.Text.RegularExpressions;
using System.Web;
using Newtonsoft.Json;
using Microsoft.Extensions.Configuration;
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
            Console.WriteLine("Handling Connections");
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
                Console.WriteLine($"Request to Webserver\n{req.Url}");

                //convert this to an endpoint 
                switch (req.HttpMethod)
                {
                    case "GET":
                        if (req.Url.AbsolutePath == "/newLoad")
                        {
                            Console.WriteLine($"New Load Requested\n{HttpUtility.ParseQueryString(req.Url.Query).Get("PartnerCode")}");
                            try{
                                var json = PartnerLoadJson(Int32.Parse(HttpUtility.ParseQueryString(req.Url.Query).Get("PartnerCode")));
                                try
                                {
                                    byte[] img = System.IO.File.ReadAllBytes(json.profile);
                                    json.pfp = img;
                                }
                                catch (DirectoryNotFoundException e)
                                {
                                    Console.WriteLine($"Looked for {json.profile} but it was not found");
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
                                Console.WriteLine(d);
                                content.Add("data", JsonConvert.SerializeObject(d));
                                //TODO: Query databse here for missed messages

                        }
                        break;
                    case "POST":
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

        public static void Main(string[] args)
        {
            config = JObject.Parse(File.ReadAllText("appsettings.json"));

            Thread webServer = new Thread(CreateWebserver);
            Thread webSocket = new Thread(CreateWebSocket);
            webSocket.Start();
            webServer.Start();


        }
        private static void CreateWebSocket()
        {
            var server = new SocketServer(IPAddress.Parse((string)config["Host"]), (int)config["Ports"]["WebSocket"]);
            server.Start();
            Console.WriteLine($"WebSocket server listening on {server.Address}...");
        }
        
        
        private static void CreateWebserver()
        {
            var url = $"{config["Method"]}{config["Host"]}:{config["Ports"]["StaticApp"]}/";
          // Create a Http server and start listening for incoming connections
            listener = new HttpListener();
            listener.Prefixes.Add(url);
            listener.Start();
            Console.WriteLine("Listening for connections on {0}", url);

            // Handle requests
            Task listenTask = HandleIncomingConnections();
            listenTask.GetAwaiter().GetResult();

            // Close the listener
            listener.Close();
        }
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
        public Nest(WsServer server) : base(server)
        {
        }

        public override void OnWsConnected(HttpRequest request)
        {
            Console.WriteLine($"Chat WebSocket session with Id {Id} connected!");
            string message = "Hello from WebSocket chat! Please send a message or '!' to disconnect the client!";
            SendTextAsync(message);
        }
        public override void OnWsDisconnected()
        {
            Console.WriteLine($"Chat WebSocket session with Id {Id} disconnected!");
        }
        public override void OnWsReceived(byte[] buffer, long offset, long size)
        {
            string message = Encoding.UTF8.GetString(buffer, (int)offset, (int)size);
            Console.WriteLine("Incoming: " + message);

            // Multicast message to all connected sessions
            ((WsServer)Server).MulticastText(message);

            // If the buffer starts with '!' the disconnect the current session
            if (message == "!")
                Close(1000);
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