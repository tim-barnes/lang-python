from concurrent import futures
import grpc
import time

import test_pb2

_ONE_DAY_IN_SECONDS = 60 * 60 * 24


def make_response(txt, score):
    return test_pb2.Response(text=txt, score=score)


class Servicer(test_pb2.ConversationServicer):

    def utterance(self, request, context):

        conversation_id = request.conversation_id
        seq_num = request.sequence_num

        print "{}  {}".format(conversation_id, seq_num)

        for i in range(1, 10):
            time.sleep(1)
            yield make_response("This is reponse {}".format(i), i * 0.1)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    test_pb2.add_ConversationServicer_to_server(Servicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == '__main__':
    serve()
