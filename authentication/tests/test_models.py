from rest_framework.test import APITestCase
from authentication.models import User



class TestModel(APITestCase):
    def test_create_user(self):
       
        user=User.objects.create_user('john','john@gmail.com','password123!@')
        self.assertFalse(user.is_staff)
        self.assertIsInstance(user,User)
        self.assertEqual(user.email,'john@gmail.com')



    def test_create_superuser(self):
       
        user=User.objects.create_superuser('john','john@gmail.com','password123!@')
        self.assertTrue(user.is_staff)
        self.assertIsInstance(user,User)
        self.assertEqual(user.email,'john@gmail.com')

    def test_raise_error_no_usename_is_supplied(self):
        
        self.assertRaises(ValueError,User.objects.create_user,username='',email='john@gmail.com',password='password123!@')
        self.assertRaisesMessage(ValueError,'The given username must be set')
       

    
    def test_raise_error_no_email_is_supplied(self):
        
        self.assertRaises(ValueError,User.objects.create_user,username='john',email='',password='password123!@')
        self.assertRaisesMessage(ValueError,'The given email must be set')
       
    def test_craete_super_user_with_is_stuff_status(self):
        with self.assertRaisesMessage(ValueError,'Superuser must have is_staff=True'):
            User.objects.create_superuser(username='john',email='john@gmail.com',password='password123!@',is_staff=False)
       
    def test_craete_super_user_with_super_user_status(self):
        
        with self.assertRaisesMessage(ValueError,'Superuser must have is_superuser=True.'):
            User.objects.create_superuser(username='john',email='john@gmail.com',password='password123!@',is_superuser=False)
       
    