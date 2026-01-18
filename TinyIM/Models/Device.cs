namespace TinyIM.Models;

public class LanDevice
{
    public string Id { get; set; } = Guid.NewGuid().ToString();
    public string Name { get; set; } = string.Empty;
    public string Avatar { get; set; } = "dotnet_bot.png";
    public DevicePlatform Platform { get; set; }
    public string IpAddress { get; set; } = string.Empty;
    public DateTime LastSeen { get; set; } = DateTime.Now;
    public bool IsOnline { get; set; } = true;
}

public enum DevicePlatform
{
    Windows,
    Android,
    iOS,
    Mac
}
