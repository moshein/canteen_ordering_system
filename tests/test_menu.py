import unittest

from menu import Food, Meal, ReadyToEat, Menu, ItemNotFoundError, EmptyMenuError, InvalidQuantityError, PriceMismatchError 

class TestFood(unittest.TestCase):

    ## Testing whether meal object is created successfully
    def test_create_meal(self):
        burger = Meal("Burger", 90)

        self.assertEqual(burger.name, "Burger")
        self.assertEqual(burger.price, 90.00)
        self.assertEqual(burger.food_type, "Meal")

    ## testing whether ReadyToEat object is created successfully
    def test_create_readyToEat(self):
        fita = ReadyToEat("Fita", 15)

        self.assertEqual(fita.name, "Fita")
        self.assertEqual(fita.price, 15.00)
        self.assertEqual(fita.food_type, "Ready-To-Eat")

    ## testing whether invalid name type raises error
    def test_invalid_name(self):
        with self.assertRaises(TypeError):
            Meal(345, 80)

    ## testing whether invalid price type raises error
    def test_invalid_price(self):
        with self.assertRaises(TypeError):
            Meal("Pasta", "asdf")

    ## testing whether zero price raises error
    def test_zero_price(self):
        with self.assertRaises(ValueError):
            Meal("Tinola", 0)

    ## testing whether negative price raises error
    def test_neg_price(self):
        with self.assertRaises(ValueError):
            Meal("Fried Chicken", -2)

class TestMenu(unittest.TestCase):
    def setUp(self):
        self.menu = Menu()
        self.burger = Meal("Burger", 90)

    ## testing if food item is successfully added
    def test_add_item(self):
        self.menu.add_item(self.burger, 5)
        self.assertEqual(len(self.menu.menu), 1)
        self.assertEqual(self.menu.menu[0][1], "Burger")
        self.assertEqual(self.menu.menu[0][2], 90.00)
        self.assertEqual(self.menu.menu[0][3], 5)

    ## testing if invalid item raises error
    def test_invalid_item(self):
        with self.assertRaises(TypeError):
            self.menu.add_item("Burger", 5)

    ## testing if zero quantity raises error
    def test_zero_quantity(self):
        with self.assertRaises(InvalidQuantityError):
            self.menu.add_item(self.burger, 0)

    ## testing if negative quantity raises error
    def test_negative_quantity(self):
        with self.assertRaises(InvalidQuantityError):
            self.menu.add_item(self.burger, -3)

    ## testing if duplicate food item increases existing quantity
    def test_duplicate_item(self):
        self.menu.add_item(self.burger, 5)
        self.menu.add_item(self.burger, 3)

        self.assertEqual(len(self.menu.menu), 1)
        self.assertEqual(self.menu.menu[0][3], 8)

    ## testing if duplicate food item with different price raises error
    def test_duplicate_item_different_price(self):
        self.menu.add_item(self.burger, 5)
        new_burger = Meal("Burger", 100)

        with self.assertRaises(PriceMismatchError):
            self.menu.add_item(new_burger, 3)

        self.assertEqual(self.menu.menu[0][2], 90.00)
        self.assertEqual(self.menu.menu[0][3], 5)

    ## testing if has_item detects existing food item
    def test_has_item(self):
        self.menu.add_item(self.burger, 5)

        self.assertTrue(self.menu.has_item("Burger"))
        self.assertFalse(self.menu.has_item("Pizza"))

    ## testing if remove_item successfully removes a food item
    def test_remove_item(self):
        self.menu.add_item(self.burger, 5)
        self.menu.remove_item("Burger")

        self.assertEqual(len(self.menu._menu), 0)


    ## testing if the copy() works in menu
    def test_menu_copy(self):
        self.menu.add_item(self.burger, 5)

        result = self.menu.menu
        result.clear()

        self.assertEqual(len(self.menu.menu), 1)

    ## testing if available_items work by returning positive stock
    def test_available_items(self):
        self.menu.add_item(self.burger, 7)

        result = self.menu.available_items

        self.assertEqual(len(result), 1)
        self.assertGreater(result[0][3], 0)

    ## testing if unavailable_items work by returning zero stocks
    def test_unavailable_items(self):
        self.menu._menu.append(["Meal", "Adobo", 80, 0])

        result = self.menu.unavailable_items

        self.assertEqual(result[0][3], 0)



if __name__ == "__main__":
    unittest.main()

