from fastapi_babel import Babel
from fastapi_babel import BabelConfigs

configs = BabelConfigs(
    ROOT_DIR=__file__,
    BABEL_DEFAULT_LOCALE="en",
    BABEL_TRANSLATION_DIRECTORY="locales",
)
babel = Babel(configs=configs)

if __name__ == "__main__":
    babel.run_cli()