using Godot;
using System;
using System.Text.Json;

public partial class AntiAirController : MinigameBase
{
    public override string MinigameId => "anti_air_reaction_test";

    private ColorRect _threat;
    private Label _label;

    private bool _active;
    private bool _inputHandled;

    private double _windowStartMs;
    private double _windowEndMs;

    private const float ThreatSpeed = 800f;
    private Vector2 ThreatVelocity = new Vector2(0, 0);
    private const double WindowDurationMs = 300;

    public override void _Ready()
    {
        _threat = GetNode<ColorRect>("Threat");
        _label = GetNode<Label>("Label");
    }

    public override void StartMinigame()
    {
        _label.Text = "Wait...";
        _inputHandled = false;
        _active = false;

        GetTree().CreateTimer(GD.RandRange(1.5f, 3.5f)).Timeout += SpawnThreat;
    }

    private void SpawnThreat()
    {
        _threat.Position = new Vector2(64, 520);
        ThreatVelocity = new Vector2(ThreatSpeed * .75f, -ThreatSpeed);
        _threat.Color = Colors.Red;

        _label.Text = "Read the jump";
        _active = true;
    }

    public override void _Process(double delta)
    {
        if (!_active) return;

        MoveThreat(delta);
        CheckInput();
    }

    private void MoveThreat(double delta)
    {
        var grav = 2000f;
        ThreatVelocity.Y += grav * (float)delta;
        _threat.Position += ThreatVelocity * (float)delta;

        if (_windowStartMs == 0 && _threat.Position.X > 225)
        {
            _windowStartMs = Timer.GetElapsedMs();
            _windowEndMs = _windowStartMs + WindowDurationMs;

            _threat.Color = Colors.Green;
            _label.Text = "Attack!";
        }

        if (_windowStartMs > 0 && Timer.GetElapsedMs() > _windowEndMs && !_inputHandled)
        {
            LogResult("missed", null);
            _label.Text = "Too late!";
            _threat.Color = Colors.Red;

            if (_threat.Position.Y >= 520)
            {
                _threat.Position = new Vector2(_threat.Position.X, 520);
                RequestEnd();
            }
        }
    }

    private void CheckInput()
    {
        if (_inputHandled)
        {
            return;
        }

        if (Input.IsActionJustPressed("front_punch"))
        {
            _inputHandled = true;
            var now = Timer.GetElapsedMs();

            string result;
            double? timingMs = null;

            if (_windowStartMs == 0)
            {
                result = "early";
                _label.Text = "Too early!";
            }
            else if (now > _windowEndMs)
            {
                result = "late";
                _label.Text = "Too late!";
                _threat.Color = Colors.Red;


            }
            else
            {
                result = "success";
                timingMs = now - _windowStartMs;
                _label.Text = "Success!";
            }

            LogResult(result, timingMs);
            RequestEnd();
        }
    }

    private void LogResult(string result, double? timingMs)
    {
        Telemetry.LogEvent(new TelemetryEvent
        {
            SessionId = "",
            MinigameId = MinigameId,
            EventType = "anti_air_attempt",
            TimestampMs = Timer.GetElapsedMs(),
            PayloadJson = JsonSerializer.Serialize(new
            {
                outcome = result,
                timing_ms = timingMs
            })
        });
    }

    public override void EndMinigame()
    {
        _active = false;
    }
}
