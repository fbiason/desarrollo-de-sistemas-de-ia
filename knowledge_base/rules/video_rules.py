from experta import Rule, MATCH, TEST, NOT
from ..facts import Symptom, SystemInfo, Diagnosis

class VideoRules:
    @Rule(
            Symptom(type="video", description=MATCH.desc),
            TEST(lambda desc: desc in ("video_not_loading", "video_buffering", "video_quality_poor")),
            SystemInfo(connection_type=MATCH.conn),
            TEST(lambda conn: conn in ("cellular", "slow_wifi"))
        )
    def video_network(self, conn, desc):
        self.declare(Diagnosis(
            problem_type="video",
            cause="network",
            solution="Conexión limitada. Cambiá a Ethernet/WiFi estable y/o bajá la calidad del video.",
            confidence=0.85
        ))

    @Rule(
        Symptom(type="video", description="video_not_loading"),
        SystemInfo(connection_type=MATCH.conn),
        TEST(lambda conn: conn in ("wifi", "ethernet"))
    )
    def video_local_issue(self, conn):
        self.declare(Diagnosis(
            problem_type="video",
            cause="browser",
            solution="Limpiá caché/cookies y desactivá extensiones (ad-block/privacidad); recargá la página.",
            confidence=0.70
        ))

    @Rule(
        Symptom(type="video", description="playback_controls_not_working"),
        SystemInfo(browser=MATCH.br)
    )
    def video_controls(self, br):
        self.declare(Diagnosis(
            problem_type="video",
            cause="browser",
            solution="Recargá sin caché, desactivá extensiones y probá otro navegador si continúa.",
            confidence=0.70
        ))

    @Rule(Symptom(type="video", description="audio_issues"))
    def video_audio(self):
        self.declare(Diagnosis(
            problem_type="video",
            cause="device",
            solution="Verificá volumen del reproductor y del sistema, y el dispositivo de salida correcto; asegurate de no tener el sitio silenciado.",
            confidence=0.75
        ))
    
    @Rule(Symptom(type="video"), NOT(Diagnosis(problem_type="video")))
    def fb_video(self):
        self.declare(Diagnosis(
            problem_type="video",
            cause="device",
            solution="Bajá calidad, desactivá extensiones y probá otra red/navegador.",
            confidence=0.40
        ))