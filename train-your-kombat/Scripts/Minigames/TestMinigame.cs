using Godot;
using System;

public partial class TestMinigame : MinigameBase
{
    public override string MinigameId => "test_minigame";

    public override void StartMinigame()
    {
        GD.Print("Test minigame started...");
    }

    public override void EndMinigame()
    {
        GD.Print("Test minigame ended.");
    }
}
