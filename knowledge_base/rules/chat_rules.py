from experta import Rule, MATCH, TEST, NOT
from ..facts import Symptom, SystemInfo, Diagnosis

class ChatRules:
    @Rule(
            Symptom(type="chat", description="messages_not_sending"),
            SystemInfo(connection_type=MATCH.conn),
            TEST(lambda conn: conn in ("cellular", "slow_wifi"))
        )
    def chat_network_send(self, conn):
        self.declare(Diagnosis(
            problem_type="chat",
            cause="network",
            solution="Tu red está inestable. Cambiá a WiFi/ethernet estables y reintentá.",
            confidence=0.75
        ))

    # Mensajes no salen con red buena: refresco/cerrar sesión
    @Rule(
        Symptom(type="chat", description="messages_not_sending"),
        SystemInfo(connection_type=MATCH.conn),
        TEST(lambda conn: conn in ("wifi", "ethernet"))
    )
    def chat_local_send(self, conn):
        self.declare(Diagnosis(
            problem_type="chat",
            cause="browser",
            solution="Actualizá la página o cerrá sesión y volvé a ingresar; probá desactivar extensiones.",
            confidence=0.60
        ))

    @Rule(Symptom(type="chat", description="cannot_see_messages"))
    def chat_cannot_see(self):
        self.declare(Diagnosis(
            problem_type="chat",
            cause="permissions",
            solution="Revisá tu rol/inscripción en el curso; si persiste, informá al docente/soporte.",
            confidence=0.75
        ))

    @Rule(Symptom(type="chat", description="notification_issues"))
    def chat_notifications(self):
        self.declare(Diagnosis(
            problem_type="chat",
            cause="browser",
            solution="Activá notificaciones del sitio en el navegador y en el sistema operativo; verificá “No molestar”.",
            confidence=0.70
        ))

    # Emojis no funcionan (compatibilidad del navegador)
    @Rule(
        Symptom(type="chat", description="emoji_not_working"),
        SystemInfo(browser=MATCH.br),
        TEST(lambda br: br in ("IE", "Other"))
    )
    def chat_emoji_browser(self, br):
        self.declare(Diagnosis(
            problem_type="chat",
            cause="browser",
            solution="El navegador no soporta emojis modernos. Probá Chrome, Firefox o Edge.",
            confidence=0.75
        ))

    @Rule(
        Symptom(type="chat", description="chat_lag"),
        SystemInfo(connection_type=MATCH.conn),
        TEST(lambda conn: conn in ("cellular", "slow_wifi"))
    )
    def chat_lag_network(self, conn):
        self.declare(Diagnosis(
            problem_type="chat",
            cause="network",
            solution="Cerrá descargas/streaming paralelos y pasate a una red más estable (o cable).",
            confidence=0.70
        ))

    @Rule(Symptom(type="chat"), NOT(Diagnosis(problem_type="chat")))
    def fb_chat(self):
        self.declare(Diagnosis(
            problem_type="chat",
            cause="unknown",
            solution="Refrescá la página, revisá notificaciones y probá otra red/navegador.",
            confidence=0.40
        ))