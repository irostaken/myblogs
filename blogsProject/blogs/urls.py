from django.urls import path

from .views import tests, index
from .views.sidebar import articles, contact, export, supports
from .views import account, home

app_name = 'blogs'
urlpatterns = [
    path('test/', tests.test),

    path('', index.IndexView.as_view(), name='index'),

    path('articles/', articles.ArticleView.as_view(), name="articles"),
    path('articles/add/', articles.AddView.as_view(), name="add_article"),
    path('articles/edit/<int:article_id>', articles.EditView.as_view(), name="edit_article"),
    path('articles/detail/<int:article_id>', articles.DetailView.as_view(), name="detail_article"),
    path('articles/<str:article_type>/', articles.ArticleView.as_view(), name="articles"),

    path('supports/', supports.SupportView.as_view(), name="supports"),
    path('contact/', contact.ContactView.as_view(), name="contact"),
    path('export/', export.ExportView.as_view(), name="export"),

    path('login/', account.AuthView.as_view(), name="auth"),
    path('logout/', account.logout, name="logout"),

    path('home/', home.HomeView.as_view(), name='home'),
]
