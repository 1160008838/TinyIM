using System.Collections.ObjectModel;
using System.ComponentModel;
using System.Runtime.CompilerServices;
using TinyIM.Models;
using TinyIM.Services;

namespace TinyIM.ViewModels;

public class MessagesViewModel : INotifyPropertyChanged
{
    public ObservableCollection<LanDevice> Devices { get; }

    public MessagesViewModel()
    {
        Devices = DeviceDiscoveryService.Instance.Devices;
        DeviceDiscoveryService.Instance.StartDiscovery();
    }

    public event PropertyChangedEventHandler? PropertyChanged;

    protected void OnPropertyChanged([CallerMemberName] string? propertyName = null)
    {
        PropertyChanged?.Invoke(this, new PropertyChangedEventArgs(propertyName));
    }
}
