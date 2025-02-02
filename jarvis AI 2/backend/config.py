import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    # OpenAI Configuration
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    
    # Speech Recognition Settings
    SPEECH_RECOGNITION_THRESHOLD = 0.5
    LANGUAGE_MODEL = 'gpt-3.5-turbo'
    
    # Task Automation Settings
    TASK_RETRY_LIMIT = 3
    DEFAULT_TIMEOUT = 30  # seconds
    
    # System Paths
    LOGS_DIRECTORY = os.path.join(os.getcwd(), 'logs')
    TEMP_DIRECTORY = os.path.join(os.getcwd(), 'temp')
    
    # Logging Configuration
    LOGGING_CONFIG = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'standard': {
                'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            },
        },
        'handlers': {
            'default': {
                'level': 'INFO',
                'formatter': 'standard',
                'class': 'logging.StreamHandler',
            },
            'file_handler': {
                'level': 'DEBUG',
                'formatter': 'standard',
                'class': 'logging.FileHandler',
                'filename': os.path.join(LOGS_DIRECTORY, 'ai_assistant.log'),
                'mode': 'a',
            }
        },
        'loggers': {
            '': {  # root logger
                'handlers': ['default', 'file_handler'],
                'level': 'INFO',
                'propagate': True
            }
        }
    }

    @classmethod
    def validate_config(cls):
        """
        Validate configuration settings
        """
        if not cls.OPENAI_API_KEY:
            raise ValueError("OpenAI API Key is not set")
        
        # Create necessary directories
        os.makedirs(cls.LOGS_DIRECTORY, exist_ok=True)
        os.makedirs(cls.TEMP_DIRECTORY, exist_ok=True)

# Initialize configuration
Config.validate_config()
