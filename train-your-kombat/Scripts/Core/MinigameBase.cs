using Godot;
using System;

public abstract partial class MinigameBase : Node
{
    public abstract string MinigameId { get; }

    protected TelemetryLogger Telemetry;
    protected TimerService Timer;
    protected Action RequestEnd;

    public virtual void Initialize(TelemetryLogger telemetry, TimerService timer, Action requestEnd)
    {
        Telemetry = telemetry;
        Timer = timer;
        RequestEnd = requestEnd;
    }

    public abstract void StartMinigame();
    public abstract void EndMinigame();
}
