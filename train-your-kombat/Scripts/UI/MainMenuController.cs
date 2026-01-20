using Godot;
using System.Linq;

public partial class MainMenuController : Node
{
    private Label _minigameNameLabel;
    private Label _descriptionLabel;
    private Button _previousButton;
    private Button _nextButton;
    private Button _startButton;

    private int _currentIndex = 0;
    private MinigameDescriptor[] _minigames;

    public override void _Ready()
    {
        _minigameNameLabel = GetParent().GetNode<Label>("CenterContainer/VBoxContainer/MinigameNameLabel");
        _descriptionLabel = GetParent().GetNode<Label>("CenterContainer/VBoxContainer/DescriptionLabel");
        _previousButton = GetParent().GetNode<Button>("CenterContainer/VBoxContainer/HBoxContainer/PreviousButton");
        _nextButton = GetParent().GetNode<Button>("CenterContainer/VBoxContainer/HBoxContainer/NextButton");
        _startButton = GetParent().GetNode<Button>("CenterContainer/VBoxContainer/HBoxContainer/StartButton");

        _previousButton.Pressed += OnPreviousPressed;
        _nextButton.Pressed += OnNextPressed;
        _startButton.Pressed += OnStartPressed;

        LoadMinigames();
        UpdateDisplay();
    }

    private void LoadMinigames()
    {
        var registry = MinigameRegistry.Instance;
        if (registry == null)
        {
            GD.PrintErr("MinigameRegistry not found!");
            return;
        }

        var minigameList = registry.GetAllMinigames();
        _minigames = minigameList.ToArray();
    }

    private void OnPreviousPressed()
    {
        if (_minigames == null || _minigames.Length == 0) return;

        _currentIndex = (_currentIndex - 1 + _minigames.Length) % _minigames.Length;
        UpdateDisplay();
    }

    private void OnNextPressed()
    {
        if (_minigames == null || _minigames.Length == 0) return;

        _currentIndex = (_currentIndex + 1) % _minigames.Length;
        UpdateDisplay();
    }

    private void OnStartPressed()
    {
        if (_minigames == null || _minigames.Length == 0) return;

        var selectedMinigame = _minigames[_currentIndex];
        GetTree().ChangeSceneToFile(selectedMinigame.ScenePath);
    }

    private void UpdateDisplay()
    {
        if (_minigames == null || _minigames.Length == 0)
        {
            _minigameNameLabel.Text = "No minigames available";
            _descriptionLabel.Text = "";
            return;
        }

        var current = _minigames[_currentIndex];
        _minigameNameLabel.Text = current.DisplayName;
        _descriptionLabel.Text = current.ShortDescription;
    }
}