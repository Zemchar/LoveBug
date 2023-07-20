using System;
using System.Buffers.Text;
using System.Data.SqlClient;
using System.IO;
using System.Text;
using System.Net;
using System.Net.Http.Json;
using System.Numerics;
using System.Text.Json.Nodes;
using System.Threading.Tasks;
using System.Web;
using Newtonsoft.Json;

namespace BugNest
{
    class BugNest
    {
        public static HttpListener listener;
        public static string url = "http://localhost:8080/";
        public static int pageViews = 0;
        public static int requestCount = 0;
        
        public static PartnerProfile LoadJson(int code)
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

                Uri uri_params = req.Url;
                JsonObject content = new JsonObject();

                //convert this to an endpoint 
                switch (req.HttpMethod)
                {
                    case "GET":
                        if (req.Url.AbsolutePath == "/newLoad")
                        {
                            Console.WriteLine($"New Load Requested\n{HttpUtility.ParseQueryString(req.Url.Query).Get("PartnerCode")}");
                            try{
                                var json = LoadJson(Int32.Parse(HttpUtility.ParseQueryString(req.Url.Query).Get("PartnerCode")));
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
                        break;
                    case "POST":
                        // If `shutdown` url requested, then shutdown the server after serving the page
                        if (req.Url.AbsolutePath == "/shutdown")
                        {
                            runServer = false;
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

        public static void Main(string[] args)
        {
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
}