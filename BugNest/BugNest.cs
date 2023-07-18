using System;
using System.Data.SqlClient;
using System.IO;
using System.Text;
using System.Net;
using System.Net.Http.Json;
using System.Text.Json.Nodes;
using System.Threading.Tasks;
using System.Web;

namespace BugNest
{
    class BugNest
    {
        public static HttpListener listener;
        public static string url = "http://localhost:8080/";
        public static int pageViews = 0;
        public static int requestCount = 0;
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
                switch (req.HttpMethod)
                {
                    case "GET":
                        if (req.Url.AbsolutePath == "/ketchup")
                        {
                            HttpUtility.ParseQueryString(uri_params.Query).Get("epoch");
                            content.Add("epoch", HttpUtility.ParseQueryString(uri_params.Query).Get("epoch"));
                            // TODO: Respond with json data
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
                byte[] data = Encoding.UTF8.GetBytes(content.ToJsonString());
                resp.ContentType = "text/json";
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
            listener.Prefixes.Add($"http://{args[0]}:{args[1]}/");
            listener.Start();
            Console.WriteLine("Listening for connections on {0}", url);

            // Handle requests
            Task listenTask = HandleIncomingConnections();
            listenTask.GetAwaiter().GetResult();

            // Close the listener
            listener.Close();
        }
    }
}