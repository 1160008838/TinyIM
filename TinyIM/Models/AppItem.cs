namespace TinyIM.Models;

public class AppItem
{
    public string Id { get; set; } = Guid.NewGuid().ToString();
    public string Name { get; set; } = string.Empty;
    public string Icon { get; set; } = "dotnet_bot.png";
    public string Description { get; set; } = string.Empty;
}
