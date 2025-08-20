import os
import logging
from datetime import datetime
import structlog

print(os.getcwd())
class CustomLogger:
    def __init__(self, log_dir="logs", max_logs=5):
        # Ensure logs directory exists
        self.logs_dir = os.path.join(os.getcwd(), log_dir)
        os.makedirs(self.logs_dir, exist_ok=True)

        # Timestamped log file (for persistence)
        log_file = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"
        self.log_file_path = os.path.join(self.logs_dir, log_file)
        
        self.max_logs = max_logs


        self._cleanup_old_logs()

    def _cleanup_old_logs(self):
        """
        Keeps only the latest `max_logs` files in the log directory.
        """
        log_files = sorted(
            [f for f in os.listdir(self.logs_dir) if f.endswith(".log")],
            key=lambda f: os.path.getmtime(os.path.join(self.logs_dir, f))
        )

        while len(log_files) > self.max_logs:
            oldest = log_files.pop(0)   # remove oldest
            os.remove(os.path.join(self.logs_dir, oldest))
            print(f"Deleted old log file: {oldest}")


    def get_logger(self, name=__file__):
        logger_name = os.path.basename(name)

        # Configure logging for console + file (both JSON)
        file_handler = logging.FileHandler(self.log_file_path)
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(logging.Formatter("%(message)s"))  # Raw JSON lines

        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(logging.Formatter("%(message)s"))

        logging.basicConfig(
            level=logging.INFO,
            format="%(message)s",  # Structlog will handle JSON rendering
            handlers=[console_handler, file_handler]
        )

        # Configure structlog for JSON structured logging
        structlog.configure(
            processors=[
                structlog.processors.TimeStamper(fmt="iso", utc=True, key="timestamp"),
                structlog.processors.add_log_level,
                structlog.processors.EventRenamer(to="event"),
                structlog.processors.JSONRenderer()
            ],
            logger_factory=structlog.stdlib.LoggerFactory(),
            cache_logger_on_first_use=True,
        )

        return structlog.get_logger(logger_name)


# --- Usage Example ---
if __name__ == "__main__":
    logger = CustomLogger().get_logger(__file__)
    logger.info("User uploaded a file", user_id=123, filename="report.pdf")
    logger.error("Failed to process PDF", error="File not found", user_id=123)