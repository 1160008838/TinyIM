using System.Collections.ObjectModel;
using System.ComponentModel;
using System.Runtime.CompilerServices;
using TinyIM.Models;

namespace TinyIM.ViewModels;

public class ApplicationsViewModel : INotifyPropertyChanged
{
    private ObservableCollection<AppItem> _applications = new();

    public ObservableCollection<AppItem> Applications
    {
        get => _applications;
        set
        {
            _applications = value;
            OnPropertyChanged();
        }
    }

    public ApplicationsViewModel()
    {
        LoadApplications();
    }

    private void LoadApplications()
    {
        // Mock data for demonstration
        Applications = new ObservableCollection<AppItem>
        {
            new AppItem { Name = "文件传输", Icon = "dotnet_bot.png", Description = "快速传输文件" },
            new AppItem { Name = "屏幕共享", Icon = "dotnet_bot.png", Description = "共享屏幕内容" },
            new AppItem { Name = "远程桌面", Icon = "dotnet_bot.png", Description = "远程控制设备" },
            new AppItem { Name = "聊天", Icon = "dotnet_bot.png", Description = "即时通讯" },
            new AppItem { Name = "语音通话", Icon = "dotnet_bot.png", Description = "语音对话" },
            new AppItem { Name = "视频通话", Icon = "dotnet_bot.png", Description = "视频对话" },
            new AppItem { Name = "共享剪贴板", Icon = "dotnet_bot.png", Description = "同步剪贴板" },
            new AppItem { Name = "通知同步", Icon = "dotnet_bot.png", Description = "同步通知" },
            new AppItem { Name = "文件浏览", Icon = "dotnet_bot.png", Description = "浏览文件系统" },
            new AppItem { Name = "相册", Icon = "dotnet_bot.png", Description = "共享相册" },
            new AppItem { Name = "音乐", Icon = "dotnet_bot.png", Description = "共享音乐" },
            new AppItem { Name = "视频", Icon = "dotnet_bot.png", Description = "共享视频" }
        };
    }

    public event PropertyChangedEventHandler? PropertyChanged;

    protected void OnPropertyChanged([CallerMemberName] string? propertyName = null)
    {
        PropertyChanged?.Invoke(this, new PropertyChangedEventArgs(propertyName));
    }
}
