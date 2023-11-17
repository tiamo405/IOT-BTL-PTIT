import numpy as np
import cv2
import grpc
from tritonclient.grpc import service_pb2, service_pb2_grpc
import os
import sys
root = os.getcwd()
pwd = os.path.dirname(os.path.realpath("."))
sys.path.insert(0, root)
import config 


# from src import TRITON_HOST, TRITON_PORT

def _random_crop(img, width, height):
    if img.shape[1] - width <= 0 or img.shape[0] - height <= 0:
        return img
    x = np.random.randint(0, img.shape[1] - width)
    y = np.random.randint(0, img.shape[0] - height)
    img = img[y:y + height, x:x + width].copy()
    if np.random.uniform() < 0.5:
        img = cv2.flip(img, 1)
    return img


def _l2_norm(x, axis=1):
    """l2 norm"""
    norm = np.linalg.norm(x, axis=axis, keepdims=True)
    output = x / norm
    return output

def _augment(face_img, total=10):
    # face_img = cv2.resize(face_img, (128, 128))
    # a = int((128 - 112) / 2)  # x start
    # b = int((128 - 112) / 2 + 112)  # x end
    # c = int((128 - 112) / 2)  # y start
    # d = int((128 - 112) / 2 + 112)  # y end
    
    face_imgs = [face_img]
    for _ in range(total-1):
        face_imgs.append(_random_crop(face_img, 112, 112))

    return face_imgs

def _preprocess(face, net_inshape):
        face = cv2.resize(face, net_inshape[::-1])  # (h, w) to (w, h)
        
        face = (face.astype(np.float32) - 127.5) / 127.5 # ta đưa giá trị pixel về khoảng từ -1 đến 1. Chuẩn hóa giá trị pixel giúp mô hình học sâu học được hiệu quả hơn.

        face = np.transpose(face, (2, 0, 1)) # W, H, C -> C, W, H
        face = np.expand_dims(face, 0).astype(np.float32) # 1, C, W, H
        return face

class FaceEmbedding:
    def __init__(self, enet_inshape=(112, 112), TRITON_HOST = "0.0.0.0", TRITON_PORT = 8001):
        self.enet_inshape = enet_inshape

        self.embedding_model_name = "webface_R50_RT"
        self.e_input_name = ["input.1"]
        self.e_output_names = ["683", "output_1"]
        options = [('grpc.max_send_message_length', 512 * 1024 * 1024), ('grpc.max_receive_message_length', 512 * 1024 * 1024)]
        channel = grpc.insecure_channel(f"{TRITON_HOST}:{TRITON_PORT}", options=options)
        self.grpc_stub = service_pb2_grpc.GRPCInferenceServiceStub(channel)

    def get_embs(self, l_face_img):
        """
        Embedding a face_img with random crop from 1 to 10 item
        Args:
            img: A np.array BGR format
        Return:
            embs
        """
        if len(l_face_img) > 5:
            l_face_img = l_face_img[:5]
        face_imgs = []
        chunk = 5//len(l_face_img)
        _zp = len(l_face_img) - (5%len(l_face_img))
        for i, face_img in enumerate(l_face_img):            
            face_img = face_img[..., ::-1]  # BGR to RGB
            if i >= _zp:
                face_imgs.extend(_augment(face_img, total=chunk+1))
            else:
                face_imgs.extend(_augment(face_img, total=chunk))

        
        # init request
        e_request = service_pb2.ModelInferRequest()
        e_request.model_name = self.embedding_model_name
        # setup output
        for e_output_name in self.e_output_names:
            e_output = service_pb2.ModelInferRequest().InferRequestedOutputTensor()
            e_output.name = e_output_name
            e_request.outputs.extend([e_output])
        # setup input
        e_input = service_pb2.ModelInferRequest().InferInputTensor()
        e_input.name = self.e_input_name[0]
        e_input.datatype = "FP32"
        e_input.shape.extend([1, 3, self.enet_inshape[0], self.enet_inshape[0]])  # fix
        e_request.inputs.extend([e_input])
        
        input_bytes = None
        for face in face_imgs:
            face = _preprocess(face, self.enet_inshape)
            print(face.tobytes())
            if input_bytes == None:
                input_bytes = face.tobytes()
            else:
                input_bytes += face.tobytes()
        e_request.raw_input_contents.extend([input_bytes])
        # infer
        e_response = self.grpc_stub.ModelInfer(e_request)
        
        _emb_shape = e_response.outputs[0].shape
        embs = np.frombuffer(e_response.raw_output_contents[0], dtype=np.float32).reshape(_emb_shape)
        embs = _l2_norm(embs)
        # _score_shape = e_response.outputs[1].shape
        # scores = np.frombuffer(e_response.raw_output_contents[1], dtype=np.float32).reshape(_score_shape)
        scores = np.ones([_emb_shape[0],1])*100
        return embs, scores

    def get_emb(self, face_img):
        """
        Embedding a face_img with random crop from 1 to 10 item
        Args:
            img: A np.array BGR format, one image
        Return:
            embs
        """
        # init request
        e_request = service_pb2.ModelInferRequest()
        e_request.model_name = self.embedding_model_name
        # setup output
        for e_output_name in self.e_output_names:
            e_output = service_pb2.ModelInferRequest().InferRequestedOutputTensor()
            e_output.name = e_output_name
            e_request.outputs.extend([e_output])
        # setup input
        e_input = service_pb2.ModelInferRequest().InferInputTensor()
        e_input.name = self.e_input_name[0]
        e_input.datatype = "FP32"
        e_input.shape.extend([1, 3, self.enet_inshape[0], self.enet_inshape[0]])  # fixed
        e_request.inputs.extend([e_input])
        
        face = _preprocess(face_img, self.enet_inshape)
        input_bytes = face.tobytes()

        e_request.raw_input_contents.extend([input_bytes])
        # infer
        e_response = self.grpc_stub.ModelInfer(e_request)
        
        _emb_shape = e_response.outputs[0].shape
        embs = np.frombuffer(e_response.raw_output_contents[0], dtype=np.float32).reshape(_emb_shape)
        embs = _l2_norm(embs)
        _score_shape = e_response.outputs[1].shape
        scores = np.frombuffer(e_response.raw_output_contents[1], dtype=np.float32).reshape(_score_shape)
        # scores = np.ones([_emb_shape[0],1])*100
        return embs, scores

if __name__=="__main__":


    TRITON_HOST = config.TRITON_HOST
    # TRITON_HOST = "192.168.100.89"
    TRITON_PORT = config.TRITON_PORT

    print(TRITON_HOST, TRITON_PORT) 
    embs = []
    Yujii_A = FaceEmbedding(TRITON_HOST= TRITON_HOST, TRITON_PORT= TRITON_PORT)
    # for file in os.listdir('data-face'):
    #     path = os.path.join('data-face', file)
    #     image = cv2.imread(path)

    #     emb, score = Yujii_A.get_emb(image)
    #     embs.append(emb)

    image = cv2.imread('face_align.jpg')
    emb, score = Yujii_A.get_emb(image)
    print(score)
    print(emb.shape)