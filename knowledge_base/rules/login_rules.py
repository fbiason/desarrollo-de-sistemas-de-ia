from experta import Rule, MATCH, TEST, NOT
from ..facts import Symptom, SystemInfo, Diagnosis

class LoginRules:
    @Rule(
        Symptom(type="login", description=MATCH.desc),
        TEST(lambda desc: desc in ("cannot_login", "invalid_credentials")),
        SystemInfo(browser=MATCH.br, connection_type=MATCH.conn)
    )
    def login_creds_generic(self, br, conn):
        self.declare(Diagnosis(
            problem_type="login",
            cause="user",
            solution="Verificá usuario/contraseña; si persiste, restablecé la clave.",
            confidence=0.80
        ))

    @Rule(
        Symptom(type="login", description="cannot_login"),
        SystemInfo(browser=MATCH.br),
        TEST(lambda br: br in ("IE", "Other"))
    )
    def login_incompatible_browser(self, br):
        self.declare(Diagnosis(
            problem_type="login",
            cause="browser",
            solution="Navegador no compatible. Probá Chrome, Firefox o Edge.",
            confidence=0.80
        ))

    @Rule(Symptom(type="login", description="forgot_password"))
    def login_forgot_password(self):
        self.declare(Diagnosis(
            problem_type="login",
            cause="user",
            solution="Usá '¿Olvidaste tu contraseña?' y revisá spam; pedí reenvío si no llega.",
            confidence=0.85
        ))

    @Rule(Symptom(type="login", description="account_locked"))
    def login_locked(self):
        self.declare(Diagnosis(
            problem_type="login",
            cause="user",
            solution="Cuenta bloqueada por intentos fallidos. Pedí desbloqueo al administrador.",
            confidence=0.90
        ))

    @Rule(Symptom(type="login", description="registration_failed"))
    def login_registration_failed(self):
        self.declare(Diagnosis(
            problem_type="login",
            cause="user",
            solution="Completá todos los campos requeridos y reintentá; si persiste, informá el mensaje de error.",
            confidence=0.70
        ))

    @Rule(Symptom(type="login"), NOT(Diagnosis(problem_type="login")))
    def fb_login(self):
        self.declare(Diagnosis(
            problem_type="login",
            cause="unknown",
            solution="Limpiá caché/cookies, usá ventana privada y probá otro navegador. Si persiste, restablecé la contraseña.",
            confidence=0.40
        ))