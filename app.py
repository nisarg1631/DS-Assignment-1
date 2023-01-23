from src import app
import config

if __name__ == "__main__":
    app.config.from_object(config.DevConfig)
    app.run()
