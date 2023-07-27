from django.contrib.auth.models import Group
from urllib.request import urlopen
from django.core.files import File
import tempfile

def add_groups(backend, user, response, *args, **kwargs):
    if user.groups.all().count() == 0:
        group = Group.objects.get(name=backend.name)
        user.groups.add(group)
    if not user.name:
        user.name = response['name']
        user.save()
    print(response)
    if user.profile_picture == "user_base.jpg":
        if backend.name == 'facebook':
            with urlopen(response['picture']['data']['url']) as uo:
                assert uo.status == 200
                with tempfile.NamedTemporaryFile(delete=True) as img_tmp:
                    img_tmp.write(uo.read())
                    img_tmp.flush()
                    img = File(img_tmp)
                    user.profile_picture.save(f'image_{user.name}.png', img)
                    user.save()
        else:
            with urlopen(response['picture']) as uo:
                assert uo.status == 200
                with tempfile.NamedTemporaryFile(delete=True) as img_tmp:
                    img_tmp.write(uo.read())
                    img_tmp.flush()
                    img = File(img_tmp)
                    user.profile_picture.save(f'image_{user.name}.png', img)
                    user.save()
