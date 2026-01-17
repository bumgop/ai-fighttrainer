using Godot;
using System.IO;
using System.Text.Json;

public partial class TelemetryLogger : Node
{
    private string _filePath;
    private string _sessionId;

    public void StartSession(string sessionId)
    {
        _sessionId = sessionId;

        string relativePath = $"user://telemetry/{sessionId}.csv";
        string absolutePath = ProjectSettings.GlobalizePath(relativePath);
        string directoryPath = Path.GetDirectoryName(absolutePath);
        if (!Directory.Exists(directoryPath))
        {
            Directory.CreateDirectory(directoryPath);
        }


        _filePath = absolutePath;

        File.WriteAllText(
            _filePath,
            "session_id,minigame_id,event_type,timestamp_ms,payload\n"
        );

        GD.Print(_filePath);
    }

    public void LogEvent(TelemetryEvent evt)
    {
        var payloadEscaped = evt.PayloadJson.Replace("\"", "\"\"");

        var line =
            $"{evt.SessionId}," +
            $"{evt.MinigameId}," +
            $"{evt.EventType}," +
            $"{evt.TimestampMs}," +
            $"\"{payloadEscaped}\"\n";

        File.AppendAllText(_filePath, line);
    }
}
