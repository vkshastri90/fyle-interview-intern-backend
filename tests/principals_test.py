from core.models.assignments import AssignmentStateEnum, GradeEnum
from core.models.principals  import Principal

def test_principal():
    principal = Principal.query.get(1)

    assert principal.id is not None
    assert principal.user_id is not None
    assert principal.created_at is not None
    assert principal.updated_at is not None
    assert repr(principal) == f'<Principal {principal.id}>'


def test_get_teachers(client, h_principal):
    response = client.get(
        '/principal/teachers',
        headers=h_principal
    )
    assert response.status_code == 200
    teacher_list = response.json['data']
    assert isinstance(teacher_list, list)
    assert len(teacher_list) > 0

    for teacher in teacher_list:
        assert isinstance(teacher, dict)
        assert 'id' in teacher
        assert 'user_id' in teacher


def test_get_assignments(client, h_principal):
    response = client.get(
        '/principal/assignments',
        headers=h_principal
    )

    assert response.status_code == 200

    data = response.json['data']
    for assignment in data:
        assert assignment['state'] in [AssignmentStateEnum.SUBMITTED, AssignmentStateEnum.GRADED]


def test_grade_assignment_draft_assignment(client, h_principal):
    """
    failure case: If an assignment is in Draft state, it cannot be graded by principal
    """
    response = client.post(
        '/principal/assignments/grade',
        json={
            'id': 5,
            'grade': GradeEnum.A.value
        },
        headers=h_principal
    )

    assert response.status_code == 400


def test_grade_assignment(client, h_principal):
    response = client.post(
        '/principal/assignments/grade',
        json={
            'id': 4,
            'grade': GradeEnum.C.value
        },
        headers=h_principal
    )

    assert response.status_code == 200

    assert response.json['data']['state'] == AssignmentStateEnum.GRADED.value
    assert response.json['data']['grade'] == GradeEnum.C


def test_regrade_assignment(client, h_principal):
    response = client.post(
        '/principal/assignments/grade',
        json={
            'id': 4,
            'grade': GradeEnum.B.value
        },
        headers=h_principal
    )

    assert response.status_code == 200

    assert response.json['data']['state'] == AssignmentStateEnum.GRADED.value
    assert response.json['data']['grade'] == GradeEnum.B
