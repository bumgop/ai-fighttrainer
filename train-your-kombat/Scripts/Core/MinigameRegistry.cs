using Godot;
using System.Collections.Generic;
using System.Linq;

public partial class MinigameRegistry : Node
{
    private static MinigameRegistry _instance;
    public static MinigameRegistry Instance => _instance;

    private readonly List<MinigameDescriptor> _minigames = new();

    public override void _Ready()
    {
        _instance = this;
        RegisterMinigames();
    }

    private void RegisterMinigames()
    {
        _minigames.Add(new MinigameDescriptor
        {
            MinigameId = "anti_air_reaction_test",
            DisplayName = "Anti-Air Reaction Test",
            ScenePath = "res://Scenes/Minigames/AntiAir.tscn",
            ShortDescription = "Test your timing for anti-air attacks"
        });

        _minigames.Add(new MinigameDescriptor
        {
            MinigameId = "hit_confirm_test",
            DisplayName = "Hit-Confirm Challenge",
            ScenePath = "res://Scenes/Minigames/HitConfirm.tscn",
            ShortDescription = "Practice decision-making under uncertainty"
        });

        _minigames.Add(new MinigameDescriptor
        {
            MinigameId = "whiff_punish_test",
            DisplayName = "Whiff Punish Timing",
            ScenePath = "res://Scenes/Minigames/WhiffPunish.tscn",
            ShortDescription = "Learn to punish whiffed attacks during recovery"
        });

        _minigames.Add(new MinigameDescriptor
        {
            MinigameId = "defense_under_pressure_test",
            DisplayName = "Defense Under Pressure",
            ScenePath = "res://Scenes/Minigames/DefenseUnderPressure.tscn",
            ShortDescription = "Block mixed attack strings correctly"
        });
    }

    public List<MinigameDescriptor> GetAllMinigames()
    {
        return _minigames.ToList();
    }

    public MinigameDescriptor GetMinigameById(string minigameId)
    {
        return _minigames.FirstOrDefault(m => m.MinigameId == minigameId);
    }
}