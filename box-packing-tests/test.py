from py3dbp import Packer, Bin, Item

# All dimensions are in inches
box_list = [
    Bin('small_0', 3, 3, 3, 100),
    Bin('small_1', 3, 4, 3, 100),
    Bin('small_2', 4, 4, 4, 100),
    Bin('small_3', 5, 5, 5, 100),
    Bin('medium', 6, 6, 6, 100),
    Bin('large', 7, 7, 7, 100)
]

def get_packages():
    """Gets the package sizes from the user and
    calculates the total volume of the packages
    
    Returns: packages_list and volume of packages
    """
    packages_list = []
    total_volume = 0
    number_of_packages = int(input("How many packages? "))
    for i in range(1, number_of_packages + 1):
        print(" ")
        print(f"Data for Package {i}.")
        width = int(input("Width? ")) 
        height = int(input("Height? "))
        depth= int(input("Depth? "))
        total_volume += (width * height * width)
        packages_list.append({"name": str(i), "width": width, "height": height, "depth": depth})
    return (packages_list, total_volume)

packages, packages_volume = get_packages()

for box in box_list:
    packer = Packer()
    packer.add_bin(box)
    for package in packages:
        packer.add_item(Item(package["name"], package["width"], package["height"], package["depth"], 0.1))      
    packer.pack(number_of_decimals=0)
    if box.unfitted_items == []:
        print("All items fit!")
        print(" ")
        fit_box = box
        break    

print(" ")
print(box.name)
print(f'Volume of box: {box.width * box.height * box.depth} cubic inches')
print(f'Volume of packages: {packages_volume} cubic inches')
print(" ")
