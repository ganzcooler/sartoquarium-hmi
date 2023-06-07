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
        public string WaterTemperature { get; set; } = string.Empty;
        public string THP_T { get; set; } = string.Empty;
        public string THP_H { get; set; } = string.Empty;
        public string THP_P { get; set; } = string.Empty;
        public List<string> PortNames { get; set; }

        public ICommand OpenCOM { get; set; }
        public ICommand CloseCOM { get; set; }

        public MainViewModel()
        {
            PortNames = SerialPort.GetPortNames().ToList();
            OpenCOM = new RelayCommand(() => OnOpenCOM());
            CloseCOM = new RelayCommand(() => OnCloseCOM());

            WaterTemperature = "XX.X °C";
            THP_T = "XX.X °C";
            THP_H = "XX %";
            THP_P = "XXXX mbar";
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
