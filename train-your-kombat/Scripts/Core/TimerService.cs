using Godot;
using System;

public partial class TimerService : Node
{
    private double _sessionStartTime;

    public void StartSession()
    {
        _sessionStartTime = Time.GetTicksMsec();
    }

    public double GetElapsedMs()
    {
        return Time.GetTicksMsec() - _sessionStartTime;
    }
}
