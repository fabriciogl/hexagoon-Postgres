#  Copyright (c) 2021. Hexagoon. Criador: Fabricio Gatto Lourençone. Todos os direitos reservados.

# Imports the Google Cloud client library

def iniciar_gcp_logger():

    # Imports the Cloud Logging client library
    import google.cloud.logging

    # Instantiates a client
    client = google.cloud.logging.Client()

    # Retrieves a Cloud Logging handler based on the environment
    # you're running in and integrates the handler with the
    # Python logging module. By default this captures all logs
    # at INFO level and higher
    client.setup_logging()


