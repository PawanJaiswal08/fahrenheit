from django import forms
from blog.models import Blog , BlogComment
from blog.models import unique_slug_generator 

class UpdateForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['titleBlog','name','content']
        
    def save(self, commit=True):
        blog = self.instance
        blog.titleBlog = self.cleaned_data['titleBlog']
        blog.name = self.cleaned_data['name']
        blog.content = self.cleaned_data['content']
        blog.slug = unique_slug_generator(blog)

        if commit:
            blog.save()
        return blog
    
class CommentForm(forms.ModelForm):
    class Meta:
        model = BlogComment
        fields = ['comment']

        widgets={
            'comment' : forms.TextInput(attrs={'class' : 'form-control'})
        }