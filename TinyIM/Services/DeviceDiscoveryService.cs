using System.Collections.ObjectModel;
using TinyIM.Models;

namespace TinyIM.Services;

public class DeviceDiscoveryService
{
    private readonly ObservableCollection<LanDevice> _devices = new();
    private static DeviceDiscoveryService? _instance;
    
    public static DeviceDiscoveryService Instance => _instance ??= new DeviceDiscoveryService();
    
    public ObservableCollection<LanDevice> Devices => _devices;
    
    private DeviceDiscoveryService()
    {
        // Initialize with mock data for demonstration
        InitializeMockDevices();
    }
    
    private void InitializeMockDevices()
    {
        _devices.Add(new LanDevice
        {
            Name = "Windows PC",
            Platform = Models.DevicePlatform.Windows,
            IpAddress = "192.168.1.100",
            Avatar = "dotnet_bot.png"
        });
        
        _devices.Add(new LanDevice
        {
            Name = "Android Phone",
            Platform = Models.DevicePlatform.Android,
            IpAddress = "192.168.1.101",
            Avatar = "dotnet_bot.png"
        });
        
        _devices.Add(new LanDevice
        {
            Name = "iPhone",
            Platform = Models.DevicePlatform.iOS,
            IpAddress = "192.168.1.102",
            Avatar = "dotnet_bot.png"
        });
        
        _devices.Add(new LanDevice
        {
            Name = "MacBook Pro",
            Platform = Models.DevicePlatform.Mac,
            IpAddress = "192.168.1.103",
            Avatar = "dotnet_bot.png"
        });
    }
    
    public void StartDiscovery()
    {
        // TODO: Implement actual UDP broadcast/multicast discovery
        // For now, using mock data
    }
    
    public void StopDiscovery()
    {
        // TODO: Implement stopping discovery
    }
}
