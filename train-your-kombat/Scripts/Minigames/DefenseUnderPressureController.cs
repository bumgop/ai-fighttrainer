using Godot;
using System;
using System.Collections.Generic;
using System.Text.Json;

public partial class DefenseUnderPressureController : MinigameBase
{
    public override string MinigameId => "defense_under_pressure_test";

    private ColorRect _attacker;
    private Label _label;
    private Label _attackLabel;

    private bool _active;
    private bool _stringComplete;

    private List<AttackType> _currentString;
    private int _currentAttackIndex;
    private double _attackStartMs;
    private double _impactStartMs;
    private double _impactEndMs;

    private const double StartupDurationMs = 400;
    private const double ImpactDurationMs = 200;

    private enum AttackType
    {
        Low,
        Mid, 
        High,
        Overhead
    }

    private enum DefenseType
    {
        StandBlock,
        CrouchBlock,
        Crouch,
        None
    }

    private readonly List<List<AttackType>> _attackStrings = new()
    {
        new() { AttackType.Mid, AttackType.Low },
        new() { AttackType.High, AttackType.Overhead },
        new() { AttackType.Low, AttackType.Mid, AttackType.High },
        new() { AttackType.Overhead, AttackType.Low },
        new() { AttackType.Mid, AttackType.Overhead, AttackType.Low }
    };

    public override void _Ready()
    {
        _attacker = GetNode<ColorRect>("Attacker");
        _label = GetNode<Label>("Label");
        _attackLabel = GetNode<Label>("AttackLabel");
    }

    public override void StartMinigame()
    {
        _label.Text = "Get ready to defend...";
        _attackLabel.Text = "";
        _active = false;
        _stringComplete = false;
        _attacker.Color = Colors.Gray;

        _currentString = _attackStrings[GD.RandRange(0, _attackStrings.Count)];
        _currentAttackIndex = 0;

        GetTree().CreateTimer(GD.RandRange(1.0f, 2.0f)).Timeout += StartAttackString;
    }

    private void StartAttackString()
    {
        _active = true;
        StartNextAttack();
    }

    private void StartNextAttack()
    {
        GD.Print("Starting next attack...");
        if (_currentAttackIndex >= _currentString.Count)
        {
            CompleteString();
            return;
        }

        var attack = _currentString[_currentAttackIndex];
        _attackStartMs = Timer.GetElapsedMs();
        _impactStartMs = _attackStartMs + StartupDurationMs;
        _impactEndMs = _impactStartMs + ImpactDurationMs;

        UpdateAttackVisuals(attack, false);
        _label.Text = "Defend!";

        GetTree().CreateTimer(StartupDurationMs / 1000.0).Timeout += () => UpdateAttackVisuals(attack, true);
        GetTree().CreateTimer((StartupDurationMs + ImpactDurationMs) / 1000.0).Timeout += ProcessAttackResult;
    }

    private void UpdateAttackVisuals(AttackType attack, bool isImpact)
    {
        if (isImpact)
        {
            _attacker.Color = Colors.Red;
            _attackLabel.Text = $"{attack.ToString().ToUpper()} - IMPACT!";
        }
        else
        {
            _attacker.Color = GetAttackColor(attack);
            _attackLabel.Text = $"Incoming {attack.ToString().ToUpper()}";
        }
    }

    private Color GetAttackColor(AttackType attack)
    {
        return attack switch
        {
            AttackType.Low => Colors.Blue,
            AttackType.Mid => Colors.Yellow,
            AttackType.High => Colors.Green,
            AttackType.Overhead => Colors.Purple,
            _ => Colors.Gray
        };
    }

    private void ProcessAttackResult()
    {
        GD.Print("Processing attack result...");
        var attack = _currentString[_currentAttackIndex];
        var playerDefense = GetPlayerDefenseInput();
        var validDefenses = GetValidDefenses(attack);
        var outcome = EvaluateDefense(attack, playerDefense);

        LogAttackResult(attack, validDefenses, playerDefense, outcome);

        _currentAttackIndex++;
        GetTree().CreateTimer(0.3).Timeout += StartNextAttack;

        GD.Print($"Attack processed: {attack}, Player Defense: {playerDefense}, Outcome: {outcome}");
    }

    private DefenseType GetPlayerDefenseInput()
    {
        GD.Print("Getting player defense input...");
        if (Input.IsActionPressed("crouch") && Input.IsActionPressed("block"))
            return DefenseType.CrouchBlock;
        if (Input.IsActionPressed("block"))
            return DefenseType.StandBlock;
        if (Input.IsActionPressed("crouch"))
            return DefenseType.Crouch;
        return DefenseType.None;
    }

    private string GetValidDefenses(AttackType attack)
    {
        return attack switch
        {
            AttackType.Low => "crouch_block",
            AttackType.Mid => "stand_block,crouch_block",
            AttackType.High => "stand_block,crouch_block,crouch",
            AttackType.Overhead => "stand_block",
            _ => "none"
        };
    }

    private string EvaluateDefense(AttackType attack, DefenseType defense)
    {
        return attack switch
        {
            AttackType.Low => defense == DefenseType.CrouchBlock ? "correct_block" : "hit_taken",
            AttackType.Mid => defense is DefenseType.StandBlock or DefenseType.CrouchBlock ? "correct_block" : "hit_taken",
            AttackType.High => (defense is DefenseType.StandBlock or DefenseType.CrouchBlock) || defense == DefenseType.Crouch ? 
                (defense == DefenseType.Crouch ? "correct_evade" : "correct_block") : "hit_taken",
            AttackType.Overhead => defense == DefenseType.StandBlock ? "correct_block" : "hit_taken",
            _ => "hit_taken"
        };
    }

    private void LogAttackResult(AttackType attack, string validDefenses, DefenseType actual, string outcome)
    {
        Telemetry.LogEvent(new TelemetryEvent
        {
            SessionId = "",
            MinigameId = MinigameId,
            EventType = "defense_attack_result",
            TimestampMs = Timer.GetElapsedMs(),
            PayloadJson = JsonSerializer.Serialize(new
            {
                attack_type = attack.ToString().ToLower(),
                expected_defense = validDefenses,
                player_defense_input = actual.ToString().ToLower(),
                outcome = outcome,
                input_time_ms = Timer.GetElapsedMs() - _attackStartMs,
                attack_index_in_string = _currentAttackIndex
            })
        });
    }

    private void CompleteString()
    {
        _stringComplete = true;
        _attacker.Color = Colors.Gray;
        _attackLabel.Text = "";
        _label.Text = "String complete!";

        LogStringResult();
        RequestEnd();
    }

    private void LogStringResult()
    {
        Telemetry.LogEvent(new TelemetryEvent
        {
            SessionId = "",
            MinigameId = MinigameId,
            EventType = "defense_string_complete",
            TimestampMs = Timer.GetElapsedMs(),
            PayloadJson = JsonSerializer.Serialize(new
            {
                total_hits = _currentString.Count,
                successful_defenses = 0, // Would need to track this during execution
                string_success = false   // Would need to track this during execution
            })
        });
    }

    public override void EndMinigame()
    {
        _active = false;
    }
}