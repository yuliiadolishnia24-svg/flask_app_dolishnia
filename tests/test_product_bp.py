import unittest
from app import create_app

class ProductBPTestCase(unittest.TestCase):
    def setUp(self):
        app = create_app()
        app.config["TESTING"] = True
        self.client = app.test_client()

    def test_product_list(self):
        response = self.client.get("/products/list")
        self.assertEqual(response.status_code, 200)

        # Декодуємо байти у рядок
        html = response.data.decode('utf-8')

        self.assertIn("Яблуко", html)
        self.assertIn("Банан", html)
        self.assertIn("Апельсин", html)

if __name__ == "__main__":
    unittest.main()
