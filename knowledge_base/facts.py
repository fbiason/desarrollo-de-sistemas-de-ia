from experta import Fact, Field

class Symptom(Fact):
    """Represents a symptom or problem reported by the user."""
    type = Field(str, mandatory=True)  # Type of symptom (login, video, chat, etc.)
    description = Field(str, mandatory=True)  # Detailed description
    severity = Field(str, default="medium")  # low, medium, high
    frequency = Field(str, default="sometimes")  # rarely, sometimes, always
    
class SystemInfo(Fact):
    """Information about the user's system."""
    browser = Field(str, default=None)
    browser_version = Field(str, default=None)
    operating_system = Field(str, default=None)
    device_type = Field(str, default=None)  # desktop, mobile, tablet
    connection_type = Field(str, default=None)  # wifi, ethernet, cellular
    
class ServerStatus(Fact):
    """Information about the server status."""
    is_online = Field(bool, default=True)
    response_time = Field(int, default=None)  # in milliseconds
    last_maintenance = Field(str, default=None)  # date of last maintenance
    reported_issues = Field(int, default=0)  # number of reported issues
    
class Diagnosis(Fact):
    """The result of the expert system's analysis."""
    problem_type = Field(str, mandatory=True)
    cause = Field(str, mandatory=True)
    solution = Field(str, mandatory=True)
    confidence = Field(float, default=0.0)  # 0.0 to 1.0

# Predefined symptoms that the system can recognize
LOGIN_SYMPTOMS = [
    "cannot_login",
    "forgot_password",
    "account_locked",
    "invalid_credentials",
    "registration_failed"
]

VIDEO_SYMPTOMS = [
    "video_not_loading",
    "video_buffering",
    "video_quality_poor",
    "audio_issues",
    "playback_controls_not_working"
]

CHAT_SYMPTOMS = [
    "messages_not_sending",
    "cannot_see_messages",
    "notification_issues",
    "emoji_not_working",
    "chat_lag"
]

CONTENT_SYMPTOMS = [
    "content_not_loading",
    "missing_files",
    "broken_links",
    "formatting_issues",
    "access_denied_to_content"
]

# Causes categorized by source
CAUSES = {
    "server": [
        "server_down",
        "maintenance_in_progress",
        "database_issues",
        "high_traffic",
        "api_failure"
    ],
    "browser": [
        "incompatible_browser",
        "outdated_browser",
        "cache_issues",
        "cookie_problems",
        "extension_conflict"
    ],
    "user": [
        "incorrect_credentials",
        "network_issues",
        "device_limitations",
        "permission_issues",
        "user_error"
    ]
}
