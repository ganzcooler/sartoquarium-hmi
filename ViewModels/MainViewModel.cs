using CommunityToolkit.Mvvm.ComponentModel;
using CommunityToolkit.Mvvm.Input;
using System.Collections.Generic;
using System.Diagnostics;
using System.IO.Ports;
using System.Linq;
using System.Windows.Input;

namespace sarto_aquarium_hmi.ViewModels
{
    class MainViewModel : ObservableObject
    {
        public string Temperature { get; set; } = string.Empty;
        public List<string> PortNames { get; set; }

        public ICommand OpenCOM { get; set; }
        public ICommand CloseCOM { get; set; }

        public MainViewModel()
        {
            Temperature = "XX.X °C";
            PortNames = SerialPort.GetPortNames().ToList();
            OpenCOM = new RelayCommand(() => OnOpenCOM());
            CloseCOM = new RelayCommand(() => OnCloseCOM());
        }

        private void OnCloseCOM()
        {
            Debug.WriteLine("Closing COmport!!");

            //port.DataReceived -= Port_DataReceived;
            //port.Close();
        }

        private void OnOpenCOM()
        {
            Debug.WriteLine("Open COM!!!11");

            //port.DataReceived += Port_DataReceived;
            //port.Open();

            //private void Port_DataReceived(object sender, SerialDataReceivedEventArgs e)
            //{
            //    string TemperatureText = "Temperature: " + port.ReadExisting() + " °C";

            //    // Bei Änderungen von UI-Elementen von anderem Thread muss das hier aufgerufen werden, sonst Error
            //    this.Dispatcher.Invoke(() =>
            //    {
            //        TextTemperature.Text = TemperatureText;
            //    });
            //}
        }
    }
}
