from core.models.users import User

def test_user():
    user  = User.get_by_id(1)
    _user = User.get_by_email('student1@fylebe.com')
    assert user == _user
    assert user.id == 1
    assert user.username == 'student1'
    assert user.email == 'student1@fylebe.com'
    assert user.created_at is not None
    assert user.updated_at is not None
    assert repr(user) == f"<User '{user.username}'>"


def test_http_exception(client):
    response = client.get('/not_found')
    assert response.status_code == 404
