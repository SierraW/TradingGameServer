import copy

import debug_toolkit
from models.cities.property.Product import Product
from models.cities.property.ProductStack import ProductStack


class Storage(object):
    def __init__(self, owner_fe_id: str, location: str, city_id: str, size: int = None,
                 product_stacks: list[ProductStack] = None):
        if product_stacks is None:
            product_stacks = []
        self.product_stacks = product_stacks
        self.size = size
        self.location = location
        self.city_id = city_id
        self.owner_fe_id = owner_fe_id

    def __len__(self):
        count = 0
        for product_stack in self.product_stacks:
            count += len(product_stack)
        return count

    @staticmethod
    def from_dict(source):
        return Storage(owner_fe_id=source['owner_fe_id'], size=source['size'],
                       product_stacks=list(
                           map(lambda product_stack_source: ProductStack.from_dict(product_stack_source),
                               ProductStack.from_dict(source['product_stacks']))),
                       location=source['storage_id'], city_id=source['city_id'])

    def to_dict(self):
        return {
            'product_stacks': list(map(lambda product_stack: product_stack.to_dict(), self.product_stacks)),
            'size': self.size,
            'location': self.location,
            'city_id': self.city_id,
            'owner_fe_id': self.owner_fe_id
        }

    @staticmethod
    def extract_product_id_dict_from_product_stacks(product_stacks: list[ProductStack]) -> \
            dict[str, list[ProductStack]]:
        _debug_str = 'extract_product_id_dict_from_product_stacks'
        debug_toolkit.function_start(_debug_str)
        restructured_product_stacks = []
        for product_stack in product_stacks:
            if ProductStack.stack_over_flow(product_stack=product_stack):
                restructured_product_stacks.extend(ProductStack.generate_product_stacks(
                    unlimited_product_stack=product_stack))
            else:
                restructured_product_stacks.append(product_stack)
        product_id_info_dict = dict()
        for product_stack in restructured_product_stacks:
            if product_stack.product_id in product_id_info_dict:
                product_id_info_dict[product_stack.product_id].append(product_stack)
            else:
                product_id_info_dict[product_stack.product_id] = [product_stack]
        debug_toolkit.function_end(_debug_str, args=[product_id_info_dict.__repr__()])
        return product_id_info_dict

    @staticmethod
    def export_product_stacks_from_product_id_info_dict(product_id_info_dict: dict[str, list[ProductStack]]) -> \
            list[ProductStack]:
        _debug_str = 'export_product_stacks_from_product_id_info_dict'
        debug_toolkit.function_start(_debug_str)
        export_product_stacks = []
        for _, product_stacks in product_id_info_dict.items():
            for product_stack in product_stacks:
                if ProductStack.stack_over_flow(product_stack=product_stack):
                    export_product_stacks.extend(
                        ProductStack.generate_product_stacks(unlimited_product_stack=product_stack))
                else:
                    export_product_stacks.append(product_stack)
        debug_toolkit.function_end(_debug_str, args=[export_product_stacks.__repr__()])
        return export_product_stacks

    @staticmethod
    def sorted(product_stacks: list[ProductStack]) -> list[ProductStack]:
        product_id_info_dict = dict()
        for product_stack in product_stacks:
            if product_stack.product_id not in product_id_info_dict:
                product_id_info_dict[product_stack.product_id] = product_stack
            else:
                product_info_dict = product_id_info_dict[product_stack.product_id].product_info_dict
                for product_info, amount in product_stack.product_info_dict.items():
                    if product_info in product_info_dict:
                        product_info_dict[product_info] += amount
                    else:
                        product_info_dict[product_info] = amount
        output_product_stack = []
        for product_id, unlimited_product_stack in product_id_info_dict.items():
            output_product_stack.extend(ProductStack.generate_product_stacks(
                unlimited_product_stack=unlimited_product_stack))
        return output_product_stack

    @staticmethod
    def add_to_storage_forced(destination_storage, product_stacks: list[ProductStack]) -> list[ProductStack]:
        _debug_str = 'add_to_storage_forced'
        debug_toolkit.function_start(_debug_str)
        incoming_product_id_info_dict = \
            Storage.extract_product_id_dict_from_product_stacks(
                product_stacks=Storage.sorted(product_stacks=product_stacks))
        for product_stack in destination_storage.product_stacks:
            if not ProductStack.is_full(product_stack):
                if product_stack.product_id in incoming_product_id_info_dict:
                    incoming_product_stacks = incoming_product_id_info_dict[product_stack.product_id]
                    for index in range(len(incoming_product_stacks)):
                        incoming_product_stack = incoming_product_stacks[index]
                        left = product_stack.add_to_stack(product_stack=incoming_product_stack)
                        incoming_product_stacks[index] = left
        incoming_product_stacks = []
        for _, product_stacks in incoming_product_id_info_dict.items():
            incoming_product_stacks.extend(product_stacks)
        incoming_product_stacks = Storage.sorted(product_stacks=incoming_product_stacks)
        available_space = (destination_storage.size - len(destination_storage.product_stacks)) \
            if destination_storage.size is not None else len(destination_storage.product_stacks)
        destination_storage.product_stacks.extend(incoming_product_stacks[:available_space])
        debug_toolkit.function_end(_debug_str)
        return incoming_product_stacks[available_space:]

    @staticmethod
    def remove_from_storage_detailed_forced(destination_storage, product_stacks: list[ProductStack]) \
            -> bool:
        _debug_str = 'remove_from_storage_detailed_forced'
        debug_toolkit.function_start(_debug_str)
        outgoing_product_id_info_dict = Storage.extract_product_id_dict_from_product_stacks(
            product_stacks=product_stacks)
        destination_product_id_info_dict = Storage.extract_product_id_dict_from_product_stacks(
            product_stacks=destination_storage.product_stacks)
        for product_id, product_stacks in outgoing_product_id_info_dict.items():
            if product_id in destination_product_id_info_dict:
                for index in range(len(product_stacks)):
                    product_stack = product_stacks[index]
                    for destination_product_stack in destination_product_id_info_dict[product_id]:
                        result = destination_product_stack.remove_from_stack(product_stack=product_stack)
                        product_stacks[index] = result
                        product_stack = result
                        if len(result) == 0:
                            break
            else:

                return False
        count = 0
        for product_id, product_stacks in outgoing_product_id_info_dict.items():
            for product_stack in product_stacks:
                count += len(product_stack)
        debug_toolkit.function_end(_debug_str)
        return count == 0

    def __repr__(self):
        return self.to_dict().__repr__()

    def _get_product_stacks_includes_product(self, product_id: str) -> list[ProductStack]:
        return list(filter(lambda product_stack_temp: product_stack_temp.product_id == product_id, self.product_stacks))

    def calculate_empty_space(self, product_id: str, product: Product) -> int:
        filtered_product_stacks = self._get_product_stacks_includes_product(product_id=product_id)
        product_stack_maximum = product.items_per_stack
        empty_space_count = (self.size - len(self.product_stacks)) * product_stack_maximum
        for product_stack in filtered_product_stacks:
            empty_space_count += product_stack_maximum - len(product_stack)
        return empty_space_count

    def add_to_storage(self, product_stacks: list[ProductStack]) -> bool:
        temp_storage = copy.deepcopy(self)
        if len(self.add_to_storage_forced(destination_storage=temp_storage, product_stacks=product_stacks)) > 0:
            return False
        else:
            self.add_to_storage_forced(destination_storage=self, product_stacks=product_stacks)
            return True

    def count_products(self, product_information_filter=None) -> int:
        count = 0
        for product_stack in self.product_stacks:
            if product_information_filter is None:
                count += len(product_stack)
            else:
                for product_information in product_stack.product_info_dict:
                    if product_information_filter(product_information):
                        count += 1
        return count

    def remove_from_storage(self, product_stacks: list[ProductStack]) -> bool:
        temp_storage = copy.deepcopy(self)
        if self.remove_from_storage_detailed_forced(destination_storage=temp_storage, product_stacks=product_stacks):
            self.remove_from_storage_detailed_forced(destination_storage=self, product_stacks=product_stacks)
            return True
        else:
            return False
