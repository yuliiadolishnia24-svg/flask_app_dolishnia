import unittest
from app import create_app, db
from app.posts.models import Post

class PostTestCase(unittest.TestCase):
    def setUp(self):
        # Створюємо додаток у тестовому режимі
        self.app = create_app()
        self.app.config.update({
            "TESTING": True,
            "WTF_CSRF_ENABLED": False,  # вимикаємо CSRF для тестів
            "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:"
        })
        self.client = self.app.test_client()

        # Створення бази в контексті додатка
        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        # Очистка бази після кожного тесту
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_create_post(self):
        # Надсилаємо POST-запит для створення нового поста
        response = self.client.post(
            "/post/create",
            data={
                "title": "My first post",
                "content": "This is TDD",
                "is_active": "y",
                "publish_date": "2025-12-14T15:00",
                "category": "news"
            },
            follow_redirects=True
        )

        # Перевірка редіректу на список постів
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"My first post", response.data)  # перевіряємо, що заголовок зʼявився на сторінці

        # Перевірка, що пост додано в базу
        with self.app.app_context():
            post = Post.query.filter_by(title="My first post").first()
            self.assertIsNotNone(post)
            self.assertEqual(post.content, "This is TDD")
            self.assertEqual(post.category, "news")
            self.assertTrue(post.is_active)
