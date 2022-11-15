from rest_framework.test import APIClient
from rest_framework.test import APITestCase
from .models import CommentModel,PostModel,StoryModel
from users.models import CustomUser
from rest_framework.reverse import reverse
from rest_framework.authtoken.models import Token
from django.core.files.uploadedfile import SimpleUploadedFile
# Create your tests here.

class BookCommentTestCase(APITestCase):
    def setUp(self):
        self.create_by = CustomUser.objects.create(username = 'shexroz',first_name='Toshpolatov')
        self.create_by.set_password('someward')
        self.create_by.save()

        self.post = PostModel.objects.create(post_title = 'Bu zor kitob',post_creator=self.create_by)
        self.create_by.save()
        self.responce_one = self.client.post(
            reverse('users:login'),
            data={
                "username":"shexroz",
                "password":'someward',
            }
        )
        self.token = self.responce_one.data['token']
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

    def test_book_review_detail_get(self):
        
        comment = CommentModel.objects.create(
            feed_by = self.post,create_by = self.create_by,comment='I like this book'
        )
        responce = self.client.get(reverse('feed:comment_detail',kwargs={"id":comment.id}))
        self.assertEqual(responce.status_code,200)
        self.assertEqual(responce.data['id'],comment.id)
        self.assertEqual(responce.data['create_by']['username'],'shexroz')
        self.assertEqual(responce.data['feed_by'],self.post.id)

    def test_book_review_detail_delete(self):
        comment = CommentModel.objects.create(
            feed_by = self.post,create_by = self.create_by,comment='I like this book'
            )
        responce = self.client.delete(reverse('feed:comment_detail',kwargs={"id":comment.id}))
        self.assertEqual(responce.status_code,404)
       
    
    def test_book_review_detail_put(self):
        comment = CommentModel.objects.create(
            feed_by = self.post,create_by = self.create_by,comment='I like this book'
            )
        responce = self.client.put(
            reverse('feed:comment_detail',kwargs={"id":comment.id}),
            data={
                "comment":"Assalomu alaykum"
            },
            headers = {"Authorization": f"Bearer{self.token}"}
        )
        self.assertEqual(responce.status_code,201)
        self.assertEqual(responce.data['comment'],"Assalomu alaykum")
    
    def test_comment_get(self):
        post_two = PostModel.objects.create(post_title = 'Bu zor kitob',post_creator=self.create_by)
        comment1 = CommentModel.objects.create(
            feed_by = self.post,create_by = self.create_by,comment='I like this book'
            )
        comment1 = CommentModel.objects.create(
            feed_by = post_two,create_by = self.create_by,comment='My Book'
            )
        responce = self.client.get(reverse('feed:comment_detail',kwargs={"id":post_two.id}))
        self.assertEqual(responce.status_code,200)
        self.assertEqual(responce.data['id'],2)
    
    def test_book_review_detail_post(self):
        comment = CommentModel.objects.create(
            feed_by = self.post,create_by = self.create_by,comment='I like this book'
            )
        responce = self.client.post(
            reverse('feed:comments',kwargs={"id":comment.id}),
            data={
                "comment":"Assalomu alaykum"
            },
            headers = {"Authorization": f"Bearer{self.token}"}
        )
        self.assertEqual(responce.status_code,201)
        self.assertEqual(responce.data['comment'],"Assalomu alaykum")

    
    
