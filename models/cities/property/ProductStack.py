import copy

import debug_toolkit
from models.cities.property.Product import Product
from models.cities.property.ProductInformation import ProductInformation


class ProductStack(object):
    def __init__(self, product_id: str, product: Product, product_info_dict: dict[ProductInformation: int]):
        self.product_id = product_id
        self.product = product
        self.product_info_dict = product_info_dict

    @staticmethod
    def from_dict(source):
        return ProductStack(product_id=source['product_id'],
                            product=Product.from_dict(source['product']),
                            product_info_dict=source['product_info_dict'])

    def to_dict(self):
        return {
            'product_id': self.product_id,
            'product': self.product.to_dict(),
            'product_info_dict': self.product_info_dict
        }

    def __repr__(self):
        return self.to_dict().__repr__()

    @staticmethod
    def generate_product_stacks(unlimited_product_stack):
        _debug_str = 'generate_product_stacks'
        debug_toolkit.function_start(_debug_str, args=[unlimited_product_stack])
        stacks = []
        space_left = 0
        stack = None
        for info, amount in unlimited_product_stack.product_info_dict.items():
            while amount > 0:
                if space_left == 0:
                    space_left = unlimited_product_stack.product.items_per_stack
                    if stack is not None:
                        stacks.append(stack)
                    stack = ProductStack(product_id=unlimited_product_stack.product_id,
                                         product=unlimited_product_stack.product, product_info_dict={})
                if amount <= space_left:
                    space_left -= amount
                    stack.product_info_dict[info] = amount
                    amount = 0
                else:
                    amount -= space_left
                    stack.product_info_dict[info] = space_left
                    space_left = 0
        if stack is not None and len(stack) > 0:
            stacks.append(stack)
        debug_toolkit.function_end(_debug_str, args=[stacks.__repr__()])
        return stacks

    @staticmethod
    def stack_over_flow(product_stack) -> bool:
        return product_stack.product.items_per_stack < len(product_stack)

    @staticmethod
    def is_full(product_stack) -> bool:
        return len(product_stack) >= product_stack.product.items_per_stack

    @staticmethod
    def remove_from_dict(original_dict: dict[ProductInformation: int],
                         item_to_be_removed: dict[ProductInformation: int]) -> dict[ProductInformation: int]:
        original_dict = copy.deepcopy(original_dict)
        for info_hash, amount in item_to_be_removed.items():
            if info_hash in original_dict:
                if original_dict[info_hash] <= amount:
                    if original_dict[info_hash] < amount:
                        debug_toolkit.warning_print('ProductStack:remove_from_dict', 'original dict items smaller.',
                                                    [original_dict, item_to_be_removed])
                    del original_dict[info_hash]
                else:
                    original_dict[info_hash] -= amount
        return original_dict

    def __len__(self):
        count = 0
        for _, amount in self.product_info_dict.items():
            count += amount
        return count

    def add_to_stack(self, product_stack):
        if self.product_id != product_stack.product_id:
            return product_stack
        added_product_info_dict = dict()
        addition_count = self.product.items_per_stack - len(self)
        for info_hash, amount in product_stack.product_info_dict.items():
            if addition_count > 0:
                amount_wanted = amount if amount <= addition_count else addition_count
                self.product_info_dict[info_hash] += amount_wanted
                if info_hash in added_product_info_dict:
                    added_product_info_dict[info_hash] += amount_wanted
                else:
                    added_product_info_dict[info_hash] = amount_wanted
                addition_count -= amount_wanted
            else:
                break
        return ProductStack(product_id=self.product_id, product=self.product,
                            product_info_dict=ProductStack.remove_from_dict(
                                original_dict=product_stack.product_info_dict,
                                item_to_be_removed=added_product_info_dict))

    def remove_from_stack(self, product_stack):
        if self.product_id != product_stack.product_id:
            return product_stack
        removed_product_info_dict = dict()
        for info_hash, amount in product_stack.product_info_dict.items():
            if info_hash in self.product_info_dict:
                owned_amount = self.product_info_dict[info_hash]
                if owned_amount <= amount:
                    del self.product_info_dict[info_hash]
                    if info_hash in removed_product_info_dict:
                        removed_product_info_dict[info_hash] += amount - owned_amount
                    else:
                        removed_product_info_dict[info_hash] = amount - owned_amount
                else:
                    self.product_info_dict[info_hash] -= amount
                    if info_hash in removed_product_info_dict:
                        removed_product_info_dict[info_hash] += amount
                    else:
                        removed_product_info_dict[info_hash] = amount
        return ProductStack(product_id=self.product_id, product=self.product,
                            product_info_dict=ProductStack.remove_from_dict(
                                original_dict=product_stack.product_info_dict,
                                item_to_be_removed=removed_product_info_dict))
