using MySqlConnector;
using Newtonsoft.Json.Linq;

namespace BugNest;

public static class Program
{
    public static JObject config;
    public static async Task Main(string[] args)
    {
        config = JObject.Parse(File.ReadAllText("appsettings.json"));
        var conn = new MySqlConnection(
            $"Server={config["DB"]["Host"]};Database={config["DB"]["Database"]};Uid={config["DB"]["User"]};Pwd={config["DB"]["Password"]};");
        try
        {
            Console.WriteLine("[SQL] Connecting to DB");
            conn.Open();
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
        Thread webServer = new Thread(Static.CreateWebserver);
        Thread webSocket = new Thread(Socket.Nest.CreateWebSocket);
        webSocket.Start();
        webServer.Start();
    }

}