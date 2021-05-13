import unittest
from flask import url_for
from flask_testing import TestCase
from application import app, db
from application.models import Games

class TestBase(TestCase):
    def create_app(self):

        app.config.update(SQLALCHEMY_DATABASE_URI="sqlite:///data.db",
                SECRET_KEY='TEST_SECRET_KEY',
                DEBUG=True,
                WTF_CSRF_ENABLED=False
                )
        return app

    def setUp(self):
        """
        Will be called before every test
        """
        db.create_all()
        test_monopoly = Games(
                    game_name='Monopoly', 
                    age_rating=3,
                    genre='Board Game',
                    description='Destroys friendships',
                    rated = True
                )
        db.session.add(test_monopoly)
        test_farming = Games(
                    game_name='Farming Simulator', 
                    age_rating=3,
                    genre='Simulation',
                    description='Pretend to be a farmer',
                    rated = True
                )
        db.session.add(test_farming)
        test_doom = Games(
                    game_name='Doom', 
                    age_rating=18,
                    genre='First person shooter',
                    description='Shoot all the demons',
                    rated = False
                )
        db.session.add(test_doom)
        test_warhammer = Games(
                    game_name='Total War:Warhammer 2',
                    age_rating=18,
                    genre='Strategy',
                    description='Better than the tabletop version',
                    rated=False
        )
        db.session.add(test_warhammer)
        db.session.commit()

    def tearDown(self):
        """
        Will be called after every test
        """

        db.session.remove()
        db.drop_all()

class TestViews(TestBase):
    def test_home_get(self):
        response = self.client.get(url_for('home'))
        self.assertEqual(response.status_code, 200)

    def test_add_game_get(self):
        response = self.client.get(url_for('add_game'))
        self.assertEqual(response.status_code, 200)

    def test_update_get(self):
        response = self.client.get(url_for('update'))
        self.assertEqual(response.status_code, 200)
    
    def test_add_rating_get(self):
        response = self.client.get(url_for('add_rating'))
        self.assertEqual(response.status_code, 200)
    
    def test_delete_game_get(self):
        response = self.client.get(url_for('delete_game', id=1))
        self.assertEqual(response.status_code, 200)

class TestRead(TestBase):
    def test_read_tasks(self):
        response = self.client.get(url_for("home"))
        self.assertIn(b'Monopoly')