class ProductInformation(object):
    def __init__(self, charming: int, production_t_plus: int, expiry_t_plus: int = None):
        self.charming = charming
        self.production_t_plus = production_t_plus
        self.expiry_t_plus = expiry_t_plus

    @staticmethod
    def from_dict(source):
        product_information = ProductInformation(charming=source['charming'],
                                                 production_t_plus=source['production_t_plus'])
        if 'expiry_t_plus' in product_information:
            product_information.expiry_t_plus = source['expiry_t_plus']
        return product_information

    def to_dict(self):
        return {
            'charming': self.charming,
            'production_t_plus': self.production_t_plus,
            'expiry_t_plus': self.expiry_t_plus
        }

    def __repr__(self):
        return self.to_dict().__repr__()

    def __eq__(self, other):
        return self.charming == other.charming and self.production_t_plus == other.production_t_plus and \
               (True if self.expiry_t_plus is None and
                other.expiry_t_plus is None else self.expiry_t_plus == other.expiry_t_plus)

    def __hash__(self):
        return f'c{self.charming}p{self.production_t_plus}e{self.expiry_t_plus}'.__hash__()
