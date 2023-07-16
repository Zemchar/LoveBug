using System;
using Gtk;
using System.Net.Http.Headers;
using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Net.WebSockets;
using System.Threading;
using System.Threading.Tasks;

namespace LoveBug
{
    class BugEntry
    {
        [STAThread]
        public static async Task Main(string[] args)
        {
            Application.Init();
            var app = new Application("org.juniper.Lovebug", GLib.ApplicationFlags.None);
            app.Register(GLib.Cancellable.Current);
            
            //Connect to websocket server
            Console.WriteLine("Connecting to websocket server...");
            ClientWebSocket webSocket = new ClientWebSocket();
            await webSocket.ConnectAsync(new Uri("ws://localhost:8080"), CancellationToken.None).ContinueWith((res) =>
            {
                Console.WriteLine(res.Exception);
                Console.WriteLine("Connected to websocket server");
            });
            

            var win = new GraphicalBug();
            app.AddWindow(win);

            win.Show();
            Application.Run();
        }
    }
}
