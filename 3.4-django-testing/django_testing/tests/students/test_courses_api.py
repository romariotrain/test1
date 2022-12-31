import pytest as pytest
from rest_framework.test import APIClient
from model_bakery import baker
from students.models import Student, Course


@pytest.fixture
def client():
    return APIClient()

@pytest.fixture
def course_factory():
    def course(*args, **kwargs):
        return baker.make(Course, *args, **kwargs)
    return course



@pytest.fixture
def student_factory():
    def student(*args, **kwargs):
        return baker.make(Student, *args, **kwargs)
    return student

@pytest.mark.django_db
def test_current_course(course_factory, client):
    course_factory(_quantity=10)
    course_id = 1
    response = client.get(f'/courses/{course_id}/')
    assert response.status_code == 200
    data1 = response.json()
    assert data1['id'] == course_id
#
#
@pytest.mark.django_db
def test_list_course(course_factory, client):
    courses = course_factory(_quantity=10)
    response = client.get(f'/courses/')
    assert response.status_code == 200
    data = response.json()
    assert len(data) == len(courses)

@pytest.mark.django_db
def test_course_filter_id(course_factory, client):
    courses = course_factory(_quantity=10)
    course_id = courses[2].id
    response = client.get(f'/courses/?id={course_id}')
    assert response.status_code == 200
    data = response.json()
    assert data[0]['id'] == course_id


@pytest.mark.django_db
def test_course_filter_name(course_factory, client):
    courses = course_factory(_quantity=10)
    course_name = courses[3].name
    response = client.get(f'/courses/?name={course_name}')
    assert response.status_code == 200
    data = response.json()
    assert data[0]['name'] == course_name


@pytest.mark.django_db
def test_create_course(client):
    response = client.post(f'/courses/', {'name' : 'new_name'})
    assert response.status_code == 201


@pytest.mark.django_db
def test_change_course(course_factory, client):
    courses = course_factory(_quantity=10)
    course_id = courses[2].id
    response = client.patch(f'/courses/{course_id}/', {'name': 'new_name'})
    assert response.status_code == 200

@pytest.mark.django_db
def test_delete_course(course_factory, client):
    courses = course_factory(_quantity=10)
    course_id = courses[2].id
    response = client.delete(f'/courses/{course_id}/')
    assert response.status_code == 204



