using System.Text;
using System.Net;
using System.Text.Json.Nodes;
using System.Web;
using Newtonsoft.Json;
using MySqlConnector;
using Newtonsoft.Json.Linq;

namespace BugNest
{
    abstract class Static
    {
        private static HttpListener? listener;
        public static JObject? config;

        public static ISharedMethods.PartnerProfile? PartnerLoadJson(int code)
        {
            string json = File.ReadAllText($"partners/{code}.json");
            ISharedMethods.PartnerProfile? profile = JsonConvert.DeserializeObject<ISharedMethods.PartnerProfile>(json);
            return profile;
        }

        
        private static async Task HandleIncomingConnections()
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
                Console.WriteLine(
                    $"[WEBSERVER] Request to Webserver\n==> ({req.HttpMethod}) {req.Url}\n==> {req.RemoteEndPoint}");

                //convert this to an endpoint 

                switch (req.HttpMethod)
                {
                    case "GET":
                        // copilot covert this to a REST endpoint
                        if (req.Url.AbsolutePath == "/newLoad")
                        {
                            string sql = @"
                            INSERT INTO UserProfiles (Code, Name, SteamID, AdditionalGames)
                            VALUES (@Code, @Name, @Steam, @AdditionalGames)
                            ON DUPLICATE KEY UPDATE
                                Name = VALUES(Name),
                                SteamID = VALUES(SteamID),
                                AdditionalGames = VALUES(AdditionalGames);
                        ";
                            


                            try
                            {
                                // Assuming you have the parameters ready, create the parameters dictionary
                                var p = new Dictionary<string, object?>
                                {
                                    { "@Code", HttpUtility.ParseQueryString(req.Url.Query).Get("UserCode") },
                                    { "@Name", HttpUtility.ParseQueryString(req.Url.Query).Get("userName") },
                                    { "@Steam", HttpUtility.ParseQueryString(req.Url.Query).Get("SteamID") },
                                    {
                                        "@AdditionalGames",
                                        HttpUtility.ParseQueryString(req.Url.Query).Get("AdditionalGames")
                                    }
                                };
                                await ISharedMethods.QueryDB(sql, p, ISharedMethods.SqlMethods.Execute);
                                var partnerCode = HttpUtility.ParseQueryString(req.Url.Query).Get("PartnerCode");
                                sql = "SELECT * FROM UserProfiles WHERE Code = @PartnerCode;";
                                if (partnerCode != null)
                                {
                                    var parameters = new Dictionary<string, object>
                                    {
                                        { "@PartnerCode", partnerCode }
                                    };
                                    var res = await ISharedMethods.QueryDB(sql, parameters, ISharedMethods.SqlMethods.Retrieve);
                                    if (res.HasRows)
                                    {
                                        while (res.Read())
                                        {
                                            content.Add("status", "success");
                                            content.Add("responseType", "PartnerProfile");
                                            content.Add("data", JsonConvert.SerializeObject(new ISharedMethods.PartnerProfile()
                                            {
                                                Code = res.GetInt32("Code"),
                                                SteamID = res.GetInt64("SteamID"),
                                                Name = res.GetString("Name"),
                                                Mood = res.GetString("Mood"),
                                                AdditionalGames = res.GetString("AdditionalGames"),
                                                pfp = res["Image"] as byte[] ?? Array.Empty<byte>()
                                            }));
                                        }

                                    }
                                    else
                                    {
                                        content.Add("status", "failure");
                                        content.Add("data", "No profile found");
                                        resp.StatusCode = 404;
                                    }
                                }
                            }
                            catch (Exception e)
                            {
                                content.Add("status", "failure");
                                content.Add("data", e.Message);
                                resp.StatusCode = 400;
                            }
                        }

                        if (req.Url.AbsolutePath == "/resource")
                        {
                            Console.WriteLine(
                                $"Resource Requested\n===> {HttpUtility.ParseQueryString(req.Url.Query).Get("ResourceType")}");

                            if (HttpUtility.ParseQueryString(req.Url.Query).Get("ResourceType") == "customGame")
                            {
                                try
                                {
                                    content.Add("status", "success");
                                    content.Add("responseType", "R_GamePlaceholder");
                                    content.Add("data",
                                        Convert.ToBase64String(await File.ReadAllBytesAsync("partners/images/CUSTOM.jpg")));
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
                            Dictionary<string, string> d = new Dictionary<string, string>
                            {
                                { "Host", (string)config["Host"] },
                                { "Port", ((int)config["Ports"]["WebSocket"]).ToString() }
                            };
                            content.Add("data", JsonConvert.SerializeObject(d));

                        }

                        break;
                    case "POST":
                        if (req.Url.AbsolutePath == "/resource")
                        {
                            var body = await new StreamReader(ctx.Request.InputStream).ReadToEndAsync();
                            var b2 = JsonConvert.DeserializeObject<Dictionary<string, string>>(body);
                            b2["Data"] = b2["Data"].Substring(2, b2["Data"].Length - 3);
                            byte[] imageData = Convert.FromBase64String(b2["Data"]);
                            await ISharedMethods.QueryDB($"UPDATE UserProfiles SET Image = @Image WHERE Code = @Code",
                                new Dictionary<string, object>() { { "Image", imageData }, { "Code", b2["Code"] } },
                                ISharedMethods.SqlMethods.Execute);
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
            config = JObject.Parse(File.ReadAllText("appsettings.json"));
            var conn = new MySqlConnection(
                $"Server={config["DB"]["Host"]};Database={config["DB"]["Database"]};Uid={config["DB"]["User"]};Pwd={config["DB"]["Password"]};");
            try
            {
                Console.WriteLine("[SQL] Connecting to DB");
                await conn.OpenAsync();
                Console.WriteLine($"[SQL] Connected to DB {conn.Database} as {config["DB"]["User"]}");

                await ISharedMethods.QueryDB(
                    "CREATE TABLE IF NOT EXISTS `UserProfiles` (Code int not null primary key, Name text null, SteamID bigint null, Mood text null, Image longtext null, AdditionalGames text null);CREATE TABLE IF NOT EXISTS `Interactions` (Code int not null, EventType text null, data text null, Epoch bigint not null, constraint Interactions_UserProfiles_code_fk foreign key (Code) references UserProfiles (Code))",
                    null, ISharedMethods.SqlMethods.Execute);

            }
            catch (Exception e)
            {
                Console.WriteLine("DB ERROR");
                Console.WriteLine(e.Message);
            }

            conn.CloseAsync();
            Thread webServer = new Thread(CreateWebserver);
            Thread webSocket = new Thread(Socket.Nest.CreateWebSocket);
            webSocket.Start();
            webServer.Start();
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
    
}