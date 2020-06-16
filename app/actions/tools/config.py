# -*- coding:UTF-8 -*-
import logging
# env="_1sit"
# env="_6pre"
env="_7prd"
# loggerlevel = "INFO"
# loggerlevel=logging.DEBUG
loggerlevel=logging.DEBUG
loggerWrite=True
class config():
    def publicConfig(self):
        if (env=="_1sit"):
            from app.actions.tools._1sit import envConfig
            envC = envConfig
            return envC
        elif (env == "_6pre"):
            from app.actions.tools._6pre import envConfig
            envC = envConfig
            return envC
        elif (env == "_7prd"):
            from app.actions.tools._7prd import envConfig
            envC = envConfig
            return envC