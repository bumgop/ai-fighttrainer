using Godot;

public partial class RegistryTestController : Node
{
    public override void _Ready()
    {
        // Wait for registry to initialize
        GetTree().CreateTimer(0.1).Timeout += TestRegistry;
    }

    private void TestRegistry()
    {
        var registry = MinigameRegistry.Instance;
        if (registry == null)
        {
            GD.PrintErr("MinigameRegistry not found!");
            return;
        }

        var minigames = registry.GetAllMinigames();
        GD.Print($"Found {minigames.Count} registered minigames:");
        
        foreach (var minigame in minigames)
        {
            GD.Print($"- {minigame.DisplayName} ({minigame.MinigameId})");
        }

        // Launch the first minigame as a test
        if (minigames.Count > 0)
        {
            var launcher = GetNode<MinigameLauncher>("../MinigameLauncher");
            launcher.LaunchMinigame(minigames[0].ScenePath);
        }
    }
}