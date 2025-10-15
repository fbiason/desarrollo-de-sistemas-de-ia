from experta import Rule, MATCH, TEST, NOT
from ..facts import Symptom, SystemInfo, Diagnosis


class LoginRules:
    # --- cannot_login ---
    @Rule(Symptom(type="login", description="cannot_login"), SystemInfo(browser="IE"))
    def cannot_login_ie(self):
        self.declare(
            Diagnosis(
                problem_type="login",
                cause="browser",
                solution="Estás usando Internet Explorer. Cambiá a Chrome, Firefox, Edge o Safari e intentá de nuevo.",
                confidence=0.95,
            )
        )

    @Rule(
        Symptom(type="login", description="cannot_login"), SystemInfo(browser="Other")
    )
    def cannot_login_other(self):
        self.declare(
            Diagnosis(
                problem_type="login",
                cause="browser",
                solution="Tu navegador puede no ser compatible. Usá Chrome, Firefox, Edge o Safari e intentá de nuevo.",
                confidence=0.90,
            )
        )

    @Rule(
        Symptom(type="login", description="cannot_login"),
        SystemInfo(browser=MATCH.br),
        TEST(lambda br: br in ("Chrome", "Firefox", "Edge", "Safari")),
        SystemInfo(connection_type="slow_wifi"),
    )
    def cannot_login_slow_wifi(self, br):
        self.declare(
            Diagnosis(
                problem_type="login",
                cause="user",
                solution="No podés iniciar sesión. Verificá usuario y contraseña; si persiste, restablecé la clave. Tu WiFi es inestable: acercate al router o probá Ethernet/datos móviles.",
                confidence=0.85,
            )
        )

    @Rule(
        Symptom(type="login", description="cannot_login"),
        SystemInfo(browser=MATCH.br),
        TEST(lambda br: br in ("Chrome", "Firefox", "Edge", "Safari")),
        SystemInfo(connection_type="cellular"),
    )
    def cannot_login_cellular(self, br):
        self.declare(
            Diagnosis(
                problem_type="login",
                cause="user",
                solution="No podés iniciar sesión. Verificá usuario y contraseña; si persiste, restablecé la clave. Estás con datos móviles: probá una red WiFi o cable más estable.",
                confidence=0.85,
            )
        )

    @Rule(
        Symptom(type="login", description="cannot_login"),
        SystemInfo(browser=MATCH.br),
        TEST(lambda br: br in ("Chrome", "Firefox", "Edge", "Safari")),
        SystemInfo(connection_type=MATCH.ct),
        TEST(lambda ct: ct in ("wifi", "ethernet")),
    )
    def cannot_login_modern_stable(self, br, ct):
        self.declare(
            Diagnosis(
                problem_type="login",
                cause="user",
                solution="No podés iniciar sesión. Verificá tu usuario y contraseña; si persiste, restablecé la clave desde '¿Olvidaste tu contraseña?'.",
                confidence=0.86,
            )
        )

    # --- invalid_credentials ---
    @Rule(
        Symptom(type="login", description="invalid_credentials"),
        SystemInfo(browser="IE"),
    )
    def invalid_credentials_ie(self):
        self.declare(
            Diagnosis(
                problem_type="login",
                cause="browser",
                solution="Internet Explorer no es compatible. Cambiá a Chrome, Firefox, Edge o Safari y volvé a ingresar tus credenciales.",
                confidence=0.95,
            )
        )

    @Rule(
        Symptom(type="login", description="invalid_credentials"),
        SystemInfo(browser="Other"),
    )
    def invalid_credentials_other(self):
        self.declare(
            Diagnosis(
                problem_type="login",
                cause="browser",
                solution="Usá un navegador compatible (Chrome, Firefox, Edge o Safari) y reingresá usuario y contraseña.",
                confidence=0.90,
            )
        )

    @Rule(
        Symptom(type="login", description="invalid_credentials"),
        SystemInfo(browser=MATCH.br),
        TEST(lambda br: br in ("Chrome", "Firefox", "Edge", "Safari")),
    )
    def invalid_credentials_modern(self, br):
        self.declare(
            Diagnosis(
                problem_type="login",
                cause="user",
                solution="Credenciales inválidas. Verificá mayúsculas/minúsculas y que la contraseña sea la correcta; si la olvidaste, restablecela.",
                confidence=0.90,
            )
        )

    # --- forgot_password (siempre igual, sin depender de navegador o conexión) ---
    @Rule(Symptom(type="login", description="forgot_password"))
    def forgot_password(self):
        self.declare(
            Diagnosis(
                problem_type="login",
                cause="user",
                solution="Restablecé tu contraseña desde '¿Olvidaste tu contraseña?'. Revisá bandeja de entrada y spam; si no llega el correo, solicitá uno nuevo.",
                confidence=0.88,
            )
        )

    # --- account_locked (independiente de navegador/conexión) ---
    @Rule(Symptom(type="login", description="account_locked"))
    def account_locked(self):
        self.declare(
            Diagnosis(
                problem_type="login",
                cause="user",
                solution="Tu cuenta está bloqueada por intentos fallidos. Esperá unos minutos o solicitá el desbloqueo al administrador.",
                confidence=0.93,
            )
        )

    # --- registration_failed ---
    @Rule(
        Symptom(type="login", description="registration_failed"),
        SystemInfo(browser="IE"),
    )
    def registration_failed_ie(self):
        self.declare(
            Diagnosis(
                problem_type="login",
                cause="browser",
                solution="Internet Explorer no es compatible. Cambiá a Chrome, Firefox, Edge o Safari y repetí el registro.",
                confidence=0.94,
            )
        )

    @Rule(
        Symptom(type="login", description="registration_failed"),
        SystemInfo(browser="Other"),
    )
    def registration_failed_other(self):
        self.declare(
            Diagnosis(
                problem_type="login",
                cause="browser",
                solution="Usá un navegador compatible (Chrome, Firefox, Edge o Safari) y reintentá el registro.",
                confidence=0.88,
            )
        )

    @Rule(
        Symptom(type="login", description="registration_failed"),
        SystemInfo(browser=MATCH.br),
        TEST(lambda br: br in ("Chrome", "Firefox", "Edge", "Safari")),
    )
    def registration_failed_modern(self, br):
        self.declare(
            Diagnosis(
                problem_type="login",
                cause="user",
                solution="No se pudo completar el registro. Completá todos los campos y verificá que el correo no esté ya registrado; luego reintentá.",
                confidence=0.80,
            )
        )

    # --- fallback ---
    @Rule(Symptom(type="login"), NOT(Diagnosis(problem_type="login")))
    def fallback(self):
        self.declare(
            Diagnosis(
                problem_type="login",
                cause="unknown",
                solution="Probá con un navegador compatible y reintentá. Si persiste, restablecé la contraseña.",
                confidence=0.40,
            )
        )
