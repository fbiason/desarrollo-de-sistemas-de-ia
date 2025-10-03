from experta import Rule, AND, OR, NOT, MATCH, TEST
from .facts import Symptom, SystemInfo, ServerStatus, Diagnosis
from .facts import LOGIN_SYMPTOMS, VIDEO_SYMPTOMS, CHAT_SYMPTOMS, CONTENT_SYMPTOMS, CAUSES

class EdTechRules:
    """Rules for the EdTech Expert System."""
    
    # LOGIN PROBLEM RULES
    
    @Rule(
        Symptom(type="login", description=MATCH.desc),
        TEST(lambda desc: desc == "cannot_login" or desc == "invalid_credentials"),
        ServerStatus(is_online=True)
    )
    def login_credentials_issue(self):
        self.declare(Diagnosis(
            problem_type="login",
            cause="user",
            solution="Verify that you're using the correct username and password. If you've forgotten your password, use the 'Forgot Password' option.",
            confidence=0.8
        ))
    
    @Rule(
        Symptom(type="login", description=MATCH.desc),
        TEST(lambda desc: desc == "cannot_login"),
        ServerStatus(is_online=False)
    )
    def login_server_down(self):
        self.declare(Diagnosis(
            problem_type="login",
            cause="server",
            solution="The server appears to be down. Please wait and try again later, or contact support if the problem persists.",
            confidence=0.9
        ))
    
    @Rule(
        Symptom(type="login", description="account_locked")
    )
    def login_account_locked(self):
        self.declare(Diagnosis(
            problem_type="login",
            cause="user",
            solution="Your account may be locked due to multiple failed login attempts. Contact the administrator to unlock your account.",
            confidence=0.9
        ))
    
    @Rule(
        Symptom(type="login", description=MATCH.desc),
        TEST(lambda desc: desc in LOGIN_SYMPTOMS),
        SystemInfo(browser=MATCH.browser),
        TEST(lambda browser: browser in ["Internet Explorer", "IE"])
    )
    def login_incompatible_browser(self):
        self.declare(Diagnosis(
            problem_type="login",
            cause="browser",
            solution="You're using an outdated or incompatible browser. Please try using Chrome, Firefox, or Edge.",
            confidence=0.7
        ))
    
    # VIDEO PROBLEM RULES
    
    @Rule(
        Symptom(type="video", description="video_not_loading"),
        SystemInfo(connection_type=MATCH.conn),
        TEST(lambda conn: conn == "cellular" or conn == "slow_wifi")
    )
    def video_slow_connection(self):
        self.declare(Diagnosis(
            problem_type="video",
            cause="user",
            solution="Your internet connection may be too slow for video streaming. Try connecting to a faster network or reducing the video quality in settings.",
            confidence=0.8
        ))
    
    @Rule(
        Symptom(type="video", description=MATCH.desc),
        TEST(lambda desc: desc in ["video_buffering", "video_quality_poor"]),
        ServerStatus(response_time=MATCH.time),
        TEST(lambda time: time and time > 1000)  # Response time > 1000ms
    )
    def video_server_overload(self):
        self.declare(Diagnosis(
            problem_type="video",
            cause="server",
            solution="The server is experiencing high load. Try watching the video during off-peak hours or contact support.",
            confidence=0.7
        ))
    
    @Rule(
        Symptom(type="video", description=MATCH.desc),
        TEST(lambda desc: desc in VIDEO_SYMPTOMS),
        SystemInfo(browser=MATCH.browser, browser_version=MATCH.version),
        TEST(lambda browser, version: browser == "Chrome" and version and float(version.split('.')[0]) < 80)
    )
    def video_outdated_browser(self):
        self.declare(Diagnosis(
            problem_type="video",
            cause="browser",
            solution="Your browser version is outdated. Update your browser to the latest version for better video playback.",
            confidence=0.8
        ))
    
    # CHAT PROBLEM RULES
    
    @Rule(
        Symptom(type="chat", description="messages_not_sending"),
        ServerStatus(is_online=True)
    )
    def chat_connection_issue(self):
        self.declare(Diagnosis(
            problem_type="chat",
            cause="user",
            solution="Check your internet connection and refresh the page. If the problem persists, try logging out and back in.",
            confidence=0.6
        ))
    
    @Rule(
        Symptom(type="chat", description=MATCH.desc),
        TEST(lambda desc: desc in ["chat_lag", "messages_not_sending"]),
        ServerStatus(reported_issues=MATCH.issues),
        TEST(lambda issues: issues > 5)
    )
    def chat_server_issues(self):
        self.declare(Diagnosis(
            problem_type="chat",
            cause="server",
            solution="The chat server is experiencing issues. Please be patient and try again later.",
            confidence=0.8
        ))
    
    @Rule(
        Symptom(type="chat", description="emoji_not_working"),
        SystemInfo(browser=MATCH.browser)
    )
    def chat_emoji_browser_issue(self):
        self.declare(Diagnosis(
            problem_type="chat",
            cause="browser",
            solution="Your browser may not support all emoji features. Try updating your browser or using a different one.",
            confidence=0.7
        ))
    
    # CONTENT PROBLEM RULES
    
    @Rule(
        Symptom(type="content", description="content_not_loading"),
        SystemInfo(browser=MATCH.browser),
        TEST(lambda browser: browser in ["Chrome", "Firefox", "Edge", "Safari"])
    )
    def content_browser_cache(self):
        self.declare(Diagnosis(
            problem_type="content",
            cause="browser",
            solution="Try clearing your browser cache and cookies, then reload the page.",
            confidence=0.7
        ))
    
    @Rule(
        Symptom(type="content", description="access_denied_to_content")
    )
    def content_permission_issue(self):
        self.declare(Diagnosis(
            problem_type="content",
            cause="user",
            solution="You may not have the necessary permissions to access this content. Contact your instructor or administrator.",
            confidence=0.9
        ))
    
    @Rule(
        Symptom(type="content", description=MATCH.desc),
        TEST(lambda desc: desc in ["broken_links", "missing_files"]),
        ServerStatus(last_maintenance=MATCH.maint),
        TEST(lambda maint: maint and "recent" in maint.lower())
    )
    def content_recent_maintenance(self):
        self.declare(Diagnosis(
            problem_type="content",
            cause="server",
            solution="The system recently underwent maintenance which may have affected some content. Contact support with specific details about the missing content.",
            confidence=0.8
        ))
    
    # DEFAULT RULES (when no specific rule matches)
    
    @Rule(
        Symptom(type=MATCH.type),
        NOT(Diagnosis(problem_type=MATCH.type))
    )
    def unknown_issue(self, type):
        self.declare(Diagnosis(
            problem_type=type,
            cause="unknown",
            solution="We couldn't identify the specific cause of this issue. Please contact technical support with details about your problem.",
            confidence=0.3
        ))
