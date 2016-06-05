from ecsdiLAB.ecsdimazon.data.ProductService import ProductService
from ecsdiLAB.ecsdimazon.data.UserService import UserService


class ECSDIContext:
    def __init__(self):
        self.product_service = ProductService()
        self.user_service = UserService()
