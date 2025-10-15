from experta import Rule, MATCH, TEST, NOT
from ..facts import Symptom, SystemInfo, Diagnosis


class VideoRules:
    @Rule(
        Symptom(type="video", description="video_not_loading"), SystemInfo(browser="IE")
    )
    def vnl_ie(self):
        self.declare(
            Diagnosis(
                problem_type="video",
                cause="browser",
                solution="Internet Explorer no es compatible con el reproductor. Usá Chrome, Firefox, Edge o Safari.",
                confidence=0.95,
            )
        )

    @Rule(
        Symptom(type="video", description="video_not_loading"),
        SystemInfo(browser="Other"),
    )
    def vnl_other(self):
        self.declare(
            Diagnosis(
                problem_type="video",
                cause="browser",
                solution="Tu navegador puede no ser compatible. Usá Chrome, Firefox, Edge o Safari para reproducir el video.",
                confidence=0.90,
            )
        )

    @Rule(
        Symptom(type="video", description="video_not_loading"),
        SystemInfo(browser=MATCH.br),
        TEST(lambda br: br in ("Chrome", "Firefox", "Edge", "Safari")),
        SystemInfo(connection_type=MATCH.conn),
        TEST(lambda conn: conn in ("cellular", "slow_wifi")),
    )
    def vnl_poor_net(self, br, conn):
        self.declare(
            Diagnosis(
                problem_type="video",
                cause="network",
                solution="La conexión es inestable. Pasate a WiFi o Ethernet estable, o esperá unos minutos antes de recargar.",
                confidence=0.85,
            )
        )

    @Rule(
        Symptom(type="video", description="video_not_loading"),
        SystemInfo(browser=MATCH.br),
        TEST(lambda br: br in ("Chrome", "Firefox", "Edge", "Safari")),
        SystemInfo(connection_type=MATCH.conn),
        TEST(lambda conn: conn in ("wifi", "ethernet")),
    )
    def vnl_stable_net(self, br, conn):
        self.declare(
            Diagnosis(
                problem_type="video",
                cause="browser",
                solution="Limpiá caché y cookies, desactivá extensiones (adblock o privacidad) y recargá la página.",
                confidence=0.78,
            )
        )

    @Rule(
        Symptom(type="video", description="video_buffering"),
        SystemInfo(connection_type=MATCH.conn),
        TEST(lambda conn: conn in ("cellular", "slow_wifi")),
    )
    def buffering_poor_net(self, conn):
        self.declare(
            Diagnosis(
                problem_type="video",
                cause="network",
                solution="Tu red está saturada o lenta. Cerrá otras aplicaciones o bajá la calidad del video.",
                confidence=0.85,
            )
        )

    @Rule(
        Symptom(type="video", description="video_buffering"),
        SystemInfo(connection_type=MATCH.conn),
        TEST(lambda conn: conn in ("wifi", "ethernet")),
    )
    def buffering_stable_net(self, conn):
        self.declare(
            Diagnosis(
                problem_type="video",
                cause="browser",
                solution="Cerrá otras pestañas, desactivá extensiones y recargá. Si sigue, probá en otro navegador compatible.",
                confidence=0.75,
            )
        )

    @Rule(
        Symptom(type="video", description="video_quality_poor"),
        SystemInfo(connection_type=MATCH.conn),
        TEST(lambda conn: conn in ("cellular", "slow_wifi")),
    )
    def quality_poor_net(self, conn):
        self.declare(
            Diagnosis(
                problem_type="video",
                cause="network",
                solution="La calidad baja por conexión limitada. Cambiá a una red estable o reducí la resolución del video.",
                confidence=0.85,
            )
        )

    @Rule(
        Symptom(type="video", description="video_quality_poor"),
        SystemInfo(connection_type=MATCH.conn),
        TEST(lambda conn: conn in ("wifi", "ethernet")),
    )
    def quality_stable_net(self, conn):
        self.declare(
            Diagnosis(
                problem_type="video",
                cause="browser",
                solution="Actualizá el navegador y cerrá otras pestañas que consuman recursos. Si persiste, probá otro navegador.",
                confidence=0.75,
            )
        )

    @Rule(Symptom(type="video", description="audio_issues"), SystemInfo(browser="IE"))
    def audio_ie(self):
        self.declare(
            Diagnosis(
                problem_type="video",
                cause="browser",
                solution="Internet Explorer no maneja correctamente el audio. Usá Chrome, Firefox, Edge o Safari.",
                confidence=0.92,
            )
        )

    @Rule(
        Symptom(type="video", description="audio_issues"),
        SystemInfo(browser=MATCH.br),
        TEST(lambda br: br in ("Chrome", "Firefox", "Edge", "Safari", "Other")),
    )
    def audio_device(self, br):
        self.declare(
            Diagnosis(
                problem_type="video",
                cause="device",
                solution="Verificá el volumen del reproductor y del sistema, el dispositivo de salida correcto y que el sitio no esté silenciado.",
                confidence=0.78,
            )
        )

    @Rule(
        Symptom(type="video", description="playback_controls_not_working"),
        SystemInfo(browser="IE"),
    )
    def controls_ie(self):
        self.declare(
            Diagnosis(
                problem_type="video",
                cause="browser",
                solution="Internet Explorer no soporta los controles del reproductor. Cambiá a Chrome, Firefox, Edge o Safari.",
                confidence=0.94,
            )
        )

    @Rule(
        Symptom(type="video", description="playback_controls_not_working"),
        SystemInfo(browser="Other"),
    )
    def controls_other(self):
        self.declare(
            Diagnosis(
                problem_type="video",
                cause="browser",
                solution="Usá un navegador compatible (Chrome, Firefox, Edge o Safari) y recargá el video.",
                confidence=0.88,
            )
        )

    @Rule(
        Symptom(type="video", description="playback_controls_not_working"),
        SystemInfo(browser=MATCH.br),
        TEST(lambda br: br in ("Chrome", "Firefox", "Edge", "Safari")),
    )
    def controls_modern(self, br):
        self.declare(
            Diagnosis(
                problem_type="video",
                cause="browser",
                solution="Recargá la página sin caché (Ctrl+F5), desactivá extensiones y probá ventana privada o navegador alternativo.",
                confidence=0.78,
            )
        )

    @Rule(Symptom(type="video"), NOT(Diagnosis(problem_type="video")))
    def fb_video(self):
        self.declare(
            Diagnosis(
                problem_type="video",
                cause="unknown",
                solution="Recargá el video, bajá la calidad y probá con otro navegador o red estable. Si persiste, informá al soporte.",
                confidence=0.40,
            )
        )
