using System;
using Gtk;
using UI = Gtk.Builder.ObjectAttribute;

namespace LoveBug
{
    class GraphicalBug : Window
    {
        [UI] private Label _label1 = null;
        [UI] private Button _button1 = null;

        private int _counter;

        public GraphicalBug() : this(new Builder("LoveBugMain.glade")) { }

        private GraphicalBug(Builder builder) : base(builder.GetRawOwnedObject("MainWindow"))
        {
            builder.Autoconnect(this);

            DeleteEvent += Window_DeleteEvent;
        }

        private void Window_DeleteEvent(object sender, DeleteEventArgs a)
        {
            Application.Quit();
        }
        
    }
}