class PostTestCase(APITestCase):
    def setUp(self):
        self.create_by = CustomUser.objects.create(username = 'shexroz',first_name='Toshpolatov')
        self.create_by.set_password('someward')
        self.create_by.save()

        self.post = PostModel.objects.create(post_title = 'Bu zor kitob',post_creator=self.create_by)
        self.create_by.save()
        self.responce_one = self.client.post(
            reverse('users:login'),
            data={
                "username":"shexroz",
                "password":'someward',
            }
        )
        # get token
        self.token = self.responce_one.data['token']
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
    

    def test_post_get(self):
        
        responce = self.client.get(reverse('feed:feeds'))
        self.assertAlmostEqual(responce.status_code,200)
        self.assertAlmostEqual(responce.data[0]['id'],1)
        self.assertAlmostEqual(responce.data[0]['post_title'],'Bu zor kitob')
    def test_post_post(self):
        data =  open("D:\Backent\Bookweb\static\sh.png","rb")    
        data = SimpleUploadedFile(
        content=data.read(), name=data.name, content_type="multipart/form-data"
        )

        responce = self.client.post(reverse('feed:feeds'),
        {
            "post_title":"i created this post",
            "post_image":data
        },
        headers = {
            "Authorization": f"Bearer{self.token}",
            'Content-Type':'multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW',},
        format="multipart"
        )
        data.close()
      
        self.assertEqual(responce.status_code,201)
        self.assertEqual(responce.data['post_title'],"i created this post")

class PostDetailTestCase(APITestCase):
    def setUp(self):
        self.create_by = CustomUser.objects.create(username = 'shexroz',first_name='Toshpolatov')
        self.create_by.set_password('someward')
        self.create_by.save()

        self.post = PostModel.objects.create(post_title = 'Bu zor kitob',post_creator=self.create_by)
        self.create_by.save()
        self.responce_one = self.client.post(
            reverse('users:login'),
            data={
                "username":"shexroz",
                "password":'someward',
            }
        )
        # get token
        self.token = self.responce_one.data['token']
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

    def test_post_get(self):
        responce = self.client.get(reverse('feed:detail',kwargs={"id":self.post.id}))
        self.assertAlmostEqual(responce.status_code,200)
        self.assertAlmostEqual(responce.data['post_title'],'Bu zor kitob')

    def test_post_put(self):
        data =  open("D:\Backent\Bookweb\static\sh.png","rb")    
        data = SimpleUploadedFile(
        content=data.read(), name=data.name, content_type="multipart/form-data"
        )

        responce = self.client.put(reverse('feed:detail',kwargs={"id":self.post.id}),
        {
            "post_title":"i created this post",
            "post_image":data
        },
        headers = {
            "Authorization": f"Bearer{self.token}",
            'Content-Type':'multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW',},
        format="multipart"
        )
        data.close()
      
        self.assertEqual(responce.status_code,201)
        self.assertEqual(responce.data['post_title'],"i created this post")
    
    def test_post_delete(self):
        data =  open("D:\Backent\Bookweb\static\sh.png","rb")    
        data = SimpleUploadedFile(
        content=data.read(), name=data.name, content_type="multipart/form-data"
        )

        responce = self.client.delete(reverse('feed:detail',kwargs={"id":self.post.id}),
        headers = {
            "Authorization": f"Bearer{self.token}",\
            'Content-Type':'multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW',},
        format="multipart"
        )
        data.close()
      
        self.assertEqual(responce.status_code,404)
        self.assertEqual(responce.data['state'],False)
    
    def test_post_like(self):
        responce = self.client.get(reverse('feed:like',kwargs={"id":self.post.id}),
        # put like
        headers = {
            "Authorization": f"Bearer{self.token}",\
            'Content-Type':'multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW',},
        format="multipart"
        )
      
        self.assertEqual(responce.status_code,201)

        # get like
        responce = self.client.get(reverse('feed:like',kwargs={"id":self.post.id}),
        headers = {
            "Authorization": f"Bearer{self.token}",\
            'Content-Type':'multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW',},
        format="multipart"
        )
        self.assertEqual(responce.status_code,404)
       
