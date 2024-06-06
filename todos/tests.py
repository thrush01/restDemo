from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from . models import Todo


class TodoAPITestCase(APITestCase):
    def create_todo(self):
        sample_todo={'title':'hello','description':'test'}
        response=self.client.post(reverse('todos'),sample_todo)

        return response


    
    def authenticate(self):
        self.client.post(reverse('register'),{'username':'username','email':'email@email.com','password':'password'})
        response=self.client.post(reverse('login'),{'email':'email@email.com','password':'password'})
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {response.data['token']}")
        

class TestListCreateTodos(TodoAPITestCase):

    def test_should_no_create_todo_with_no_auth(self):
        response=self.create_todo()
        self.assertEqual(response.status_code,status.HTTP_403_FORBIDDEN)

    
    def test_should_create_todo(self):
        previous_todo_count=Todo.objects.all().count()
        self.authenticate()
        response=self.create_todo()
        self.assertEqual(Todo.objects.all().count(),previous_todo_count+1)
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'],'hello')
        self.assertEqual(response.data['description'],'test')

    def test_retrieves_all(self):
        self.authenticate()
        response=self.client.get(reverse('todos'))
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertIsInstance(response.data['results'],list)
        self.create_todo()
        res=self.client.get(reverse('todos'))
        self.assertEqual(res.data['count'],1)
        self.assertIsInstance(res.data['count'],int)

        

class TestTodoAPIView(TodoAPITestCase):

    def test_retrieves_one_item(self):
        self.authenticate()
        response=self.create_todo()
        res=self.client.get(reverse('todo',kwargs={'id':response.data['id']}))

        self.assertEqual(res.status_code,status.HTTP_200_OK)

        todo=Todo.objects.get(id=response.data['id'])
        self.assertEqual(res.data['title'],todo.title)



    def test_update_one_item(self):
        self.authenticate()
        response=self.create_todo()
        res=self.client.patch(reverse('todo',kwargs={'id':response.data['id']}),{
            'title':'new title',
            'is_completed':True
            
        })
        self.assertEqual(res.status_code,status.HTTP_200_OK)
        updated_todo=Todo.objects.get(id=response.data['id'])

        self.assertEqual(updated_todo.is_completed,True)
        self.assertEqual(updated_todo.title,'new title')



    def test_deletes_one_item(self):
        self.authenticate()
        res=self.create_todo()
        prev_db_count=Todo.objects.all().count()

        self.assertGreater(prev_db_count,0)
        self.assertEqual(prev_db_count,1)

        response=self.client.delete(reverse('todo',kwargs={'id':res.data['id']}))

        self.assertEqual(response.status_code,status.HTTP_204_NO_CONTENT)

        self.assertEqual(Todo.objects.all().count(),0)