import logging

def setup_logging():
    logging.basicConfig(
        filename="client_run.log",
        filemode="w",
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s"
    )
    return logging.getLogger(__name__)
