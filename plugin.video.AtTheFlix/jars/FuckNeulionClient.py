import socket

import FuckNeulionService

__CLIENT_NAME__ = 'FuckNeulionClient'

__client_socket__ = None


def __connect_to_server():
    """
    Connects to the server
    """
    log('Client connecting to server')

    global __client_socket__
    __client_socket__ = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    log('Client socket created')

    __client_socket__.connect((FuckNeulionService.HOST, FuckNeulionService.PORT))
    log('Client socket connected')


def __close_connection():
    """
    Closes the connection to the server
    """
    global __client_socket__
    if __client_socket__ is not None:
        __client_socket__.close()
        log('Client socket closed')


def request_proxy_hack(game_id, team_type):
    """
    Requests the server to run proxy hack for the given stream
    :param game_id:
    :param team_type:
    :return:
    """
    global __client_socket__

    # Connect to the server
    __connect_to_server()

    if __client_socket__ is None:
        raise Exception('Client socket is not connected')

    # Send the run proxy hack command
    command_string = FuckNeulionService.RunProxyHackCommand(game_id, team_type).to_string()
    __client_socket__.send(command_string)

    # Receive the response
    response_string = __client_socket__.recv(FuckNeulionService.MSG_SIZE)
    response = FuckNeulionService.Response.accept(response_string)
    log('Proxy hack response ' + str(response))

    # Close the connection
    __close_connection()

    return response.success, response.msg


def request_server_shutdown():
    global __client_socket__

    # Connect to the server
    __connect_to_server()

    if __client_socket__ is None:
        raise Exception('Client socket is not connected')

    # Send the shutdown command
    command_string = FuckNeulionService.ShutdownServerCommand().to_string()
    __client_socket__.send(command_string)

    # Close the connection
    __close_connection()


def log(msg):
    print __CLIENT_NAME__ + ': ' + msg


if __name__ == "__main__":
    request_proxy_hack('100111', 'away')
    request_server_shutdown()