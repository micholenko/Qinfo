import pytest
from flask import url_for
from app.models import User
from app import db, app
from tests import client


@pytest.fixture
def setup_db():
    with app.app_context():
        db.create_all()


def test_tst(client):
    assert True


def test_create_study(client):
    response = client.post(url_for('studies.create_study'), json={'title': 'Test Study', 'question': 'What is your favorite color?',
                                                                  'description': 'This is a study about colors',
                                                                  'distribution': [1, 2, 3, 2, 1],
                                                                  'col_values': [-2, -1, 0, 1, 2],
                                                                  })
    assert response.status_code == 200
    assert response.json.items() >= {'id': 1, 'title': 'Test Study', 'question': 'What is your favorite color?',
                                     'description': 'This is a study about colors', 'status': 'not_started'}.items()


def test_get_study(client):
    # create a study
    response = client.post(url_for('studies.create_study'), json={'title': 'Test Study', 'question': 'What is your favorite color?',
                                                                  'description': 'This is a study about colors',
                                                                  'distribution': [1, 2, 3, 2, 1],
                                                                  'col_values': [-2, -1, 0, 1, 2],
                                                                  })

    id = response.json['id']
    response = client.get(url_for('studies.get_study', id=id))
    assert response.status_code == 200
    assert response.json.items() >= {'id': 1, 'title': 'Test Study', 'question': 'What is your favorite color?',
                                     'description': 'This is a study about colors', 'status': 'not_started'}.items()


def test_get_studies(client):
    response = client.get(url_for('studies.get_studies'))
    assert response.status_code == 200
    assert response.json == []

    response = client.post(url_for('studies.create_study'), json={'title': 'Test Study', 'question': 'What is your favorite color?',
                                                                  'description': 'This is a study about colors',
                                                                  'distribution': [1, 2, 3, 2, 1],
                                                                  'col_values': [-2, -1, 0, 1, 2],
                                                                  })
    id1 = response.json['id']
    response = client.post(url_for('studies.create_study'), json={'title': 'Test Study 2', 'question': 'What is your favorite animal?',
                                                                  'description': 'This is a study about animals',
                                                                  'distribution': [1, 2, 3, 2, 1],
                                                                  'col_values': [-2, -1, 0, 1, 2],
                                                                  })

    id2 = response.json['id']

    response = client.get(url_for('studies.get_studies'))
    assert response.status_code == 200
    assert response.json[0]['id'] == id1
    assert response.json[1]['id'] == id2


def test_update_study(client):
    response = client.post(url_for('studies.create_study'), json={'title': 'Test Study', 'question': 'What is your favorite color?',
                                                                  'description': 'This is a study about colors',
                                                                  'distribution': [1, 2, 3, 2, 1],
                                                                  'col_values': [-2, -1, 0, 1, 2],
                                                                  })
    id = response.json['id']
    response = client.patch(url_for('studies.update_study', id=id), json={
                            'status': 'in_progress'})
    assert response.status_code == 200
    assert response.json.items() >= {'id': 1, 'title': 'Test Study', 'question': 'What is your favorite color?',
                                     'description': 'This is a study about colors', 'status': 'in_progress'}.items()


def test_delete_study(client):
    response = client.post(url_for('studies.create_study'), json={'title': 'Test Study', 'question': 'What is your favorite color?',
                                                                  'description': 'This is a study about colors',
                                                                  'distribution': [1, 2, 3, 2, 1],
                                                                  'col_values': [-2, -1, 0, 1, 2],
                                                                  })
    id = response.json['id']
    response = client.get(url_for('studies.get_studies'))
    assert response.status_code == 200
    assert len(response.json) == 1
    response = client.delete(url_for('studies.delete_study', id=id))
    assert response.status_code == 200
    response = client.get(url_for('studies.get_studies'))
    assert response.status_code == 200
    assert len(response.json) == 0
