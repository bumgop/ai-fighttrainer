using Godot;
using System;
using System.Text.Json;

public partial class WhiffPunishController : MinigameBase
{
    public override string MinigameId => "whiff_punish_test";

    private ColorRect _enemy;
    private Label _label;
    private ColorRect _progress;

    private bool _active;
    private bool _inputHandled;

    private double _attackStartMs;
    private double _startupEndMs;
    private double _activeEndMs;
    private double _recoveryEndMs;

    private const double StartupDurationMs = 200;
    private const double ActiveDurationMs = 150;
    private const double RecoveryDurationMs = 300;
    private const double TotalDurationMs = StartupDurationMs + ActiveDurationMs + RecoveryDurationMs;
    private const float BarWidth = 200f;

    private enum AttackPhase
    {
        Startup,
        Active,
        Recovery,
        PostRecovery
    }

    public override void _Ready()
    {
        _enemy = GetNode<ColorRect>("Enemy");
        _label = GetNode<Label>("Label");
        _progress = GetNode<ColorRect>("FrameBar/Progress");
    }

    public override void StartMinigame()
    {
        _label.Text = "Wait for the attack...";
        _inputHandled = false;
        _active = false;
        _enemy.Color = Colors.Gray;
        _progress.Size = new Vector2(0, _progress.Size.Y);

        GetTree().CreateTimer(GD.RandRange(1.0f, 3.0f)).Timeout += StartAttack;
    }

    private void StartAttack()
    {
        _attackStartMs = Timer.GetElapsedMs();
        _startupEndMs = _attackStartMs + StartupDurationMs;
        _activeEndMs = _startupEndMs + ActiveDurationMs;
        _recoveryEndMs = _activeEndMs + RecoveryDurationMs;

        _active = true;
        _enemy.Color = Colors.Yellow;
        _label.Text = "Startup...";

        GetTree().CreateTimer((RecoveryDurationMs + 500) / 1000.0).Timeout += EndMinigameIfNoInput;
    }

    private void EndMinigameIfNoInput()
    {
        if (_inputHandled) return;

        _inputHandled = true;
        LogResult("missed_punish", null, AttackPhase.PostRecovery, null);
        _label.Text = "Missed punish!";
        RequestEnd();
    }

    public override void _Process(double delta)
    {
        if (!_active || _inputHandled) return;

        UpdateVisualState();
        CheckInput();
    }

    private void UpdateVisualState()
    {
        var currentTime = Timer.GetElapsedMs();
        var phase = GetCurrentPhase(currentTime);
        var elapsed = currentTime - _attackStartMs;
        var progress = Math.Min(elapsed / TotalDurationMs, 1.0);
        _progress.Size = new Vector2((float)(progress * BarWidth), _progress.Size.Y);

        switch (phase)
        {
            case AttackPhase.Startup:
                _enemy.Color = Colors.Yellow;
                _label.Text = "Startup...";
                break;
            case AttackPhase.Active:
                _enemy.Color = Colors.Red;
                _label.Text = "Active - Don't attack!";
                break;
            case AttackPhase.Recovery:
                _enemy.Color = Colors.Green;
                _label.Text = "Recovery - Punish now!";
                break;
            case AttackPhase.PostRecovery:
                _enemy.Color = Colors.Gray;
                _label.Text = "Too late!";
                break;
        }
    }

    private AttackPhase GetCurrentPhase(double currentTime)
    {
        if (currentTime < _startupEndMs)
            return AttackPhase.Startup;
        if (currentTime < _activeEndMs)
            return AttackPhase.Active;
        if (currentTime < _recoveryEndMs)
            return AttackPhase.Recovery;
        return AttackPhase.PostRecovery;
    }

    private void CheckInput()
    {
        if (Input.IsActionJustPressed("front_punch"))
        {
            _inputHandled = true;
            var inputTime = Timer.GetElapsedMs();
            var phase = GetCurrentPhase(inputTime);

            string result;
            double? windowOffsetMs = null;

            switch (phase)
            {
                case AttackPhase.Startup:
                    result = "early_whiff_punish";
                    _label.Text = "Too early!";
                    break;
                case AttackPhase.Active:
                    result = "unsafe_whiff_punish";
                    _label.Text = "Unsafe! Got hit!";
                    break;
                case AttackPhase.Recovery:
                    result = "correct_whiff_punish";
                    windowOffsetMs = inputTime - _activeEndMs;
                    _label.Text = "Good punish!";
                    break;
                case AttackPhase.PostRecovery:
                    result = "late_whiff_punish";
                    _label.Text = "Too late!";
                    break;
                default:
                    result = "unknown";
                    break;
            }

            LogResult(result, inputTime, phase, windowOffsetMs);
            RequestEnd();
        }
    }

    private void LogResult(string outcome, double? inputTimeMs, AttackPhase phaseAtInput, double? windowOffsetMs)
    {
        Telemetry.LogEvent(new TelemetryEvent
        {
            SessionId = SessionId,
            MinigameId = MinigameId,
            EventType = "whiff_punish_attempt",
            TimestampMs = Timer.GetElapsedMs(),
            PayloadJson = JsonSerializer.Serialize(new
            {
                outcome = outcome,
                input_time_ms = inputTimeMs,
                phase_at_input = phaseAtInput.ToString().ToLower(),
                window_offset_ms = windowOffsetMs
            })
        });
    }

    public override void EndMinigame()
    {
        _active = false;
    }
}