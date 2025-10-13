from experta import Rule, MATCH, TEST, NOT
from ..facts import Symptom, SystemInfo, Diagnosis

class ContentRules:
    @Rule(Symptom(type="content", description="content_not_loading"))
    def content_not_loading(self):
        self.declare(Diagnosis(
            problem_type="content",
            cause="browser",
            solution="Borrá caché/cookies o usá modo incógnito; probá con otro navegador.",
            confidence=0.70
        ))

    @Rule(Symptom(type="content", description="missing_files"))
    def content_missing(self):
        self.declare(Diagnosis(
            problem_type="content",
            cause="link",
            solution="Faltan archivos. Avisá al docente/soporte qué recurso no aparece para que lo republiquen.",
            confidence=0.80
        ))

    @Rule(Symptom(type="content", description="broken_links"))
    def content_broken(self):
        self.declare(Diagnosis(
            problem_type="content",
            cause="link",
            solution="Hay enlaces rotos. Compartí la URL del curso y el nombre del recurso para su corrección.",
            confidence=0.80
        ))

    @Rule(
        Symptom(type="content", description="formatting_issues"),
        SystemInfo(browser=MATCH.br),
        TEST(lambda br: br in ("IE", "Other"))
    )
    def content_format_ie(self, br):
        self.declare(Diagnosis(
            problem_type="content",
            cause="browser",
            solution="Problemas de formato por compatibilidad. Probá Chrome/Firefox/Edge.",
            confidence=0.75
        ))

    @Rule(Symptom(type="content", description="access_denied_to_content"))
    def content_access_denied(self):
        self.declare(Diagnosis(
            problem_type="content",
            cause="permissions",
            solution="No tenés permisos para este recurso. Pedí acceso o verificación de inscripción.",
            confidence=0.90
        ))

    @Rule(Symptom(type="content"), NOT(Diagnosis(problem_type="content")))
    def fb_content(self):
        self.declare(Diagnosis(
            problem_type="content",
            cause="unknown",
            solution="Limpiá caché, probá modo incógnito y verificá el enlace o tus permisos.",
            confidence=0.40
        ))