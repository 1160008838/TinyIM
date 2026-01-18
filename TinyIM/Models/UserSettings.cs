namespace TinyIM.Models;

public class UserSettings
{
    // Personal Information
    public string UserName { get; set; } = "User";
    public string UserAvatar { get; set; } = "dotnet_bot.png";
    public string DeviceName { get; set; } = DeviceInfo.Name;
    
    // Network Settings
    public bool AutoDiscovery { get; set; } = true;
    public int DiscoveryPort { get; set; } = 8888;
    public string NetworkInterface { get; set; } = "Auto";
    
    // Storage Settings
    public string DownloadPath { get; set; } = FileSystem.AppDataDirectory;
    public long MaxStorageSize { get; set; } = 1024 * 1024 * 100; // 100MB
    public bool AutoCleanup { get; set; } = true;
}
