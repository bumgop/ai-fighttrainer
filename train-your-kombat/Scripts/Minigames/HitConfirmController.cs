using Godot;
using System;
using System.Text.Json;

public partial class HitConfirmController : MinigameBase
{
    public override string MinigameId => "hit_confirm_test";

    private ColorRect _opponent;
    private Label _label;

    private bool _active;
    private bool _inputHandled;
    private bool _isHitState;

    private double _cueStartMs;
    private const double InputWindowMs = 500;

    public override void _Ready()
    {
        _opponent = GetNode<ColorRect>("Opponent");
        _label = GetNode<Label>("Label");
    }

    public override void StartMinigame()
    {
        _label.Text = "Wait for the cue...";
        _inputHandled = false;
        _active = false;
        _opponent.Color = Colors.Gray;

        GetTree().CreateTimer(GD.RandRange(1.0f, 3.0f)).Timeout += ShowCue;
    }

    private void ShowCue()
    {
        _isHitState = GD.Randf() > 0.5f;
        _cueStartMs = Timer.GetElapsedMs();
        _active = true;

        if (_isHitState)
        {
            _opponent.Color = Colors.Green;
            _label.Text = "HIT - Confirm!";
        }
        else
        {
            _opponent.Color = Colors.Red;
            _label.Text = "BLOCK - Don't attack!";
        }

        GetTree().CreateTimer(InputWindowMs / 1000.0).Timeout += TimeExpired;
    }

    private void TimeExpired()
    {
        if (_inputHandled) return;

        _inputHandled = true;
        string result = _isHitState ? "missed_hit_confirm" : "correct_block";
        _label.Text = _isHitState ? "Missed confirm!" : "Good block!";

        LogResult(result, null);
        RequestEnd();
    }

    public override void _Process(double delta)
    {
        if (!_active || _inputHandled) return;

        CheckInput();
    }

    private void CheckInput()
    {
        if (Input.IsActionJustPressed("front_punch"))
        {
            _inputHandled = true;
            var timingMs = Timer.GetElapsedMs() - _cueStartMs;

            string result;
            if (_isHitState)
            {
                result = "correct_hit_confirm";
                _label.Text = "Good confirm!";
            }
            else
            {
                result = "false_hit_confirm";
                _label.Text = "Wrong! That was blocked!";
            }

            LogResult(result, timingMs);
            RequestEnd();
        }
    }

    private void LogResult(string result, double? timingMs)
    {
        Telemetry.LogEvent(new TelemetryEvent
        {
            SessionId = SessionId,
            MinigameId = MinigameId,
            EventType = "hit_confirm_attempt",
            TimestampMs = Timer.GetElapsedMs(),
            PayloadJson = JsonSerializer.Serialize(new
            {
                outcome = result,
                timing_ms = timingMs,
                was_hit_state = _isHitState
            })
        });
    }

    public override void EndMinigame()
    {
        _active = false;
    }
}