class StoryTestCase(APITestCase):
    def setUp(self):
        self.create_by = CustomUser.objects.create(username = 'shexroz',first_name='Toshpolatov')
        self.create_by.set_password('someward')
        self.create_by.save()
        data =  open("D:\Backent\Bookweb\static\sh.png","rb")    
        data = SimpleUploadedFile(
        content=data.read(), name=data.name, content_type="multipart/form-data"
        )
        self.story = StoryModel.objects.create(
            story_image = data,story_creator=self.create_by,
            )
        self.responce_one = self.client.post(
            reverse('users:login'),
            data={
                "username":"shexroz",
                "password":'someward',
            }
        )
        # get token
        self.post = PostModel.objects.create(post_title = 'Bu zor kitob',post_creator=self.create_by)
        self.token = self.responce_one.data['token']
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        data.close()
    
    def test_story_get(self):
        responce = self.client.get(reverse('feed:story'),
        # put like
        headers = {
            "Authorization": f"Bearer{self.token}",\
            'Content-Type':'multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW',},
        format="multipart"
        )
        self.assertEqual(responce.status_code,200)
        self.assertEqual(responce.data[0]['id'],1)
        self.assertEqual(responce.data[0]['story_creator']['username'],'shexroz')
    
    def test_story_post(self):
        data =  open("D:\Backent\Bookweb\static\sh.png","rb")    
        data = SimpleUploadedFile(
        content=data.read(), name=data.name, content_type="multipart/form-data"
        )

        responce = self.client.post(reverse('feed:story'),
        {
            "story_image":data
        },
        headers = {
            "Authorization": f"Bearer{self.token}",
            'Content-Type':'multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW',},
        format="multipart"
        )
        data.close()
        self.assertEqual(responce.status_code,201)
        self.assertEqual(responce.data['story_creator']['username'],'shexroz')
    
    def test_story_seen(self):
        responce = self.client.get(reverse('feed:seen_story',kwargs={"id":self.story.id}),
        # put like
        headers = {
            "Authorization": f"Bearer{self.token}",\
            'Content-Type':'multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW',},
        format="multipart"
        )
        self.assertEqual(responce.status_code,200)
    
    def test_story_seen_personal(self):
        responce = self.client.get(reverse('feed:personal_story',kwargs={"id":self.create_by.id}),
        # put like
        headers = {
            "Authorization": f"Bearer{self.token}",\
            'Content-Type':'multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW',},
        format="multipart"
        )
        self.assertEqual(responce.status_code,200)
        self.assertEqual(responce.data['story_creator']['username'],'shexroz')
    
    def test_notifications(self):
        responce = self.client.get(reverse('feed:notifications'),
        # put like
        headers = {
            "Authorization": f"Bearer{self.token}",\
            'Content-Type':'multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW',},
        format="multipart"
        )
        self.assertEqual(responce.status_code,200)
    
    def test_favorite(self):
        responce = self.client.get(reverse('feed:favorite_detail',kwargs={"id":self.post.id}),
        
        headers = {
            "Authorization": f"Bearer{self.token}",\
            'Content-Type':'multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW',},
        format="multipart"
        )
        self.assertEqual(responce.status_code,201)
        responce = self.client.get(reverse('feed:favorite_detail',kwargs={"id":self.post.id}),
        
        headers = {
            "Authorization": f"Bearer{self.token}",\
            'Content-Type':'multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW',},
        format="multipart"
        )
        self.assertEqual(responce.status_code,400)
        
        responce = self.client.get(reverse('feed:favorite_all'),
        
        headers = {
            "Authorization": f"Bearer{self.token}",\
            'Content-Type':'multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW',},
        format="multipart"
        )
        self.assertEqual(responce.status_code,200)
        self.assertEqual(responce.data[0]['favorite_post']['id'],self.post.id)
    
    def test_favorite_post_delete(self):
        responce = self.client.get(reverse('feed:favorite_detail',kwargs={"id":self.post.id}),
        
        headers = {
            "Authorization": f"Bearer{self.token}",\
            'Content-Type':'multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW',},
        format="multipart"
        )
        self.assertEqual(responce.status_code,201)

        responce = self.client.delete(reverse('feed:favorite_detail',kwargs={"id":self.post.id}),
        
        headers = {
            "Authorization": f"Bearer{self.token}",\
            'Content-Type':'multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW',},
        format="multipart"
        )
        self.assertEqual(responce.status_code,404)
        