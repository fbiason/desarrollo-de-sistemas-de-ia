from experta import Rule, MATCH, TEST, NOT
from ..facts import Symptom, SystemInfo, Diagnosis


class ChatRules:
    # messages_not_sending
    @Rule(
        Symptom(type="chat", description="messages_not_sending"),
        SystemInfo(browser="IE"),
    )
    def msn_send_ie(self):
        self.declare(
            Diagnosis(
                problem_type="chat",
                cause="browser",
                solution="Estás usando Internet Explorer. Cambiá a Chrome, Firefox, Edge o Safari e intentá enviar nuevamente.",
                confidence=0.95,
            )
        )

    @Rule(
        Symptom(type="chat", description="messages_not_sending"),
        SystemInfo(browser="Other"),
    )
    def msn_send_other(self):
        self.declare(
            Diagnosis(
                problem_type="chat",
                cause="browser",
                solution="Tu navegador puede no ser compatible. Usá Chrome, Firefox, Edge o Safari e intentá enviar nuevamente.",
                confidence=0.90,
            )
        )

    @Rule(
        Symptom(type="chat", description="messages_not_sending"),
        SystemInfo(browser=MATCH.br),
        TEST(lambda br: br in ("Chrome", "Firefox", "Edge", "Safari")),
        SystemInfo(connection_type=MATCH.ct),
        TEST(lambda ct: ct in ("cellular", "slow_wifi")),
    )
    def msn_send_poor_net(self, br, ct):
        self.declare(
            Diagnosis(
                problem_type="chat",
                cause="network",
                solution="La red es inestable. Cambiá a WiFi o cable, o acercate al router, y reintentá el envío.",
                confidence=0.85,
            )
        )

    @Rule(
        Symptom(type="chat", description="messages_not_sending"),
        SystemInfo(browser=MATCH.br),
        TEST(lambda br: br in ("Chrome", "Firefox", "Edge", "Safari")),
        SystemInfo(connection_type=MATCH.ct),
        TEST(lambda ct: ct in ("wifi", "ethernet")),
    )
    def msn_send_stable_net(self, br, ct):
        self.declare(
            Diagnosis(
                problem_type="chat",
                cause="browser",
                solution="Actualizá la página e iniciá sesión de nuevo. Si sigue, probá en ventana privada o desactivá extensiones.",
                confidence=0.75,
            )
        )

    # cannot_see_messages
    @Rule(
        Symptom(type="chat", description="cannot_see_messages"),
        SystemInfo(browser="IE"),
    )
    def cannot_see_ie(self):
        self.declare(
            Diagnosis(
                problem_type="chat",
                cause="browser",
                solution="Internet Explorer no es compatible. Usá Chrome, Firefox, Edge o Safari para ver los mensajes.",
                confidence=0.95,
            )
        )

    @Rule(
        Symptom(type="chat", description="cannot_see_messages"),
        SystemInfo(browser="Other"),
    )
    def cannot_see_other(self):
        self.declare(
            Diagnosis(
                problem_type="chat",
                cause="browser",
                solution="Cambiá a un navegador compatible (Chrome, Firefox, Edge o Safari) y verificá nuevamente.",
                confidence=0.90,
            )
        )

    @Rule(
        Symptom(type="chat", description="cannot_see_messages"),
        SystemInfo(browser=MATCH.br),
        TEST(lambda br: br in ("Chrome", "Firefox", "Edge", "Safari")),
        SystemInfo(connection_type=MATCH.ct),
        TEST(lambda ct: ct in ("cellular", "slow_wifi")),
    )
    def cannot_see_poor_net(self, br, ct):
        self.declare(
            Diagnosis(
                problem_type="chat",
                cause="network",
                solution="Conexión inestable. Cambiá a WiFi o Ethernet y recargá el chat.",
                confidence=0.82,
            )
        )

    @Rule(
        Symptom(type="chat", description="cannot_see_messages"),
        SystemInfo(browser=MATCH.br),
        TEST(lambda br: br in ("Chrome", "Firefox", "Edge", "Safari")),
        SystemInfo(connection_type=MATCH.ct),
        TEST(lambda ct: ct in ("wifi", "ethernet")),
    )
    def cannot_see_stable_net(self, br, ct):
        self.declare(
            Diagnosis(
                problem_type="chat",
                cause="permissions",
                solution="Revisá que tengas acceso al chat o estés inscripta en el curso. Si corresponde, pedí al docente/soporte que verifique tu rol.",
                confidence=0.80,
            )
        )

    # notification_issues
    @Rule(
        Symptom(type="chat", description="notification_issues"),
        SystemInfo(browser="IE"),
    )
    def notif_ie(self):
        self.declare(
            Diagnosis(
                problem_type="chat",
                cause="browser",
                solution="Internet Explorer no maneja bien notificaciones del sitio. Usá Chrome, Firefox, Edge o Safari.",
                confidence=0.94,
            )
        )

    @Rule(
        Symptom(type="chat", description="notification_issues"),
        SystemInfo(browser=MATCH.br),
        TEST(lambda br: br in ("Chrome", "Firefox", "Edge", "Safari", "Other")),
    )
    def notif_any(self, br):
        self.declare(
            Diagnosis(
                problem_type="chat",
                cause="browser",
                solution="Activá las notificaciones del sitio en el navegador y en el sistema (quitá 'No molestar') y recargá la página.",
                confidence=0.78,
            )
        )

    # emoji_not_working
    @Rule(
        Symptom(type="chat", description="emoji_not_working"), SystemInfo(browser="IE")
    )
    def emoji_ie(self):
        self.declare(
            Diagnosis(
                problem_type="chat",
                cause="browser",
                solution="El navegador no soporta correctamente emojis. Cambiá a Chrome, Firefox, Edge o Safari.",
                confidence=0.92,
            )
        )

    @Rule(
        Symptom(type="chat", description="emoji_not_working"),
        SystemInfo(browser="Other"),
    )
    def emoji_other(self):
        self.declare(
            Diagnosis(
                problem_type="chat",
                cause="browser",
                solution="Usá un navegador compatible y actualizado (Chrome, Firefox, Edge o Safari) para que los emojis funcionen bien.",
                confidence=0.86,
            )
        )

    @Rule(
        Symptom(type="chat", description="emoji_not_working"),
        SystemInfo(browser=MATCH.br),
        TEST(lambda br: br in ("Chrome", "Firefox", "Edge", "Safari")),
    )
    def emoji_modern(self, br):
        self.declare(
            Diagnosis(
                problem_type="chat",
                cause="browser",
                solution="Actualizá el navegador a la última versión y recargá el chat. Probá también en ventana privada.",
                confidence=0.80,
            )
        )

    # chat_lag
    @Rule(Symptom(type="chat", description="chat_lag"), SystemInfo(browser="IE"))
    def lag_ie(self):
        self.declare(
            Diagnosis(
                problem_type="chat",
                cause="browser",
                solution="Internet Explorer es lento para el chat. Cambiá a Chrome, Firefox, Edge o Safari.",
                confidence=0.92,
            )
        )

    @Rule(
        Symptom(type="chat", description="chat_lag"),
        SystemInfo(browser=MATCH.br),
        TEST(lambda br: br in ("Chrome", "Firefox", "Edge", "Safari", "Other")),
        SystemInfo(connection_type=MATCH.ct),
        TEST(lambda ct: ct in ("cellular", "slow_wifi")),
    )
    def lag_poor_net(self, br, ct):
        self.declare(
            Diagnosis(
                problem_type="chat",
                cause="network",
                solution="Cerrá descargas/streaming, acercate al router o pasate a Ethernet. Si estás con datos móviles, probá una WiFi estable.",
                confidence=0.80,
            )
        )

    @Rule(
        Symptom(type="chat", description="chat_lag"),
        SystemInfo(browser=MATCH.br),
        TEST(lambda br: br in ("Chrome", "Firefox", "Edge", "Safari", "Other")),
        SystemInfo(connection_type=MATCH.ct),
        TEST(lambda ct: ct in ("wifi", "ethernet")),
    )
    def lag_stable_net(self, br, ct):
        self.declare(
            Diagnosis(
                problem_type="chat",
                cause="browser",
                solution="Cerrá pestañas pesadas, recargá el chat y probá ventana privada. Si continúa, probá otro navegador compatible.",
                confidence=0.72,
            )
        )

    # fallback
    @Rule(Symptom(type="chat"), NOT(Diagnosis(problem_type="chat")))
    def fb_chat(self):
        self.declare(
            Diagnosis(
                problem_type="chat",
                cause="unknown",
                solution="Recargá la página y probá en un navegador compatible y otra red. Si persiste, informá al soporte.",
                confidence=0.40,
            )
        )
