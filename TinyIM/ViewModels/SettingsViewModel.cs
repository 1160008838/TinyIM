using System.ComponentModel;
using System.Runtime.CompilerServices;
using System.Windows.Input;
using TinyIM.Models;

namespace TinyIM.ViewModels;

public class SettingsViewModel : INotifyPropertyChanged
{
    private UserSettings _settings = new();

    public string UserName
    {
        get => _settings.UserName;
        set
        {
            _settings.UserName = value;
            OnPropertyChanged();
        }
    }

    public string DeviceName
    {
        get => _settings.DeviceName;
        set
        {
            _settings.DeviceName = value;
            OnPropertyChanged();
        }
    }

    public bool AutoDiscovery
    {
        get => _settings.AutoDiscovery;
        set
        {
            _settings.AutoDiscovery = value;
            OnPropertyChanged();
        }
    }

    public int DiscoveryPort
    {
        get => _settings.DiscoveryPort;
        set
        {
            _settings.DiscoveryPort = value;
            OnPropertyChanged();
        }
    }

    public string NetworkInterface
    {
        get => _settings.NetworkInterface;
        set
        {
            _settings.NetworkInterface = value;
            OnPropertyChanged();
        }
    }

    public string DownloadPath
    {
        get => _settings.DownloadPath;
        set
        {
            _settings.DownloadPath = value;
            OnPropertyChanged();
        }
    }

    public bool AutoCleanup
    {
        get => _settings.AutoCleanup;
        set
        {
            _settings.AutoCleanup = value;
            OnPropertyChanged();
        }
    }

    public long MaxStorageSizeMB
    {
        get => _settings.MaxStorageSize / (1024 * 1024);
        set
        {
            _settings.MaxStorageSize = value * 1024 * 1024;
            OnPropertyChanged();
        }
    }

    public ICommand SaveSettingsCommand { get; }

    public SettingsViewModel()
    {
        SaveSettingsCommand = new Command(SaveSettings);
    }

    private async void SaveSettings()
    {
        // TODO: Implement actual settings persistence
        if (Application.Current?.Windows.Count > 0)
        {
            await Application.Current.Windows[0].Page!.DisplayAlertAsync("成功", "设置已保存", "确定");
        }
    }

    public event PropertyChangedEventHandler? PropertyChanged;

    protected void OnPropertyChanged([CallerMemberName] string? propertyName = null)
    {
        PropertyChanged?.Invoke(this, new PropertyChangedEventArgs(propertyName));
    }
}
