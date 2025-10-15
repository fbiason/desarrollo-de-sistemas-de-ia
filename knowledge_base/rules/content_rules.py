from experta import Rule, MATCH, TEST, NOT
from ..facts import Symptom, SystemInfo, Diagnosis


class ContentRules:
    @Rule(
        Symptom(type="content", description="content_not_loading"),
        SystemInfo(browser="IE"),
    )
    def cnl_ie(self):
        self.declare(
            Diagnosis(
                problem_type="content",
                cause="browser",
                solution="Internet Explorer no es compatible. Usá Chrome, Firefox, Edge o Safari e intentá nuevamente.",
                confidence=0.95,
            )
        )

    @Rule(
        Symptom(type="content", description="content_not_loading"),
        SystemInfo(browser="Other"),
    )
    def cnl_other(self):
        self.declare(
            Diagnosis(
                problem_type="content",
                cause="browser",
                solution="Tu navegador puede no ser compatible. Cambiá a Chrome, Firefox, Edge o Safari.",
                confidence=0.90,
            )
        )

    @Rule(
        Symptom(type="content", description="content_not_loading"),
        SystemInfo(browser=MATCH.br),
        TEST(lambda br: br in ("Chrome", "Firefox", "Edge", "Safari")),
        SystemInfo(connection_type=MATCH.ct),
        TEST(lambda ct: ct in ("cellular", "slow_wifi")),
    )
    def cnl_poor_net(self, br, ct):
        self.declare(
            Diagnosis(
                problem_type="content",
                cause="network",
                solution="Conexión inestable. Pasate a WiFi/ethernet estables o acercate al router y recargá el contenido.",
                confidence=0.85,
            )
        )

    @Rule(
        Symptom(type="content", description="content_not_loading"),
        SystemInfo(browser=MATCH.br),
        TEST(lambda br: br in ("Chrome", "Firefox", "Edge", "Safari")),
        SystemInfo(connection_type=MATCH.ct),
        TEST(lambda ct: ct in ("wifi", "ethernet")),
    )
    def cnl_stable_net(self, br, ct):
        self.declare(
            Diagnosis(
                problem_type="content",
                cause="browser",
                solution="Recargá, probá modo incógnito o limpiá caché/cookies. Si sigue, probá otro navegador compatible.",
                confidence=0.78,
            )
        )

    @Rule(Symptom(type="content", description="missing_files"))
    def content_missing(self):
        self.declare(
            Diagnosis(
                problem_type="content",
                cause="link",
                solution="Faltan archivos publicados. Informá al docente/soporte el nombre del recurso para que lo republiquen.",
                confidence=0.85,
            )
        )

    @Rule(Symptom(type="content", description="broken_links"))
    def content_broken(self):
        self.declare(
            Diagnosis(
                problem_type="content",
                cause="link",
                solution="Hay enlaces rotos. Compartí la URL del curso y el nombre del recurso para su corrección.",
                confidence=0.85,
            )
        )

    @Rule(
        Symptom(type="content", description="formatting_issues"),
        SystemInfo(browser="IE"),
    )
    def fmt_ie(self):
        self.declare(
            Diagnosis(
                problem_type="content",
                cause="browser",
                solution="Problemas de formato por incompatibilidad. Usá Chrome, Firefox, Edge o Safari.",
                confidence=0.92,
            )
        )

    @Rule(
        Symptom(type="content", description="formatting_issues"),
        SystemInfo(browser="Other"),
    )
    def fmt_other(self):
        self.declare(
            Diagnosis(
                problem_type="content",
                cause="browser",
                solution="Usá un navegador compatible y actualizado (Chrome, Firefox, Edge o Safari).",
                confidence=0.86,
            )
        )

    @Rule(
        Symptom(type="content", description="formatting_issues"),
        SystemInfo(browser=MATCH.br),
        TEST(lambda br: br in ("Chrome", "Firefox", "Edge", "Safari")),
    )
    def fmt_modern(self, br):
        self.declare(
            Diagnosis(
                problem_type="content",
                cause="browser",
                solution="Actualizá el navegador, recargá y probá modo incógnito. Si continúa, probá en otro navegador compatible.",
                confidence=0.78,
            )
        )

    @Rule(Symptom(type="content", description="access_denied_to_content"))
    def content_access_denied(self):
        self.declare(
            Diagnosis(
                problem_type="content",
                cause="permissions",
                solution="No tenés permisos para este recurso. Pedí verificación de inscripción o acceso al administrador/docente.",
                confidence=0.92,
            )
        )

    @Rule(Symptom(type="content"), NOT(Diagnosis(problem_type="content")))
    def fb_content(self):
        self.declare(
            Diagnosis(
                problem_type="content",
                cause="unknown",
                solution="Probá un navegador compatible, recargá en modo incógnito y verificá el enlace o tus permisos.",
                confidence=0.40,
            )
        )
