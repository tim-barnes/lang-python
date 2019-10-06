import grpc

import test_pb2


def make_response_request(conversation_id, seq_num):
    return test_pb2.ResponseRequest(conversation_id=conversation_id,
                                    sequence_num=seq_num)


def get_responses(stub):
    request = make_response_request("ABJKDSAJLUUWDBJKB", 10)
    responses = stub.utterance(request)

    for i in responses:
        print "{}:  {}".format(i.score, i.text)


def run():
    channel = grpc.insecure_channel('localhost:50051')
    stub = test_pb2.ConversationStub(channel)

    get_responses(stub)


if __name__ == "__main__":
    run()
