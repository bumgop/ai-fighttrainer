using Godot;
using System;

public abstract partial class MinigameBase : Node
{
    public abstract string MinigameId { get; }

    protected TelemetryLogger Telemetry;
    protected TimerService Timer;
    protected Action RequestEnd;
    protected string SessionId;

    public virtual void Initialize(TelemetryLogger telemetry, TimerService timer, Action requestEnd)
    {
        Telemetry = telemetry;
        Timer = timer;
        RequestEnd = requestEnd;
    }

    public void SetSessionId(string sessionId)
    {
        SessionId = sessionId;
    }

    public abstract void StartMinigame();
    public abstract void EndMinigame();
}