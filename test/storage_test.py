from models.Storage import Storage
from models.Storage import ProductStack
from models.cities.property.Product import Product
from models.cities.property.ProductInformation import ProductInformation

storage_a = Storage(owner_fe_id='storage_a', location='location_a', city_id='city', size=5)
storage_b = Storage(owner_fe_id='storage_b', location='location_b', city_id='city')

apple_id = 'apple is inner ghost'
apple = Product(name='apple', category=0, items_per_stack=60)

product_stack_1 = ProductStack(product_id=apple_id, product=apple, product_info_dict={
    ProductInformation(charming=100, production_t_plus=0): 1
})

product_stack_100 = ProductStack(product_id=apple_id, product=apple, product_info_dict={
    ProductInformation(charming=100, production_t_plus=0): 100
})

product_stack_1000 = ProductStack(product_id=apple_id, product=apple, product_info_dict={
    ProductInformation(charming=100, production_t_plus=0): 1000
})

print(storage_a)
print(product_stack_100)
print(storage_a.add_to_storage(product_stacks=[product_stack_100]))
print(storage_a)
print(len(storage_a))
print(storage_a.add_to_storage(product_stacks=[product_stack_100]))
print(storage_a)
print(len(storage_a))
print(storage_a.add_to_storage(product_stacks=[product_stack_1]))
print(storage_a)
print(len(storage_a))
print(storage_a.add_to_storage(product_stacks=[product_stack_1]))
print(storage_a)
print(len(storage_a))
print(storage_a.add_to_storage(product_stacks=[product_stack_1]))
print(storage_a)
print(len(storage_a))
print(storage_a.add_to_storage(product_stacks=[product_stack_1]))
print(storage_a)
print(len(storage_a))
print(storage_a.add_to_storage(product_stacks=[product_stack_1]))
print(storage_a)
print(len(storage_a))
print(storage_a.remove_from_storage(product_stacks=[product_stack_1]))
print(storage_a)
print(len(storage_a))
print(storage_a.add_to_storage(product_stacks=[product_stack_1000]))
print(storage_a)
print(len(storage_a))
print(storage_a.add_to_storage_forced(destination_storage=storage_a, product_stacks=[product_stack_100]))
print(storage_a)
print(len(storage_a))
