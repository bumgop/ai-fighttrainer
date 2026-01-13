using Godot;
using System;

public partial class TelemetryLogger : Node
{
    public void Log(string eventName)
    {
        GD.Print($"Telemetry Event Logged: {eventName}");
    }
}
