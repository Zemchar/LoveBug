using System.Data;
using System.Diagnostics;
using System.Numerics;
using MySqlConnector;

namespace BugNest;

public interface ISharedMethods
{
    internal enum SqlMethods
    {
        Execute,
        Retrieve
    }
    
    internal static async Task<MySqlDataReader> QueryDB(string sql, Dictionary<string, object?> parameters,
        SqlMethods method)
    {
        Debug.Assert(Static.config != null, "Static.config != null");
        MySqlConnection conn =
            new MySqlConnection(
                $"Server={Static.config["DB"]["Host"]};Database={Static.config["DB"]["Database"]};Uid={Static.config["DB"]["User"]};Pwd={Static.config["DB"]["Password"]};");
        if (conn.State != ConnectionState.Open)
            await conn.OpenAsync();
        await using (var cmd = new MySqlCommand())
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