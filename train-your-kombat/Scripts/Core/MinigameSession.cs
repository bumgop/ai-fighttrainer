using Godot;
using System.Linq;

public partial class MinigameSession : Node
{
    private TelemetryLogger _telemetry;
    private TimerService _timer;
    private MinigameBase _activeMinigame;
    private string _sessionId;
    private Control _returnButton;

    public override void _Ready()
    {
        _telemetry = GetNode<TelemetryLogger>("TelemetryLogger");
        _timer = new TimerService();
        AddChild(_timer);

        _sessionId = System.Guid.NewGuid().ToString();
        _timer.StartSession();
        _telemetry.StartSession(_sessionId);

        CreateReturnButton();
        StartMinigameWithDelay();
    }

    private void CreateReturnButton()
    {
        _returnButton = new Control();
        _returnButton.SetAnchorsAndOffsetsPreset(Control.LayoutPreset.BottomRight);
        _returnButton.Position = new Vector2(-120, -50);
        _returnButton.Size = new Vector2(100, 30);

        var button = new Button();
        button.Text = "Return to Menu";
        button.Size = new Vector2(100, 30);
        button.Pressed += ReturnToMenu;
        button.Visible = false;

        _returnButton.AddChild(button);
        AddChild(_returnButton);
    }

    private void StartMinigameWithDelay()
    {
        GetTree().CreateTimer(1.0).Timeout += StartMinigame;
    }

    private void StartMinigame()
    {
        _activeMinigame = GetChildren().OfType<MinigameBase>().FirstOrDefault();
        if (_activeMinigame == null)
        {
            GD.PrintErr("No minigame found in scene!");
            return;
        }

        _activeMinigame.Initialize(_telemetry, _timer, OnMinigameComplete);
        _activeMinigame.SetSessionId(_sessionId);

        _telemetry.LogEvent(new TelemetryEvent
        {
            SessionId = _sessionId,
            MinigameId = _activeMinigame.MinigameId,
            EventType = TelemetryEventTypes.MinigameStart,
            TimestampMs = _timer.GetElapsedMs(),
            PayloadJson = "{}"
        });

        _activeMinigame.StartMinigame();
    }

    private void OnMinigameComplete()
    {
        if (_activeMinigame == null) return;

        _telemetry.LogEvent(new TelemetryEvent
        {
            SessionId = _sessionId,
            MinigameId = _activeMinigame.MinigameId,
            EventType = TelemetryEventTypes.MinigameEnd,
            TimestampMs = _timer.GetElapsedMs(),
            PayloadJson = "{}"
        });

        _activeMinigame.EndMinigame();
        ShowReturnButton();
    }

    private void ShowReturnButton()
    {
        var button = _returnButton.GetChild<Button>(0);
        button.Visible = true;
    }

    private void ReturnToMenu()
    {
        GetTree().ChangeSceneToFile("res://Scenes/MainMenu.tscn");
    }
}