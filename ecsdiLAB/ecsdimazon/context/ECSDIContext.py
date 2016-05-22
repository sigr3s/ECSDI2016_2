from ecsdiLAB.ecsdimazon.data.ProductService import ProductService


class ECSDIContext:
    def __init__(self):
        self.product_service = ProductService()
