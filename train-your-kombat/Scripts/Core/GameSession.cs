using Godot;
using System;

public partial class GameSession : Node
{
    private TelemetryLogger _telemetry;
    private TimerService _timer;

    private MinigameBase _activeMinigame;
    private string _sessionId;

    public override void _Ready()
    {
        _telemetry = GetNode<TelemetryLogger>("TelemetryLogger");
        _timer = new TimerService();
        AddChild(_timer);

        _sessionId = Guid.NewGuid().ToString();
        _timer.StartSession();
        _telemetry.StartSession(_sessionId);

        var antiAirReactionTest = GetNode<AntiAirController>("AntiAir");
        StartMinigame(antiAirReactionTest);

        GD.Print($"Session started: {_sessionId}");
    }

    public void StartMinigame(MinigameBase minigame)
    {
        _activeMinigame = minigame;
        _activeMinigame.Initialize(_telemetry, _timer, EndMinigame);

        _telemetry.LogEvent(new TelemetryEvent
        {
            SessionId = _sessionId,
            MinigameId = minigame.MinigameId,
            EventType = TelemetryEventTypes.MinigameStart,
            TimestampMs = _timer.GetElapsedMs(),
            PayloadJson = "{}"
        });

        _activeMinigame.StartMinigame();
    }

    public void EndMinigame()
    {
        if (_activeMinigame == null)
        {
            return;
        }

        _telemetry.LogEvent(new TelemetryEvent
        {
            SessionId = _sessionId,
            MinigameId = _activeMinigame.MinigameId,
            EventType = TelemetryEventTypes.MinigameEnd,
            TimestampMs = _timer.GetElapsedMs(),
            PayloadJson = "{}"
        });

        _activeMinigame.EndMinigame();
    }
}
